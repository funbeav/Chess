from Field import *
from Player import *


# Основной класс игры, содержит всю информацию о состоянии
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

    def __str__(self):
        info = f"Game #\n" \
               f"Move #{self.moves_count}\n" \
               f"Player White Score: {self.player_white.score}\n" \
               f"Player Black Score: {self.player_black.score}\n" \
               f"Moves History: {self.moves_history}\n" \
               f"Current Player: {self.current_player}\n" \
               f"Chosen Figure: {self.chosen_figure}\n"
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

    def choose_figure(self, x, y):
        chosen_cell = self.field.cells_list[x][y]
        # Содержит ли ячейка фигуру
        if chosen_cell.figure:
            # Является ли она фигурой вашего цвета
            if chosen_cell.figure.is_white == self.current_player.is_white:
                self.chosen_figure = chosen_cell.figure
                return True
        self.chosen_figure = None
        return False

    def move(self, x, y):
        if self.chosen_figure:
            available_cells = self.chosen_figure.get_available_cells()
            if [x, y] in available_cells:
                move_history_record = (str(self.chosen_figure), "white" if self.chosen_figure.is_white else "black",
                                       [self.chosen_figure.x, self.chosen_figure.y], [x, y])

                # Move actions:
                # Check if any figure is taken
                if self.field.cells_list[x][y].figure:
                    self.current_player.add_score(self.field.cells_list[x][y].figure.name)

                # Check for "En Passant" attack (взятие пешкой на проходе)
                if isinstance(self.chosen_figure, Pawn):
                    last_move = self.get_last_move()
                    # Последний ход был пешкой (1)
                    # через одну клетку (2)
                    # до линии, на которой находится текущая пешка (3)
                    # рядом со столбцом текущей пешки (4)
                    if last_move:
                        if last_move[0] == "pawn" and abs(last_move[3][0] - last_move[2][0]) == 2 and \
                                last_move[3][0] == self.chosen_figure.x and \
                                abs(last_move[3][1] - self.chosen_figure.y) == 1:
                            # Очко Гриффиндору за пешку
                            self.current_player.add_score("pawn")
                            # Delete En Passant attacked pawn
                            self.field.cells_list[last_move[3][0]][last_move[3][1]].figure = None

                # Simple move to available cell
                self.field.cells_list[x][y].set_figure(self.chosen_figure)

                # Delete actions:
                self.field.cells_list[self.chosen_figure.x][self.chosen_figure.y].figure = None
                # Change new coordinates
                self.chosen_figure.x = x
                self.chosen_figure.y = y

                # New turn
                self.moves_count += 1
                self.chosen_figure = None
                if self.current_player.is_white:
                    self.current_player = self.player_black
                else:
                    self.current_player = self.player_white

                # Save movement to history
                self.set_move_to_history(move_history_record)
            else:
                self.choose_figure(x, y)


if __name__ == "__main__":
    new_game = Game()
    new_game.start()
    new_game.choose_figure(6, 2)
    new_game.move(4, 0)
    print(new_game.field)
