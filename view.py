from tkinter import *
from ChessGame import *

import PIL.Image
import PIL.ImageTk
import PIL.ImageDraw

FIELD_SIZE = 640
STEP_SIZE = int(FIELD_SIZE / 8)
CLR_BLACK = "#b58863"
CLR_WHITE = "#f0d9b5"


class Chessboard:
    def __init__(self, game, canvas):
        global images
        images = []
        canvas.delete("cell")
        canvas.delete("figure")
        canvas.delete("temp")
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

                # Отрисовка фигур
                if game.field.cells_list[i][j].figure:
                    figure = game.field.cells_list[i][j].figure
                    img = PIL.Image.open(f"Figures/style0/{figure.get_fullname()}.png")
                    img = img.resize((STEP_SIZE, STEP_SIZE), PIL.Image.ANTIALIAS)
                    photo = PIL.ImageTk.PhotoImage(img)
                    images.append(photo)
                    canvas.create_image(j * STEP_SIZE + STEP_SIZE / 2 - 1, i * STEP_SIZE + STEP_SIZE / 2,
                                        image=photo, tags="figure")

                # Отображение доступных ходов
                if game.chosen_figure:
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

                current_color = CLR_WHITE if current_color == CLR_BLACK else CLR_BLACK
            current_color = CLR_WHITE if current_color == CLR_BLACK else CLR_BLACK
        canvas.pack()


def callback(event):
    x = int(event.y / FIELD_SIZE * 8)
    y = int(event.x / FIELD_SIZE * 8)
    if new_game.chosen_figure:
        new_game.move(x, y)
    else:
        new_game.choose_figure(x, y)
    print(new_game)
    Chessboard(new_game, canvas_field)


# Возвращает прозрачный круг / окружность
def create_oval(*args, **kwargs):
    global images
    if "alpha" in kwargs:
        what_to_fill = [None, None]
        if "fill" in kwargs:
            what_to_fill[0] = "fill"
        if "outline_fill" in kwargs:
            what_to_fill[1] = "outline_fill"

        fill = root.winfo_rgb(kwargs.pop(what_to_fill[0] if what_to_fill[0] else what_to_fill[1])) + \
               (int(kwargs.pop("alpha") * 255),)
        width = kwargs.pop("width") if "width" in kwargs else None
        image = PIL.Image.new("RGBA", (FIELD_SIZE, FIELD_SIZE))
        PIL.ImageDraw.Draw(image).ellipse(args, width=width,
                                          fill=fill if what_to_fill[0] else None,
                                          outline=fill if what_to_fill[1] else None)
        image = PIL.ImageTk.PhotoImage(image)
        images.append(image)  # prevent the Image from being garbage-collected
        return canvas_field.create_image(0, 0, image=image, anchor="nw", tags="temp")
    return canvas_field.create_oval(*args, **kwargs)


new_game = Game()
new_game.start()

root = Tk()
canvas_field = Canvas(root, width=FIELD_SIZE, height=FIELD_SIZE, bg='white', borderwidth=0)
canvas_field.bind("<Button-1>", callback)
canvas_field.pack()

images = []
Chessboard(new_game, canvas_field)

root.mainloop()