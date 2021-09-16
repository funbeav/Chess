import operator
from copy import deepcopy

ops = {
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq
}


# Фигура
class Figure:
    def __init__(self, x, y, is_white, game):
        self.x = x
        self.y = y
        self.is_white = is_white
        self.game = game
        self.name = None
        self.steps_count = 0

    def __str__(self):
        return self.name

    def get_fullname(self):
        color = "white" if self.is_white else "black"
        return f"{self.name}_{color}"

    def get_available_cells(self):
        return []

    def get_steps_to_prevent_check(self, old_cells):
        available_cells = []
        # Если произошёл Шах, доступны лишь те ходы, которые избавят от Шаха
        for old_cell in old_cells:
            # Создаём копию игры, в которой проверяем, "спасут" ли ходы от шаха
            var_game = deepcopy(self.game)
            # Перенос фигуры в тестовой игре
            var_game.field.cells_list[old_cell[0]][old_cell[1]].figure = var_game.chosen_figure
            var_game.field.cells_list[var_game.chosen_figure.x][var_game.chosen_figure.y].figure = None
            var_game.chosen_figure.x = old_cell[0]
            var_game.chosen_figure.y = old_cell[1]
            # Привёл ли он к шаху
            if not var_game.is_check():
                available_cells.append(old_cell)
            del var_game
        return available_cells

    # Универсальный поиск доступных ходов / атак для фигур с цикличным проходом клеток (Ладья, Слон, Ферзь)
    # Принимает на вход список (list) из последовательностей (tuple) инструкций, как именно организовывать цикл
    # [(переменная_x, сравнение_x_со_следующим_значением, с_чем_сравнить_х,
    # переменная_y, сравнение_y_со_следующим_значением, с_чем_сравнить_y,
    # сумматор_насколько_менять_x_на_каждой_итерации, сумматор_насколько_менять_y_на_каждой_итерации), (...), ...]
    def get_available_cells_by_side_operations(self, side_operations):
        available_cells = []
        cells_list = self.game.field.cells_list

        # Проход каждой инструкции
        for operation in side_operations:
            x_curr = operation[0]
            x_op = ops[operation[1]]
            x_till = operation[2]
            y_curr = operation[3]
            y_op = ops[operation[4]]
            y_till = operation[5]
            x_adder = operation[6]
            y_adder = operation[7]

            # Двигаемся по ячейкам в зависимости от инструкции operation
            while x_op(x_curr, x_till) and y_op(y_curr, y_till):
                x_curr += x_adder
                y_curr += y_adder
                # Пустая ячейка - доступный ход
                if not cells_list[x_curr][y_curr].figure:
                    available_cells.append([x_curr, y_curr])
                # В ячейке находится вражеская фигура
                elif cells_list[x_curr][y_curr].figure.is_white != self.is_white:
                    available_cells.append([x_curr, y_curr])
                    break
                # Союзная фигура
                elif cells_list[x_curr][y_curr].figure.is_white == self.is_white:
                    break
                else:
                    break
        # Исключить ходы, ведушие к мату
        if self.game.current_player.is_white == self.is_white:
            available_cells = self.get_steps_to_prevent_check(available_cells)
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
        available_cells.extend(self.get_steps())
        available_cells.extend(self.get_attacks())
        # Исключить ходы, ведушие к мату
        if self.game.current_player.is_white == self.is_white:
            available_cells = self.get_steps_to_prevent_check(available_cells)
        return available_cells

    # Доступные шаги
    def get_steps(self):
        available_cells = []
        cells_list = self.game.field.cells_list
        adder = -1 if self.is_white else 1

        # Нет ли фигуры в следующей ячейке
        if 0 <= self.x + adder < 8:
            if not cells_list[self.x + adder][self.y].figure:
                available_cells.append([self.x + adder, self.y])
                # Нет ли фигуры в ячейке дальше
                if 0 <= self.x + 2 * adder < 8:
                    if not cells_list[self.x + 2 * adder][self.y].figure and \
                            ((self.x == 6 and self.is_white) or (self.x == 1 and not self.is_white)):
                        available_cells.append([self.x + 2 * adder, self.y])
        return available_cells

    # Доступные атаки
    def get_attacks(self):
        available_cells = []
        cells_list = self.game.field.cells_list
        adder = -1 if self.is_white else 1

        # Доступные столбцы для атаки
        side_y_s = [self.y + 1, self.y - 1]
        if self.y == 0:
            side_y_s = [1]
        if self.y == 7:
            side_y_s = [6]

        for side_y in side_y_s:
            if 0 <= self.x + adder < 8:
                # Если сбоку от текущ. пешки фигура другого цвета - она доступна для атаки
                if cells_list[self.x + adder][side_y].figure:
                    if cells_list[self.x + adder][side_y].figure.is_white != self.is_white:
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
        return available_cells


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
        available_cells = self.get_available_cells_by_side_operations(side_operations)
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
        available_cells = self.get_available_cells_by_side_operations(side_operations)
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
        cells_list = self.game.field.cells_list
        x, y = (self.x, self.y)
        # (x_adder, y_adder)
        side_operations = [(-1, 2), (-1, -2), (-2, 1), (-2, -1), (1, 2), (1, -2), (2, 1), (2, -1)]
        for operation in side_operations:
            x_adder = operation[0]
            y_adder = operation[1]
            x += x_adder
            y += y_adder
            if 0 <= x < 8 and 0 <= y < 8:
                # Ячейка свободна
                if not cells_list[x][y].figure:
                    available_cells.append([x, y])
                # Вражеская фигура
                if cells_list[x][y].figure:
                    if cells_list[x][y].figure.is_white != self.is_white:
                        available_cells.append([x, y])
            x, y = (self.x, self.y)
        # Исключить ходы, ведушие к мату
        if self.game.current_player.is_white == self.is_white:
            available_cells = self.get_steps_to_prevent_check(available_cells)
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
        available_cells = self.get_available_cells_by_side_operations(side_operations)
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
        cells_list = self.game.field.cells_list
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if 0 <= i < 8 and 0 <= j < 8:
                    if not cells_list[i][j].figure:
                        available_cells.append([i, j])
                    if cells_list[i][j].figure:
                        # Вражеская фигура
                        if cells_list[i][j].figure.is_white != self.is_white:
                            available_cells.append([i, j])

        if self.game.current_player.is_white == self.is_white:
            # Рокировка (castling)
            # Король не ходил ни разу, король не находится под шахом
            if self.steps_count == 0 and not cells_list[self.x][self.y].is_under_attack(self.is_white):
                # (y_ладьи, тип_сравнение_с_y_короля, множитель_сумматор)
                castle_operations = [
                    (7, "<", 1),     # Short (O-O)
                    (0, ">", -1)     # Long (O-O-O)
                ]

                for operation in castle_operations:
                    y_castle = operation[0]
                    op_func = ops[operation[1]]
                    y_adder = operation[2]

                    # На краю доски присутствует Ладья
                    if cells_list[self.x][y_castle].figure and isinstance(cells_list[self.x][y_castle].figure, Castle):
                        castle = cells_list[self.x][y_castle].figure
                        # Ладья - того же цвета, что и король; ладья не ходила ни разу
                        if castle.is_white == self.is_white and castle.steps_count == 0:
                            # Между ними отсуствуют фигуры
                            is_castling = True
                            y = self.y
                            while op_func(y, y_castle - y_adder):
                                y += y_adder
                                # Если на пути между Ладьёй и Королём фигуры, либо клетка под боем - запрет рокировки
                                if cells_list[self.x][y].figure or \
                                   cells_list[self.x][y].is_under_attack(self.is_white):
                                    is_castling = False
                                    break
                            if is_castling:
                                available_cells.append([self.x, self.y + 2 * y_adder])
        # Исключить ходы, ведушие к мату
        if self.game.current_player.is_white == self.is_white:
            available_cells = self.get_steps_to_prevent_check(available_cells)
        return available_cells

