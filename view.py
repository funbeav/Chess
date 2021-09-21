from tkinter import *
from ChessGame import *
from math import sin, cos

import PIL.Image
import PIL.ImageTk
import PIL.ImageDraw

FIELD_SIZE = 640
STEP_SIZE = int(FIELD_SIZE / 8)
CLR_BLACK = "#b58863"
CLR_WHITE = "#f0d9b5"
CLR_ACTIVE = "#ff7e00"


is_label_shown = False
FRAMES = 0


class Chessboard:
    def __init__(self, game, canvas):
        global images
        images.clear()
        canvas.delete("cell")
        canvas.delete("figure")
        canvas.delete("temp")
        canvas.delete("pawn_menu")

        available_cells = []
        if game.chosen_figure:
            available_cells = game.chosen_figure.get_available_cells()
        current_color = CLR_WHITE
        for i in range(8):
            for j in range(8):
                # Отрисовка клеток
                canvas.create_rectangle(j * STEP_SIZE, i * STEP_SIZE,
                                        j * STEP_SIZE + STEP_SIZE, i * STEP_SIZE + STEP_SIZE,
                                        fill=current_color, width=0, tags="cell")

                # Отрисовка последнего хода
                if game.last_move:
                    cell_from = [game.last_move[2][0], game.last_move[2][1]]
                    cell_to = [game.last_move[3][0], game.last_move[3][1]]
                    if [i, j] == cell_from or [i, j] == cell_to:
                        create_rectangle(canvas,
                                         j * STEP_SIZE, i * STEP_SIZE,
                                         j * STEP_SIZE + STEP_SIZE, i * STEP_SIZE + STEP_SIZE,
                                         fill=CLR_ACTIVE, alpha=.15, width=0)

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
                                  j * STEP_SIZE + STEP_SIZE / 2 - 1, figure)

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


frames = []
frame_count = 0


def show_label(label, is_white):
    global frame_count, frames
    if frame_count == 0:
        create_rectangle(canvas_field, 0, 0, FIELD_SIZE, FIELD_SIZE, fill="black", alpha=.3, tags="temp")
    if frame_count < 10:
        frame_count += 1
        canvas_field.delete("label")

        if frames:
            frames.pop()
        width = int(FIELD_SIZE * 1.2 - frame_count * 50)
        width = FIELD_SIZE if width < FIELD_SIZE else width

        filename = label + "_black" if is_white else label + "_white"
        img = PIL.Image.open(f"Labels/{filename}.png")
        img = img.resize((width, width), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(img)
        canvas_field.create_image(FIELD_SIZE / 2, FIELD_SIZE / 2, image=photo, tags="label")
        frames.append(photo)

        canvas_field.after(10, lambda: show_label(label, is_white))
    else:
        if label == "check":
            frames.clear()
            Chessboard(new_game, canvas_field)
        frame_count = 0


def callback(event):
    global is_label_shown
    x = int(event.y / FIELD_SIZE * 8)
    y = int(event.x / FIELD_SIZE * 8)

    if not new_game.checkmate:
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
        if new_game.check and not is_label_shown:
            if new_game.checkmate:
                show_label("checkmate", new_game.current_player.is_white)
            else:
                show_label("check", new_game.current_player.is_white)
            is_label_shown = True
        if not new_game.check:
            is_label_shown = False


# Возвращает прозрачный круг / окружность
def create_oval(*args, **kwargs):
    global images
    if "alpha" in kwargs:
        what_to_fill = [None, None]
        if "fill" in kwargs:
            what_to_fill[0] = "fill"
        if "outline_fill" in kwargs:
            what_to_fill[1] = "outline_fill"

        to_fill = what_to_fill[0] if what_to_fill[0] else what_to_fill[1]
        fill = root.winfo_rgb(kwargs.pop(to_fill)) + (int(kwargs.pop("alpha") * 255),)
        width = kwargs.pop("width") if "width" in kwargs else None
        image = PIL.Image.new("RGBA", (FIELD_SIZE, FIELD_SIZE))
        PIL.ImageDraw.Draw(image).ellipse(args, width=width,
                                          fill=fill if what_to_fill[0] else None,
                                          outline=fill if what_to_fill[1] else None)
        image = PIL.ImageTk.PhotoImage(image)
        images.append(image)  # prevent the Image from being garbage-collected
        return canvas_field.create_image(0, 0, image=image, anchor="nw", tags="temp")
    return canvas_field.create_oval(*args, **kwargs)


# Отрисовка фигуры
def create_figure(canvas, i, j, figure, is_white=True, tags="temp"):
    if isinstance(figure, Figure):
        figure_name = figure.get_fullname()
    else:
        figure_name = figure + "_" + "white" if is_white else figure + "_" + "black"
    img = PIL.Image.open(f"Figures/style0/{figure_name}.png")
    img = img.resize((STEP_SIZE, STEP_SIZE), PIL.Image.ANTIALIAS)
    photo = PIL.ImageTk.PhotoImage(img)
    images.append(photo)
    canvas.create_image(j, i, image=photo, tags=tags)


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
new_game.start()

root = Tk()
canvas_field = Canvas(root, width=FIELD_SIZE, height=FIELD_SIZE, bg='white', borderwidth=0)
canvas_field.bind("<Button-1>", callback)
canvas_field.pack()

images = []
Chessboard(new_game, canvas_field)

root.mainloop()
