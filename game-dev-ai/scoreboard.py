import pickle


class scoreboard:
    scores_data = {}

    def __init__(self):
        pass

    def save_data(self, scores_data):
        with open("scores_data.pkl", "wb") as fp:
            pickle.dump(scores_data, fp)
            print("dictionary saved successfully to file")
        pass

    def read_data(self):
        with open("scores_data.pkl", "rb") as fp:
            self.scores_data = pickle.load(fp)
            print("scores")
            print(self.scores_data)
        return self.scores_data

    def update_data(self, scores_data):
        return False
