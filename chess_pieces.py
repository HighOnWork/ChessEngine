import tkinter as tk
from PIL import Image, ImageTk

global img_ref_black_pawn 
global img_ref_white_pawn
global img_ref_black_rook
global img_ref_white_rook
global img_ref_white_horse
global img_ref_black_horse
global img_ref_white_bishop
global img_ref_black_bishop

class ChessPieces:
    def __init__(self, windowMaker, canvas):
        self.window_maker = windowMaker
        self.canvas = canvas
        self.NEW_WIDTH = 75
        self.NEW_HEIGHT = 75
        self.CENTER_X = 63
        self.CENTER_Y = 190
    
    def on_button_click(self, event):
        print("Button Clicked")

    def image_taketh_and_changeth(self, fileLocation):
        unconvertedImage = Image.open(fileLocation)
        resized_image = unconvertedImage.resize((self.NEW_WIDTH, self.NEW_HEIGHT), Image.Resampling.LANCZOS)
        img_converted = ImageTk.PhotoImage(resized_image) 
        return img_converted
    
    def black_pawn(self):
        global img_ref_black_pawn
        img_ref_black_pawn = self.image_taketh_and_changeth(".\\BlackPawn.png")
        new_x_for_each_pawn = self.CENTER_X
        for _ in range(8):
            self.canvas.create_image(new_x_for_each_pawn, self.CENTER_Y, image=img_ref_black_pawn)
            new_x_for_each_pawn += 125

    def white_pawn(self):
        global img_ref_white_pawn
        img_ref_white_pawn = self.image_taketh_and_changeth(".\\WhitePawn.png")
        new_x_for_each_pawn = self.CENTER_X
        new_y_for_each_pawn = 1000 - self.CENTER_Y
        for _ in range(8):
            self.canvas.create_image(new_x_for_each_pawn, new_y_for_each_pawn, image=img_ref_white_pawn)
            new_x_for_each_pawn += 125

    def black_rook(self):
        global img_ref_black_rook
        img_ref_black_rook = self.image_taketh_and_changeth(".\\blackRook.png")
        new_y_for_each_rook = 150 // 2
        new_x_for_each_rook = self.CENTER_X
        for _ in range(2):
            self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_black_rook)
            new_x_for_each_rook = 1000 - new_x_for_each_rook

    def white_rook(self):
        global img_ref_white_rook
        img_ref_white_rook = self.image_taketh_and_changeth(".\\WhiteRook.png")
        new_y_for_each_rook = 1000 - 150 // 2
        new_x_for_each_rook = self.CENTER_X
        for _ in range(2):
            self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_white_rook)
            new_x_for_each_rook = 1000 - new_x_for_each_rook

    def black_horse(self):
        global img_ref_black_horse
        img_ref_black_horse = self.image_taketh_and_changeth(".\\BlackHorse.png")
        new_y_for_each_rook = 150 // 2
        new_x_for_each_rook = self.CENTER_X + 125
        for _ in range(2):
            self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_black_horse)
            new_x_for_each_rook = 1000 - new_x_for_each_rook

    def white_horse(self):
        global img_ref_white_horse
        img_ref_white_horse = self.image_taketh_and_changeth(".\\WhiteHorse.png")
        new_y_for_each_rook = 1000 - 150 // 2
        new_x_for_each_rook = self.CENTER_X + 125
        for _ in range(2):
            self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_white_horse)
            new_x_for_each_rook = 1000 - new_x_for_each_rook

    def black_bishop(self):
        global img_ref_black_bishop
        img_ref_black_bishop = self.image_taketh_and_changeth(".\\BlackBishop.png")
        new_y_for_each_rook = 150 // 2
        new_x_for_each_rook = self.CENTER_X + 125 * 2
        
        black_bishop1 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_black_bishop)
        self.canvas.tag_bind(black_bishop1, "<Button-1>", self.on_button_click)

        new_x_for_each_rook = 1000 - new_x_for_each_rook

        black_bishop2 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_black_bishop)
        self.canvas.tag_bind(black_bishop2, "<Button-1>", self.on_button_click)

    def white_bishop(self):
        global img_ref_white_bishop
        img_ref_white_bishop = self.image_taketh_and_changeth(".\\WhiteBishop.png")
        new_y_for_each_rook = 1000 - 150 // 2
        new_x_for_each_rook = self.CENTER_X + 125 * 2
        
        white_bishop1 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_white_bishop)
        self.canvas.tag_bind(white_bishop1, "<Button-1>", self.on_button_click)

        new_x_for_each_rook = 1000 - new_x_for_each_rook

        white_bishop2 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_white_bishop)
        self.canvas.tag_bind(white_bishop2, "<Button-1>", self.on_button_click)

    