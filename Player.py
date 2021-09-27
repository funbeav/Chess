
class Player:
    def __init__(self, game, is_white):
        self.score = 0
        self.game = game
        self.is_white = is_white

    def __str__(self):
        if self.is_white:
            return "White"
        else:
            return "Black"

    def add_score(self, figure_name):
        if figure_name == "pawn":       # пешка
            self.score += 1
        elif figure_name == "bishop":   # слон
            self.score += 3
        elif figure_name == "knight":   # конь
            self.score += 3
        elif figure_name == "castle":   # ладья
            self.score += 5
        elif figure_name == "queen":    # ферзь
            self.score += 9
        elif figure_name == "king":     # король
            self.score += 10
