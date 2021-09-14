from Figures import *


# Ячейка поля, (не/) содержит фигуру
class Cell:
    def __init__(self, x, y, figure, game):
        self.x = x
        self.y = y
        self.game = game
        self.figure = figure

    def __str__(self):
        if not self.figure:
            return '0'
        else:
            return str(self.figure)

    def set_figure(self, figure):
        self.figure = figure


# Поле ячеек, содержит список ячеек
class Field:
    def __init__(self, game):
        self.game = game
        self.cells_list = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(Cell(i, j, None, game))
            self.cells_list.append(row)

    def __str__(self):
        field = ''
        for i in range(8):
            for j in range(8):
                field += str(self.cells_list[i][j]) + "\t"
            field += "\n"
        return field

    def set_figures(self):
        # White
        #   Pawns
        for j in range(8):
            self.cells_list[6][j].set_figure(Pawn(6, j, True, self.game))
        # Castles
        self.cells_list[7][0].set_figure(Castle(7, 0, True, self.game))
        self.cells_list[7][7].set_figure(Castle(7, 7, True, self.game))

        # Black
        #   Pawns
        for j in range(8):
            self.cells_list[1][j].set_figure(Pawn(1, j, False, self.game))
        # Castles
        self.cells_list[0][0].set_figure(Castle(0, 0, False, self.game))
        self.cells_list[0][7].set_figure(Castle(0, 7, False, self.game))

        self.cells_list[4][1].set_figure(Pawn(4, 1, False, self.game))
