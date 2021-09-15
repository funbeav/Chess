import operator


# Фигура
class Figure:
    def __init__(self, x, y, is_white, game):
        self.x = x
        self.y = y
        self.is_white = is_white
        self.game = game
        self.name = None

    def __str__(self):
        return self.name

    def get_fullname(self):
        color = "white" if self.is_white else "black"
        return f"{self.name}_{color}"

    def get_available_cells(self):
        pass

    def get_available_cells_by_side_operations(self, side_operations):
        available_cells = []
        ops = {
            ">": operator.gt,
            "<": operator.lt,
            "==": operator.eq
        }
        cells_list = self.game.field.cells_list
        for operation in side_operations:
            x_curr = operation[0]
            x_op = ops[operation[1]]
            x_till = operation[2]
            y_curr = operation[3]
            y_op = ops[operation[4]]
            y_till = operation[5]
            x_adder = operation[6]
            y_adder = operation[7]
            while x_op(x_curr, x_till) and y_op(y_curr, y_till):
                x_curr += x_adder
                y_curr += y_adder
                if not cells_list[x_curr][y_curr].figure:
                    available_cells.append([x_curr, y_curr])
                elif cells_list[x_curr][y_curr].figure.is_white != self.is_white:
                    available_cells.append([x_curr, y_curr])
                    break
                else:
                    break
        return available_cells


# Пешка
class Pawn(Figure):
    def __init__(self, x, y, is_white, game):
        super().__init__(x, y, is_white, game)
        self.name = "pawn"

    def __str__(self):
        return self.name

    # Доступные ячейки для перемещения
    def get_available_cells(self):
        available_cells = []
        # Определяет, вперёд или назад двигаться
        adder = 0
        cells_list = self.game.field.cells_list
        if self.is_white:
            adder = -1
        else:
            adder = 1
        self.get_steps(cells_list, adder, available_cells)
        self.get_attacks(cells_list, adder, available_cells)
        return available_cells

    # Доступные шаги
    def get_steps(self, cells_list, adder, available_cells):
        # Нет ли фигуры в следующей ячейке
        if 0 <= self.x + adder < 8:
            if not cells_list[self.x + adder][self.y].figure:
                available_cells.append([self.x + adder, self.y])
                # Нет ли фигуры в ячейке дальше
                if 0 <= self.x + 2 * adder < 8:
                    if not cells_list[self.x + 2 * adder][self.y].figure and \
                            ((self.x == 6 and self.is_white) or (self.x == 1 and not self.is_white)):
                        available_cells.append([self.x + 2 * adder, self.y])

    # Доступные атаки
    def get_attacks(self, cells_list, adder, available_cells):
        side_y_s = [self.y + 1, self.y - 1]
        if self.y == 0:
            side_y_s = [1]
        if self.y == 7:
            side_y_s = [6]

        for side_y in side_y_s:
            if 0 <= self.x + adder < 8:
                if cells_list[self.x + adder][side_y].figure:
                    if cells_list[self.x + adder][side_y].figure.is_white != self.game.current_player.is_white:
                        available_cells.append([self.x + adder, side_y])

        # En Passant attack (взятие на проходе)
        last_move = self.game.get_last_move()
        # Последний ход был пешкой (1)
        # через одну клетку (2)
        # до линии, на которой находится текущая пешка (3)
        # рядом со столбцом текущей пешки (4)
        if last_move:
            if last_move[0] == "pawn" and abs(last_move[3][0] - last_move[2][0]) == 2 and \
                    last_move[3][0] == self.x and abs(last_move[3][1] - self.y) == 1:
                available_cells.append([self.x + adder, last_move[3][1]])


# Ладья
class Castle(Figure):
    def __init__(self, x, y, is_white, game):
        super().__init__(x, y, is_white, game)
        self.name = "castle"

    def __str__(self):
        return self.name

    def get_available_cells(self):
        side_operations = [
            (self.x, "==", self.x, self.y, "<", 7, 0, 1),  # Ячейки справа
            (self.x, "==", self.x, self.y, ">", 0, 0, -1),  # Ячейки слева
            (self.x, ">", 0, self.y, "==", self.y, -1, 0),  # Ячейки сверху
            (self.x, "<", 7, self.y, "==", self.y, 1, 0)  # Ячейки снизу
        ]
        available_cells = super().get_available_cells_by_side_operations(side_operations)
        return available_cells


# Слон
class Bishop(Figure):
    def __init__(self, x, y, is_white, game):
        super().__init__(x, y, is_white, game)
        self.name = "bishop"

    def __str__(self):
        return self.name

    def get_available_cells(self):
        side_operations = [
            (self.x, ">", 0, self.y, "<", 7, -1, 1),  # Справа сверху
            (self.x, "<", 7, self.y, "<", 7, 1, 1),  # Справа снизу
            (self.x, ">", 0, self.y, ">", 0, -1, -1),  # Слева сверху
            (self.x, "<", 7, self.y, ">", 0, 1, -1)  # Слева снизу
        ]
        available_cells = super().get_available_cells_by_side_operations(side_operations)
        return available_cells


# Конь
class Knight(Figure):
    def __init__(self, x, y, is_white, game):
        super().__init__(x, y, is_white, game)
        self.name = "knight"

    def __str__(self):
        return self.name

    def get_available_cells(self):
        available_cells = []
        return available_cells


# Ферзь
class Queen(Figure):
    def __init__(self, x, y, is_white, game):
        super().__init__(x, y, is_white, game)
        self.name = "queen"

    def __str__(self):
        return self.name

    def get_available_cells(self):
        side_operations = [
            (self.x, "==", self.x, self.y, "<", 7, 0, 1),  # Ячейки справа
            (self.x, "==", self.x, self.y, ">", 0, 0, -1),  # Ячейки слева
            (self.x, ">", 0, self.y, "==", self.y, -1, 0),  # Ячейки сверху
            (self.x, "<", 7, self.y, "==", self.y, 1, 0),  # Ячейки снизу
            (self.x, ">", 0, self.y, "<", 7, -1, 1),  # Справа сверху
            (self.x, "<", 7, self.y, "<", 7, 1, 1),  # Справа снизу
            (self.x, ">", 0, self.y, ">", 0, -1, -1),  # Слева сверху
            (self.x, "<", 7, self.y, ">", 0, 1, -1)  # Слева снизу
        ]
        available_cells = super().get_available_cells_by_side_operations(side_operations)
        return available_cells


# Король
class King(Figure):
    def __init__(self, x, y, is_white, game):
        super().__init__(x, y, is_white, game)
        self.name = "king"

    def __str__(self):
        return self.name

    def get_available_cells(self):
        available_cells = []
        return available_cells
