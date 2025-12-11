import tkinter as tk

class chess_board:
    def __init__(self):
        self.window_maker = tk.Tk()
        self.canvas = tk.Canvas(height=1000, width=1000)
        self.SPACING = 125
        self.BOTTOM_Y_COORDINATE = 1000
        self.TOP_Y_COORDINATE = 0
        self.RIGHT_MOST_X_COORDINATE = 1000
        self.LEFT_MOST_X_COORDINATE = 0

    def create_board(self):
        self.window_maker.minsize(600, 600)
        self.canvas.config(bg="#582917")
     
    def lining(self):
        for i in range(8): 
            x = self.SPACING * i
            self.canvas.create_line(x, self.TOP_Y_COORDINATE, x, self.BOTTOM_Y_COORDINATE)

        for j in range(8): 
            y = self.SPACING * j
            self.canvas.create_line(self.LEFT_MOST_X_COORDINATE, y, self.RIGHT_MOST_X_COORDINATE, y)

    def numbers_and_alphabets(self):
        self.window_maker.title("Chess Engine")
        Y_COORDINATE_FOR_BOTTOM_ALPHABETS = self.BOTTOM_Y_COORDINATE - 10
        Y_COORDINATE_FOR_TOP_ALPHABETS = self.TOP_Y_COORDINATE + 15
        X_COORDINATE_FOR_LEFT_NUMBERS = self.LEFT_MOST_X_COORDINATE + 10
        X_COORDINATE_FOR_RIGHT_NUMBERS = self.RIGHT_MOST_X_COORDINATE - 15
        alph_spacing = self.SPACING // 2
        num_spacing = self.SPACING // 2
        alphabets_for_board = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        numbers_for_board = (1, 2, 3, 4, 5, 6 ,7, 8)

        for alph in alphabets_for_board:
            self.canvas.create_text(
                alph_spacing, Y_COORDINATE_FOR_BOTTOM_ALPHABETS,
                text=alph,
                fill="white",
                font=("Halvetica", 16, "bold")
            )
            self.canvas.create_text(
                alph_spacing, Y_COORDINATE_FOR_TOP_ALPHABETS,
                text=alph,
                fill="white",
                font=("Halvetica", 16, "bold")
            )
            alph_spacing += self.SPACING
        for num in numbers_for_board:
            self.canvas.create_text(
                X_COORDINATE_FOR_LEFT_NUMBERS, num_spacing,
                text=num,
                fill="white",
                font=("Halvetica", 16, "bold")
            )
            self.canvas.create_text(
                X_COORDINATE_FOR_RIGHT_NUMBERS, num_spacing,
                text=num,
                fill="white",
                font=("Halvetica", 16, "bold")
            )
            num_spacing += self.SPACING
    def config(self):
        self.canvas.grid(column=0, row=0)
        self.window_maker.mainloop()