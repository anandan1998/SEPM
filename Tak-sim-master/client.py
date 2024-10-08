import socket, sys, json, os, time, pdb
import math
from Game import Game
from Board import Board
import argparse
from Communicator import Communicator

class Client(Communicator):
    def __init__(self):
        self.GAME_TIMER = 100000  # in Milli Seconds
        self.NETWORK_TIMER = 150
        super().__init__()  # Updated super() syntax

    def setNetworkTimer(self, Time_in_Seconds):
        self.NETWORK_TIMER = Time_in_Seconds

    def getNetworkTimer(self):
        return self.NETWORK_TIMER

    def getGameTimer(self):
        return self.GAME_TIMER // 1000

    def setGameTimer(self, Time_in_Seconds):
        self.GAME_TIMER = Time_in_Seconds * 1000

    def CheckExeFile(self, Execution_Command, Executable_File):
        """Checks the existence of the Executable File and
		if the extension of the file matches the command used to run it.

		Args:
			Execution_Command : Command used to execute the Executable File (sh, python ./ etc)
			Executable_File : The Executable File
		Returns:
			None
		"""
        Extension = Executable_File.split('.')
        if len(Extension) == 1:
            return False
        Extension = Extension[-1]
        if os.path.isfile(Executable_File):
            if Execution_Command == './' or Execution_Command == 'sh':
                if Extension == 'sh' or Extension == 'o':
                    return True
                else:
                    return False
            elif Execution_Command == 'java':
                if Extension == 'java':
                    return True
                else:
                    return False
            elif Execution_Command == 'python':
                if Extension == 'py':
                    return True
                else:
                    return False
        else:
            return False

    def CreateChildProcess(self, Execution_Command, Executable_File):
        """Creates a Process, with which the client communicates.
		Checks the existence of the Executable_File and some basic
		checks for whether the Execution_Command used to run the code
		matches the extension of the Executable File
		Prints if error is found
		"""
        if self.CheckExeFile(Execution_Command, Executable_File):
            super().CreateChildProcess(Execution_Command, Executable_File)
        else:
            print(
                f'ERROR: EITHER FILE {Executable_File} DOES NOT EXIST OR THE EXECUTION COMMAND TO RUN THE FILE {Execution_Command} IS INCORRECT')

    def Connect2Server(self, server_address, port_no):
        """Connects to server with given IP Address and Port No."""
        self.clientSocket = socket.socket()
        self.clientSocket.connect((server_address, port_no))
        super().setSocket(self.clientSocket, self.NETWORK_TIMER)

    def SendData2Server(self, data):
        """Sends data (a dictionary) to the Server as a JSON object"""
        if data['action'] in ['KILLPROC', 'FINISH']:
            super().closeChildProcess()

        sendData = json.dumps(data)
        success_flag = super().SendDataOnSocket(sendData)

        if not success_flag:
            print('ERROR: FAILED TO SEND DATA TO SERVER')
            super().closeSocket()
        elif data['action'] in ['KILLPROC', 'FINISH']:
            super().closeSocket()

        return success_flag

    def RecvDataFromServer(self):
        """Receives data from the Server as a string and returns the move."""
        data = super().RecvDataOnSocket()

        retData = None
        if data is None:
            print('ERROR: TIMEOUT ON SERVER END')
            super().closeChildProcess()
            super().closeSocket()
        else:
            data = json.loads(data)
            if data['action'] in ['NORMAL', 'INIT']:
                retData = data['data']
            elif data['action'] == 'KILLPROC':
                print(f"ERROR: {data['meta']} ON OTHER CLIENT")
                super().closeChildProcess()
                super().closeSocket()
            elif data['action'] == 'FINISH':
                super().closeChildProcess()
                super().closeSocket()
                retData = data['data']
        return retData

    def RecvDataFromProcess(self):
        """Receives Data from the process."""
        start_time = time.time()
        BUFFER_TIMER = int(math.ceil(self.GAME_TIMER / 1000.0))
        print(f'Time remaining is: {BUFFER_TIMER}s')
        data = super().RecvDataOnPipe(BUFFER_TIMER)
        end_time = time.time()
        retData = None

        if data is None:
            print('ERROR: THIS CLIENT STOPPED UNEXPECTEDLY OR TIMED OUT')
            super().closeChildProcess()
            retData = {'meta': 'UNEXPECTED STOP', 'action': 'KILLPROC', 'data': ''}
        else:
            time_delta = max(1, int((end_time - start_time) * 1000))
            self.GAME_TIMER -= time_delta
            if self.GAME_TIMER > 0:
                retData = {'meta': '', 'action': 'NORMAL', 'data': data}
            else:
                retData = {'meta': 'TIMEOUT', 'action': 'KILLPROC', 'data': ''}
                print('ERROR: THIS CLIENT STOPPED UNEXPECTEDLY OR TIMED OUT')
        return retData

    def SendData2Process(self, data):
        """Sends Data (Move) to the process."""
        if data[-1] != '\n':
            data += '\n'
        success_flag = super().SendDataOnPipe(data)

        if not success_flag:
            print('ERROR: FAILED TO SEND DATA TO PROCESS')
            super().closeChildProcess()
        return success_flag


