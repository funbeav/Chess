

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
        available_cells = []
        cells_list = self.game.field.cells_list
        x, y = (self.x, self.y)

        # Ячейки справа
        while y < 7:
            y += 1
            if not cells_list[x][y].figure:
                available_cells.append([x, y])
            elif cells_list[x][y].figure.is_white != self.is_white:
                available_cells.append([x, y])
                x, y = (self.x, self.y)
                break
            else:
                x, y = (self.x, self.y)
                break
        x, y = (self.x, self.y)

        # Ячейки слева
        while y > 0:
            y -= 1
            if not cells_list[x][y].figure:
                available_cells.append([x, y])
            elif cells_list[x][y].figure.is_white != self.is_white:
                available_cells.append([x, y])
                x, y = (self.x, self.y)
                break
            else:
                x, y = (self.x, self.y)
                break
        x, y = (self.x, self.y)

        # Ячейки сверху
        while x > 0:
            x -= 1
            if not cells_list[x][y].figure:
                available_cells.append([x, y])
            elif cells_list[x][y].figure.is_white != self.is_white:
                available_cells.append([x, y])
                x, y = (self.x, self.y)
                break
            else:
                x, y = (self.x, self.y)
                break
        x, y = (self.x, self.y)

        # Ячейки сверху
        while x < 7:
            x += 1
            if not cells_list[x][y].figure:
                available_cells.append([x, y])
            elif cells_list[x][y].figure.is_white != self.is_white:
                available_cells.append([x, y])
                x, y = (self.x, self.y)
                break
            else:
                x, y = (self.x, self.y)
                break
        x, y = (self.x, self.y)

        return available_cells