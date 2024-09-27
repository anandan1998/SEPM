class Piece:
    def __init__(self, player, selected=False):
        self.player = player
        self.selected = selected

    def set_selected(self,selected):
        self.selected = selected
        