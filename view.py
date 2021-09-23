from tkinter import *
from ChessGame import *
from math import sin, cos

import PIL.Image
import PIL.ImageTk
import PIL.ImageDraw
import PIL.ImageOps

FIELD_SIZE = 640
STEP_SIZE = int(FIELD_SIZE / 8)
CLR_WHITE = "#f0d9b5"
CLR_BLACK = "#b58863"
CLR_ACTIVE = "#ff7e00"
CLR_CHECK = "red"
IMG_PATH = "images"
STYLE_NUM = 0

FRAMES = 0
images = []
is_menu_active = True
is_game_starts = False
is_settings_active = False
is_label_shown = False


class Menu:
    def __init__(self, canvas):
        global is_menu_active, is_game_starts, is_settings_active
        images.clear()
        canvas.delete("all")
        self.canvas = canvas

        current_color = CLR_WHITE
        for i in range(8):
            for j in range(8):
                # Отрисовка клеток
                canvas.create_rectangle(j * STEP_SIZE, i * STEP_SIZE,
                                        j * STEP_SIZE + STEP_SIZE, i * STEP_SIZE + STEP_SIZE,
                                        fill=current_color, width=0, tags="cell")
                current_color = CLR_WHITE if current_color == CLR_BLACK else CLR_BLACK
            current_color = CLR_WHITE if current_color == CLR_BLACK else CLR_BLACK
        create_rectangle(canvas, 0, 0, FIELD_SIZE, FIELD_SIZE, fill="black", alpha=.3, tags="temp")
        create_round_rectangle(canvas,
                               STEP_SIZE * 2 - STEP_SIZE * 0.05,
                               2.5 * STEP_SIZE - STEP_SIZE * 0.05,
                               FIELD_SIZE - STEP_SIZE * 2 + STEP_SIZE * 0.05,
                               FIELD_SIZE - 2.5 * STEP_SIZE + STEP_SIZE * 0.05,
                               50, 100, CLR_WHITE, tags="temp")
        # Menu
        if is_menu_active:
            self.create_label(FIELD_SIZE / 2, FIELD_SIZE / 2 - STEP_SIZE / 1.2, ("Labels/new_game", "menu"), resize=2)
            self.create_label(FIELD_SIZE / 2, FIELD_SIZE / 2, ("Labels/settings", "menu"), resize=2)
            self.create_label(FIELD_SIZE / 2, FIELD_SIZE / 2 + STEP_SIZE / 1.2, ("Labels/quit", "menu"), resize=2)

        # Settings
        if is_settings_active:
            self.canvas.delete("menu")
            active_clr = 'orange' if CLR_WHITE == "#f0d9b5" else 'black'
            self.create_label(FIELD_SIZE / 2 - STEP_SIZE * 1.2,
                              FIELD_SIZE / 2 - STEP_SIZE * 0.75,
                              ("Colors/f0d9b5_b58863", "settings"), bd=1, to_size=(80, 80), bd_fill=active_clr)
            active_clr = 'orange' if CLR_WHITE == "#eeeed2" else 'black'
            self.create_label(FIELD_SIZE / 2 - STEP_SIZE * 1.2,
                              FIELD_SIZE / 2 + STEP_SIZE * 0.75,
                              ("Colors/eeeed2_769656", "settings"), bd=1, to_size=(80, 80), bd_fill=active_clr)
            active_clr = 'orange' if STYLE_NUM == 0 else 'black'
            self.create_label(FIELD_SIZE / 2 + STEP_SIZE * 1.2,
                              FIELD_SIZE / 2 - STEP_SIZE * 0.75,
                              ("Figures/style0/queen_white", "settings"), bd=1, to_size=(80, 80), bd_fill=active_clr)
            active_clr = 'orange' if STYLE_NUM == 1 else 'black'
            self.create_label(FIELD_SIZE / 2 + STEP_SIZE * 1.2,
                              FIELD_SIZE / 2 + STEP_SIZE * 0.75,
                              ("Figures/style1/queen_white", "settings"), bd=1, to_size=(80, 80), bd_fill=active_clr)
            self.create_label(FIELD_SIZE / 2, FIELD_SIZE / 2, ("Labels/ok", "settings"), resize=2)

    def create_label(self, x, y, name, resize=1, to_size=None, bd=0, bd_fill='black'):
        img = PIL.Image.open(f"{IMG_PATH}/{name[0]}.png")
        width, height = img.size
        if to_size:
            img = img.resize((to_size[0], to_size[1]))
        else:
            img = img.resize((width // resize, height // resize))
        if bd:
            img = PIL.ImageOps.expand(img, border=1, fill=bd_fill)
        photo = PIL.ImageTk.PhotoImage(img)
        i = self.canvas.create_image(x, y, image=photo, tags=name)
        images.append(photo)


class Chessboard:
    def __init__(self, game, canvas):
        global images, is_menu_active, is_game_starts
        images.clear()
        canvas.delete("all")

        available_cells = []
        if game.chosen_figure:
            available_cells = game.chosen_figure.get_available_cells()
        current_color = CLR_WHITE

        letters = 'abcdefgh'
        for i in range(8):
            for j in range(8):
                # Отрисовка клеток
                canvas.create_rectangle(j * STEP_SIZE, i * STEP_SIZE,
                                        j * STEP_SIZE + STEP_SIZE, i * STEP_SIZE + STEP_SIZE,
                                        fill=current_color, width=0, tags="cell")
                # Нумерация
                if i == 7:
                    canvas.create_text(j * STEP_SIZE + STEP_SIZE * 9 / 10, i * STEP_SIZE + STEP_SIZE * 7 / 8,
                                       fill=CLR_BLACK if current_color == CLR_WHITE else CLR_WHITE,
                                       text=letters[j], font="Bahnschrift 10")
                if j == 0:
                    canvas.create_text(j * STEP_SIZE + STEP_SIZE * 1 / 10, i * STEP_SIZE + STEP_SIZE * 1 / 8,
                                       fill=CLR_BLACK if current_color == CLR_WHITE else CLR_WHITE,
                                       text=8 - i, font="Bahnschrift 10")

                # Отрисовка последнего хода
                if game.last_move:
                    cell_from = [game.last_move[2][0], game.last_move[2][1]]
                    cell_to = [game.last_move[3][0], game.last_move[3][1]]
                    if [i, j] == cell_from or [i, j] == cell_to:
                        create_rectangle(canvas,
                                         j * STEP_SIZE, i * STEP_SIZE,
                                         j * STEP_SIZE + STEP_SIZE, i * STEP_SIZE + STEP_SIZE,
                                         fill=CLR_ACTIVE, alpha=.15, width=0)

                # Отрисовка шаха королю
                if game.check:
                    if game.field.cells_list[i][j].figure:
                        figure = game.field.cells_list[i][j].figure
                        if isinstance(figure, King) and figure.is_white == game.current_player.is_white:
                            create_rectangle(canvas,
                                             j * STEP_SIZE, i * STEP_SIZE,
                                             j * STEP_SIZE + STEP_SIZE, i * STEP_SIZE + STEP_SIZE,
                                             fill=CLR_CHECK, alpha=.2, width=0)

                # В случае, если выбрана фигура
                if game.chosen_figure:
                    # Выделение выбранной фигуры
                    if [i, j] == [game.chosen_figure.x, game.chosen_figure.y]:
                        create_rectangle(canvas,
                                         j * STEP_SIZE, i * STEP_SIZE,
                                         j * STEP_SIZE + STEP_SIZE, i * STEP_SIZE + STEP_SIZE,
                                         fill=CLR_ACTIVE, alpha=.15, width=0)

                    # Отображение доступных ходов
                    if [i, j] in available_cells:
                        # "Особое" отображение взятия в проходе для пешек
                        if isinstance(game.chosen_figure, Pawn):
                            if abs(j - game.chosen_figure.y) == 1:
                                create_oval(j * STEP_SIZE, i * STEP_SIZE,
                                            j * STEP_SIZE + STEP_SIZE, i * STEP_SIZE + STEP_SIZE,
                                            outline_fill="black", alpha=.1, width=8)
                            else:
                                create_oval(j * STEP_SIZE + STEP_SIZE * 0.3, i * STEP_SIZE + STEP_SIZE * 0.3,
                                            j * STEP_SIZE + STEP_SIZE * 0.7, i * STEP_SIZE + STEP_SIZE * 0.7,
                                            fill="black", alpha=.1)
                        # Остальные фигуры, кроме пешек
                        else:
                            if game.field.cells_list[i][j].figure:
                                create_oval(j * STEP_SIZE, i * STEP_SIZE,
                                            j * STEP_SIZE + STEP_SIZE, i * STEP_SIZE + STEP_SIZE,
                                            outline_fill="black", alpha=.1, width=8)
                            else:
                                create_oval(j * STEP_SIZE + STEP_SIZE * 0.3, i * STEP_SIZE + STEP_SIZE * 0.3,
                                            j * STEP_SIZE + STEP_SIZE * 0.7, i * STEP_SIZE + STEP_SIZE * 0.7,
                                            fill="black", alpha=.1)

                # Отрисовка фигур
                if game.field.cells_list[i][j].figure:
                    figure = game.field.cells_list[i][j].figure
                    create_figure(canvas, i * STEP_SIZE + STEP_SIZE / 2,
                                  j * STEP_SIZE + STEP_SIZE / 2, figure)

                current_color = CLR_WHITE if current_color == CLR_BLACK else CLR_BLACK
            current_color = CLR_WHITE if current_color == CLR_BLACK else CLR_BLACK

        # Пешка добралась до границы поля
        if new_game.pawn_reached_border:
            create_rectangle(canvas, 0, 0, FIELD_SIZE, FIELD_SIZE, fill="black", alpha=.3, tags="pawn_menu")
            create_round_rectangle(canvas,
                                   FIELD_SIZE / 2 - STEP_SIZE / 2 - STEP_SIZE * 0.05, 2 * STEP_SIZE - STEP_SIZE * 0.05,
                                   FIELD_SIZE / 2 + STEP_SIZE / 2 + STEP_SIZE * 0.05,
                                   FIELD_SIZE - 2 * STEP_SIZE + STEP_SIZE * 0.05,
                                   20, 100, CLR_WHITE, tags="pawn_menu")
            create_figure(canvas, 2 * STEP_SIZE + STEP_SIZE / 2, FIELD_SIZE / 2,
                          "queen", new_game.current_player.is_white, tags="pawn_menu")
            create_figure(canvas, 3 * STEP_SIZE + STEP_SIZE / 2, FIELD_SIZE / 2,
                          "castle", new_game.current_player.is_white, tags="pawn_menu")
            create_figure(canvas, 4 * STEP_SIZE + STEP_SIZE / 2, FIELD_SIZE / 2,
                          "bishop", new_game.current_player.is_white, tags="pawn_menu")
            create_figure(canvas, 5 * STEP_SIZE + STEP_SIZE / 2, FIELD_SIZE / 2,
                          "knight", new_game.current_player.is_white, tags="pawn_menu")

            canvas.tag_raise("pawn_menu")

        canvas.pack()

    @staticmethod
    def get_figure_by_coordinates(x, y):
        if FIELD_SIZE / 2 - STEP_SIZE / 2 < x < FIELD_SIZE / 2 + STEP_SIZE / 2:
            if 2 * STEP_SIZE < y < 3 * STEP_SIZE:
                return "queen"
            if 3 * STEP_SIZE < y < 4 * STEP_SIZE:
                return "castle"
            if 4 * STEP_SIZE < y < 5 * STEP_SIZE:
                return "bishop"
            if 5 * STEP_SIZE < y < 6 * STEP_SIZE:
                return "knight"
        return None


class Label:
    def __init__(self):
        self.frames = []
        self.frame_count = 0

    def show_label(self, timer, label, is_white):
        global is_menu_active, is_game_starts
        # Отрисовка каждого кадра
        if self.frame_count < 10:
            self.frame_count += 1
            if self.frames:
                self.frames.pop()
            canvas_field.delete(f"label_{label}")

            width = int(FIELD_SIZE * 1.2 - self.frame_count * 20)
            width = FIELD_SIZE if width < FIELD_SIZE else width

            if label == "stalemate" or label == "draw":
                filename = label
            else:
                filename = label + "_black" if is_white else label + "_white"
            img = PIL.Image.open(f"{IMG_PATH}/Labels/{filename}.png")
            img = img.resize((width, width), PIL.Image.ANTIALIAS)
            photo = PIL.ImageTk.PhotoImage(img)
            canvas_field.create_image(FIELD_SIZE / 2, FIELD_SIZE / 2, image=photo, tags=f"label_{label}")
            self.frames.append(photo)

            canvas_field.after(timer, self.show_label, timer, label, is_white)
        # Все кадры отрисованы
        else:
            # tkinter очищает объекты изображений, если они не попадают в глабльный scope
            # Чтобы надпись не очищалась - занесём последний кадр в глобальный список images
            if label == "checkmate":
                images.append(self.frames[-1])
                canvas_field.after(timer, Label().show_label, timer, "win", is_white)
            if label == "win":
                images.append(self.frames[-1])
                is_game_starts = False
            if label == "stalemate":
                images.append(self.frames[-1])
                canvas_field.after(timer, Label().show_label, timer, "draw", is_white)
            if label == "draw":
                images.append(self.frames[-1])
                is_game_starts = False


# On Click event
def callback(event):
    global is_menu_active, is_game_starts, is_settings_active, new_game
    if is_menu_active:
        global CLR_ACTIVE, CLR_CHECK, CLR_BLACK, CLR_WHITE, STYLE_NUM
        item = canvas_field.find_closest(event.x, event.y)
        tags = canvas_field.itemcget(item, "tags")
        if "new_game" in tags:
            is_menu_active = False
            is_game_starts = True
            new_game = Game()
            new_game.start()
            Chessboard(new_game, canvas_field)
        if "settings" in tags:
            is_settings_active = True
            item = canvas_field.find_closest(event.x, event.y)
            tags = canvas_field.itemcget(item, "tags")
            if 'f0d9b5_b58863' in tags:
                CLR_WHITE = "#f0d9b5"
                CLR_BLACK = "#b58863"
            if 'eeeed2_769656' in tags:
                CLR_WHITE = "#eeeed2"
                CLR_BLACK = "#769656"

            if 'style0' in tags:
                STYLE_NUM = 0
            if 'style1' in tags:
                STYLE_NUM = 1

            if 'ok' in tags:
                is_settings_active = False
            Menu(canvas_field)
        if "quit" in tags:
            root.quit()

    if is_game_starts:
        global is_label_shown
        x = int(event.y / FIELD_SIZE * 8)
        y = int(event.x / FIELD_SIZE * 8)

        if not new_game.checkmate and not new_game.stalemate:
            if new_game.chosen_figure:
                if new_game.pawn_reached_border:
                    figure_str = Chessboard.get_figure_by_coordinates(event.x, event.y)
                    if figure_str:
                        new_game.pawn_transformation(figure_str)
                        new_game.choose_figure(x, y)
                else:
                    new_game.move(x, y)
            else:
                new_game.choose_figure(x, y)
            # print(new_game)
            Chessboard(new_game, canvas_field)

            # If Check / Mate
            if (new_game.checkmate or new_game.stalemate) and not is_label_shown:
                create_rectangle(canvas_field, 0, 0, FIELD_SIZE, FIELD_SIZE, fill="black", alpha=.3, tags="temp")
                if new_game.checkmate:
                    Label().show_label(10, "checkmate", new_game.current_player.is_white)
                elif new_game.stalemate:
                    Label().show_label(10, "stalemate", new_game.current_player.is_white)
                is_label_shown = True
            if not new_game.check:
                is_label_shown = False

    # Когда игра закончилась, активировать меню по нажатию, но не на варианты меню
    if not is_game_starts and (new_game.checkmate or new_game.stalemate):
        is_menu_active = True
        Menu(canvas_field)


# On mouse move event
def motion(event):
    x = int(event.y / FIELD_SIZE * 8)
    y = int(event.x / FIELD_SIZE * 8)
    item = canvas_field.find_closest(event.x, event.y)
    tags = canvas_field.itemcget(item, "tags")
    if "menu" in tags or "settings" in tags or "available_move" in tags:
        canvas_field.configure(cursor='hand2')
    elif "figure" in tags:
        if new_game.field.cells_list[x][y].figure.is_white == new_game.current_player.is_white:
            canvas_field.configure(cursor='hand2')
    else:
        canvas_field.configure(cursor='arrow')


# Возвращает прозрачный круг / окружность
def create_oval(*args, **kwargs):
    global images
    if "alpha" in kwargs:
        what_to_fill = [None, None]
        if "fill" in kwargs:
            what_to_fill[0] = "fill"
        if "outline_fill" in kwargs:
            what_to_fill[1] = "outline_fill"

        new_args = (0 + STEP_SIZE * 0.3,
                    args[1] - args[1] + STEP_SIZE * 0.3,
                    args[2] - args[0] + STEP_SIZE * 0.3,
                    args[3] - args[1] + STEP_SIZE * 0.3)

        to_fill = what_to_fill[0] if what_to_fill[0] else what_to_fill[1]
        fill = root.winfo_rgb(kwargs.pop(to_fill)) + (int(kwargs.pop("alpha") * 255),)
        width = kwargs.pop("width") if "width" in kwargs else None
        image = PIL.Image.new("RGBA", (STEP_SIZE * 2, STEP_SIZE * 2))
        PIL.ImageDraw.Draw(image).ellipse(new_args, width=width,
                                          fill=fill if what_to_fill[0] else None,
                                          outline=fill if what_to_fill[1] else None)
        image = PIL.ImageTk.PhotoImage(image)
        images.append(image)  # prevent the Image from being garbage-collected
        image_item = canvas_field.create_image(args[0] - STEP_SIZE * 0.3,
                                         args[1] - STEP_SIZE * 0.3,
                                         image=image, anchor="nw", tags="available_move")
        canvas_field.tag_raise(image_item)
        return image_item
    return canvas_field.create_oval(*args, **kwargs)


# Отрисовка фигуры
def create_figure(canvas, i, j, figure, is_white=True, tags="figure"):
    if isinstance(figure, Figure):
        figure_name = figure.get_fullname()
    else:
        figure_name = figure + "_" + "white" if is_white else figure + "_" + "black"
    img = PIL.Image.open(f"{IMG_PATH}/Figures/style{STYLE_NUM}/{figure_name}.png")
    img_size = int(STEP_SIZE * 0.95)
    img = img.resize((img_size, img_size), PIL.Image.ANTIALIAS)
    photo = PIL.ImageTk.PhotoImage(img)
    images.append(photo)
    canvas.create_image(j - 1, i, image=photo, tags=tags)


# Define a function to make the transparent rectangle
def create_rectangle(canvas, x, y, a, b, **options):
    if 'alpha' in options:
        # Calculate the alpha transparency for every color(RGB)
        alpha = int(options.pop('alpha') * 255)
        # Use the fill variable to fill the shape with transparent color
        fill = options.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = PIL.Image.new('RGBA', (a - x, b - y), fill)
        images.append(PIL.ImageTk.PhotoImage(image))
        canvas.create_image(x, y, image=images[-1], anchor='nw')
        return canvas.create_rectangle(x, y, a, b, **options)


def create_round_rectangle(c, x1, y1, x2, y2, feather, res=5, color='black', tags='temp'):
    points = []
    # top side
    points += [x1 + feather, y1,
               x2 - feather, y1]
    # top right corner
    for i in range(res):
        points += [x2 - feather + sin(i / res * 2) * feather,
                   y1 + feather - cos(i / res * 2) * feather]
    # right side
    points += [x2, y1 + feather,
               x2, y2 - feather]
    # bottom right corner
    for i in range(res):
        points += [x2 - feather + cos(i / res * 2) * feather,
                   y2 - feather + sin(i / res * 2) * feather]
    # bottom side
    points += [x2 - feather, y2,
               x1 + feather, y2]
    # bottom left corner
    for i in range(res):
        points += [x1 + feather - sin(i / res * 2) * feather,
                   y2 - feather + cos(i / res * 2) * feather]
    # left side
    points += [x1, y2 - feather,
               x1, y1 + feather]
    # top left corner
    for i in range(res):
        points += [x1 + feather - cos(i / res * 2) * feather,
                   y1 + feather - sin(i / res * 2) * feather]

    return c.create_polygon(points, fill=color, tags=tags)


new_game = Game()

root = Tk()
canvas_field = Canvas(root, width=FIELD_SIZE, height=FIELD_SIZE, bg='white', borderwidth=0)
canvas_field.bind("<Button-1>", callback)
canvas_field.bind('<Motion>', motion)
canvas_field.pack()

Menu(canvas_field)

root.mainloop()