def game_loop(game, args):
    client = Client()
    if args.exe.endswith('.py'):
        client.CreateChildProcess('python', args.exe)
    elif args.exe.endswith('.sh'):
        client.CreateChildProcess('sh', args.exe)
    else:
        client.CreateChildProcess('sh', args.exe)
    client.Connect2Server(args.ip, args.port)
    server_string = client.RecvDataFromServer()
    if server_string is None:
        print('ERROR IN SETTING UP CONNECTIONS. SORRY')
        sys.exit(0)
    server_string_list = server_string.strip().split()
    player_id = server_string_list[0]
    board_size = int(server_string_list[1])
    game_timer = int(server_string_list[2])
    client.setGameTimer(game_timer)
    print(f'You are player {player_id}')
    print(f'You are allotted a time of {game_timer}s\n')
    client.SendData2Process(server_string)
    if args.mode == 'GUI':
        game.render_board.render(game)
    elif args.mode == 'CUI':
        game.render()
    if player_id == '2':
        move = client.RecvDataFromServer()
        if move:
            move = move.strip()
            print(f"The other player played {move}")
            success = game.execute_move(move)
            client.SendData2Process(move)
        else:
            sys.exit(0)
    while True:
        move = client.RecvDataFromProcess()
        if move['action'] == 'KILLPROC':
            move['meta'] += f' BY PLAYER {player_id}'
            client.SendData2Server(move)
            break
        move['data'] = move['data'].strip()
        print(f"You played {move['data']}")
        success = game.execute_move(move['data'])
        message = {}
        if success == 0:
            message['data'] = ''
            message['action'] = 'KILLPROC'
            message['meta'] = f'INVALID MOVE BY PLAYER {player_id}'
            print('INVALID MOVE ON THIS CLIENT')
        elif success in [2, 3, 4]:
            score = f"({game.calculate_score(0)}, {game.calculate_score(1)})"
            message['action'] = 'FINISH'
            message['data'] = move['data']
            if success == 2:
                message['meta'] = f'1 wins WITH SCORE: {score}'
                print('YOU WIN!' if player_id == '1' else 'YOU LOSE :(')
            elif success == 3:
                message['meta'] = f'2 wins WITH SCORE: {score}'
                print('YOU WIN!' if player_id == '2' else 'YOU LOSE :(')
            else:
                message['meta'] = f'Game Drawn WITH SCORE: {score}'
                print('GAME DRAWN')
        elif success == 1:
            message = move
        client.SendData2Server(message)
        if message['action'] in ['FINISH', 'KILLPROC']:
            break
        move = client.RecvDataFromServer()
        if move:
            move = move.strip()
            print(f"The other player played {move}")
            success = game.execute_move(move)
            if success in [2, 3, 4]:
                if success == 2:
                    print('YOU WIN!' if player_id == '1' else 'YOU LOSE :(')
                elif success == 3:
                    print('YOU WIN!' if player_id == '2' else 'YOU LOSE :(')
                else:
                    print('GAME DRAWN')
                break
            else:
                client.SendData2Process(move)
        else:
            break
    client.closeChildProcess()
    client.closeSocket()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tak client')
    parser.add_argument('ip', metavar='0.0.0.0', type=str, help='Server IP')
    parser.add_argument('port', metavar='10000', type=int, help='Server port')
    parser.add_argument('exe', metavar='run.sh', type=str, help='Your executable')
    parser.add_argument('-n', dest='n', metavar='N', type=int, default=5, help='Tak board size')
    parser.add_argument('-mode', dest='mode', type=str, default='GUI', help='How to render')
    args = parser.parse_args()
    game = Game(args.n, args.mode)
    if args.mode != 'GUI':
        game_loop(game, args)
    else:
        from threading import Thread

        Th = Thread(target=lambda: game_loop(game, args))
        Th.start()
        game.init_display()
        game.display.mainloop()