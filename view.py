from tkinter import *
from ChessGame import *

import PIL.Image
import PIL.ImageTk
import PIL.ImageDraw


FIELD_SIZE = 640
CLR_BLACK = "#b58863"
CLR_WHITE = "#f0d9b5"


class Chessboard:
    def __init__(self, game, canvas):
        available_cells = []
        if game.chosen_figure:
            available_cells = game.chosen_figure.get_available_cells()

        step_size = int(FIELD_SIZE / 8)
        current_color = CLR_WHITE
        for i in range(8):
            for j in range(8):
                # Отрисовка клеток
                canvas.create_rectangle(j * step_size, i * step_size,
                                        j * step_size + step_size, i * step_size + step_size,
                                        fill=current_color, width=0)

                # Отрисовка фигур
                if game.field.cells_list[i][j].figure:
                    figure = game.field.cells_list[i][j].figure
                    img = PIL.Image.open(f"Figures/style0/{figure.get_fullname()}.png")
                    img = img.resize((step_size, step_size), PIL.Image.ANTIALIAS)
                    photo = PIL.ImageTk.PhotoImage(img)
                    images.append(photo)
                    canvas.create_image(j * step_size + step_size / 2 - 1, i * step_size + step_size / 2, image=photo)

                # Отображение доступных ходов
                if game.chosen_figure:
                    if [i, j] in available_cells:
                        # "Особое" отображение взятия в проходе для пешек
                        if isinstance(game.chosen_figure, Pawn):
                            if abs(j - game.chosen_figure.y) == 1:
                                create_oval(j * step_size, i * step_size,
                                            j * step_size + step_size, i * step_size + step_size,
                                            outline_fill="black", alpha=.1, width=8)
                            else:
                                create_oval(j * step_size + step_size * 0.3, i * step_size + step_size * 0.3,
                                            j * step_size + step_size * 0.7, i * step_size + step_size * 0.7,
                                            fill="black", alpha=.1)
                        # Остальные фигуры, кроме пешек
                        else:
                            if game.field.cells_list[i][j].figure:
                                create_oval(j * step_size, i * step_size,
                                            j * step_size + step_size, i * step_size + step_size,
                                            outline_fill="black", alpha=.1, width=8)
                            else:
                                create_oval(j * step_size + step_size * 0.3, i * step_size + step_size * 0.3,
                                            j * step_size + step_size * 0.7, i * step_size + step_size * 0.7,
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
    # print(new_game)
    Chessboard(new_game, canvas_field)


def create_oval(*args, **kwargs):
    if "alpha" in kwargs:
        if "outline_fill" in kwargs:
            outline_fill = root.winfo_rgb(kwargs.pop("outline_fill")) \
                   + (int(kwargs.pop("alpha") * 255),)
            width = kwargs.pop("width") if "width" in kwargs else None
            image = PIL.Image.new("RGBA", (FIELD_SIZE, FIELD_SIZE))
            PIL.ImageDraw.Draw(image).ellipse(args, fill=None, outline=outline_fill, width=width)
            images.append(PIL.ImageTk.PhotoImage(image))  # prevent the Image from being garbage-collected
            return canvas_field.create_image(0, 0, image=images[-1], anchor="nw")  # insert the Image to the 0, 0 coords
        if "fill" in kwargs:
            # Get and process the input data
            fill = root.winfo_rgb(kwargs.pop("fill"))\
                   + (int(kwargs.pop("alpha") * 255),)
            image = PIL.Image.new("RGBA", (FIELD_SIZE, FIELD_SIZE))
            PIL.ImageDraw.Draw(image).ellipse(args, fill=fill, outline=None)
            images.append(PIL.ImageTk.PhotoImage(image))  # prevent the Image from being garbage-collected
            return canvas_field.create_image(0, 0, image=images[-1], anchor="nw")  # insert the Image to the 0, 0 coords
        raise ValueError("fill color must be specified!")
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
