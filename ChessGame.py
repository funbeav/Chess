from Field import *
from Player import *


# Основной класс игры, содержит всю информацию о её состоянии
class Game:
    def __init__(self):
        self.moves_count = 1
        self.field = None
        self.player_white = None
        self.player_black = None
        self.current_player = None
        self.chosen_figure = None
        self.moves_history = list()
        self.last_move = tuple()
        self.pawn_reached_border = False
        self.pawn_to_figure_class = Queen
        self.check = False
        self.checkmate = False
        self.stalemate = False

    def __str__(self):
        if self.chosen_figure:
            steps_count = self.chosen_figure.steps_count
        else:
            steps_count = 0
        info = f"Game #\n" \
               f"Move #{self.moves_count}\n" \
               f"Player White Score: {self.player_white.score}\n" \
               f"Player Black Score: {self.player_black.score}\n" \
               f"Moves History: {self.moves_history}\n" \
               f"Current Player: {self.current_player}\n" \
               f"Chosen Figure: {self.chosen_figure}\n" \
               f"Chosen Figure Steps: {steps_count}\n" \
               f"Pawn reached border: {self.pawn_reached_border}\n" \
               f"Check: {self.check}\n" \
               f"Checkmate: {self.checkmate}\n"
               # f"{self.field}\n"
        return info

    def start(self):
        self.field = Field(self)
        self.field.set_figures()
        self.player_white = Player(self, True)
        self.player_black = Player(self, False)
        self.current_player = self.player_white

    def set_move_to_history(self, move):
        self.moves_history.append(move)
        self.last_move = move

    def get_last_move(self):
        return self.last_move

    def is_check(self):
        cells_list = self.field.cells_list
        for i in range(8):
            for j in range(8):
                if cells_list[i][j].figure:
                    if isinstance(cells_list[i][j].figure, King) and \
                       cells_list[i][j].figure.is_white == self.current_player.is_white and \
                       cells_list[i][j].is_under_attack(self.current_player.is_white):
                        return True
        return False

    def is_mate(self):
        cells_list = self.field.cells_list
        for i in range(8):
            for j in range(8):
                if cells_list[i][j].figure:
                    if cells_list[i][j].figure.is_white == self.current_player.is_white:
                        self.chosen_figure = cells_list[i][j].figure
                        if cells_list[i][j].figure.get_available_cells():
                            self.chosen_figure = None
                            return False
        self.chosen_figure = None
        return True

    def new_turn(self):
        self.chosen_figure = None
        if self.current_player.is_white:
            self.current_player = self.player_black
        else:
            self.current_player = self.player_white

        self.check = self.is_check()
        mate = self.is_mate()
        self.checkmate = True if self.check and mate else False
        self.stalemate = True if not self.check and mate else False

    def pawn_transformation(self, figure=Queen):
        figure_class = Queen
        if isinstance(figure, Figure):
            figure_class = figure
        else:
            if figure == "queen": figure_class = Queen
            if figure == "castle": figure_class = Castle
            if figure == "bishop": figure_class = Bishop
            if figure == "knight": figure_class = Knight
        self.pawn_to_figure_class = figure_class

    # Trying to choose figure by checking [x, y] of the chosen cell
    def choose_figure(self, x, y):
        # Block choosing when Pawn reached border
        if self.pawn_reached_border:
            figure_instead_of_pawn = self.pawn_to_figure_class(self.chosen_figure.x,
                                                               self.chosen_figure.y,
                                                               self.chosen_figure.is_white, self)
            figure_instead_of_pawn.steps_count = self.chosen_figure.steps_count
            self.field.cells_list[self.chosen_figure.x][self.chosen_figure.y].figure = figure_instead_of_pawn
            self.pawn_reached_border = False

            # New turn
            self.new_turn()

        else:
            chosen_cell = self.field.cells_list[x][y]
            # Содержит ли ячейка фигуру
            if chosen_cell.figure:
                # Является ли она фигурой вашего цвета
                if chosen_cell.figure.is_white == self.current_player.is_white:
                    self.chosen_figure = chosen_cell.figure
                    return True
            self.chosen_figure = None
            return False

    # Trying to move to coordinates [x, y]
    def move(self, x, y):
        if self.chosen_figure:
            available_cells = self.chosen_figure.get_available_cells()
            if [x, y] in available_cells:
                move_history_record = (str(self.chosen_figure), "white" if self.chosen_figure.is_white else "black",
                                       [self.chosen_figure.x, self.chosen_figure.y], [x, y])

                # Move actions:
                # Check if any figure is taken and give scores to the Current Player
                if self.field.cells_list[x][y].figure:
                    self.current_player.add_score(self.field.cells_list[x][y].figure.name)

                # Simple move to available cell
                self.field.cells_list[x][y].set_figure(self.chosen_figure)

                if isinstance(self.chosen_figure, Pawn):
                    # Check for "En Passant" attack (взятие пешкой на проходе)
                    last_move = self.get_last_move()
                    # Последний ход был пешкой (1)
                    # через одну клетку (2)
                    # до линии, на которой находится текущая пешка (3)
                    # рядом со столбцом текущей пешки (4)
                    # текущий ход происходит на столбце предыдущего хода (5)
                    if last_move:
                        if last_move[0] == "pawn" and \
                                abs(last_move[3][0] - last_move[2][0]) == 2 and \
                                last_move[3][0] == self.chosen_figure.x and \
                                abs(last_move[3][1] - self.chosen_figure.y) == 1 and last_move[3][1] == y:
                            # Очко Гриффиндору за пешку
                            self.current_player.add_score("pawn")
                            # Delete En Passant attacked pawn
                            self.field.cells_list[last_move[3][0]][last_move[3][1]].figure = None

                    # Check for Pawn reached the border
                    if x == 0 or x == 7:
                        self.pawn_reached_border = True
                    else:
                        self.pawn_reached_border = False

                # Check for castling move
                if isinstance(self.chosen_figure, King) and abs(self.chosen_figure.y - y) == 2:
                    y_castle, y_adder = (7, 1) if y > self.chosen_figure.y else (0, -1)
                    castle = self.field.cells_list[self.chosen_figure.x][y_castle].figure
                    # Place the Castle nearby the King
                    self.field.cells_list[self.chosen_figure.x][self.chosen_figure.y + y_adder].set_figure(castle)
                    # Clear the previous Castle cell
                    self.field.cells_list[self.chosen_figure.x][y_castle].figure = None
                    # Change the Castle coordinates
                    castle.x = self.chosen_figure.x
                    castle.y = self.chosen_figure.y + y_adder

                # Delete actions:
                self.field.cells_list[self.chosen_figure.x][self.chosen_figure.y].figure = None

                # Change new coordinates
                self.chosen_figure.x = x
                self.chosen_figure.y = y

                # Add step count to the figure
                self.chosen_figure.steps_count += 1

                # New turn
                if not self.pawn_reached_border:
                    self.new_turn()

                # Save movement to history
                self.moves_count += 1
                self.set_move_to_history(move_history_record)
                return True
            else:
                self.choose_figure(x, y)
        return False


if __name__ == "__main__":
    new_game = Game()
    new_game.start()
    new_game.choose_figure(6, 2)
    new_game.move(4, 0)
    print(new_game.field)
