import tkinter as tk
from PIL import Image, ImageTk
from movement_of_pieces import movement_of_indivisual_pieces

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
        self.movement_of_indiv = movement_of_indivisual_pieces(canvas=canvas)
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

        new_x_for_each_pawn = []

        new_x_for_each_pawn.append(self.CENTER_X)

        for i in range(1, 8):
            prev_value = new_x_for_each_pawn[i-1]
            new_x_for_each_pawn.append(prev_value + 125)
    
        black_pawn1 = self.canvas.create_image(new_x_for_each_pawn[0], self.CENTER_Y, image=img_ref_black_pawn)
        self.canvas.tag_bind(black_pawn1, "<Button-1>", lambda event, item_id=black_pawn1: self.movement_of_indiv.black_pawns_movement(event,pawn_x_position=new_x_for_each_pawn[0], pawn_y_position=self.CENTER_Y, pawn_item_id=item_id))

        black_pawn2 = self.canvas.create_image(new_x_for_each_pawn[1], self.CENTER_Y, image=img_ref_black_pawn)
        self.canvas.tag_bind(black_pawn2, "<Button-1>", lambda event, item_id=black_pawn2: self.movement_of_indiv.black_pawns_movement(event, pawn_x_position=new_x_for_each_pawn[1], pawn_y_position=self.CENTER_Y, pawn_item_id=item_id))

        black_pawn3 = self.canvas.create_image(new_x_for_each_pawn[2], self.CENTER_Y, image=img_ref_black_pawn)
        self.canvas.tag_bind(black_pawn3, "<Button-1>", lambda event, item_id=black_pawn3: self.movement_of_indiv.black_pawns_movement(event, pawn_x_position=new_x_for_each_pawn[2], pawn_y_position=self.CENTER_Y, pawn_item_id=item_id))

        black_pawn4 = self.canvas.create_image(new_x_for_each_pawn[3], self.CENTER_Y, image=img_ref_black_pawn)
        self.canvas.tag_bind(black_pawn4, "<Button-1>", lambda event, item_id=black_pawn4: self.movement_of_indiv.black_pawns_movement(event, pawn_x_position=new_x_for_each_pawn[3], pawn_y_position=self.CENTER_Y, pawn_item_id=item_id))

        black_pawn5 = self.canvas.create_image(new_x_for_each_pawn[4], self.CENTER_Y, image=img_ref_black_pawn)
        self.canvas.tag_bind(black_pawn5, "<Button-1>", lambda event, item_id=black_pawn5: self.movement_of_indiv.black_pawns_movement(event, pawn_x_position=new_x_for_each_pawn[4], pawn_y_position=self.CENTER_Y, pawn_item_id=item_id))

        black_pawn6 = self.canvas.create_image(new_x_for_each_pawn[5], self.CENTER_Y, image=img_ref_black_pawn)
        self.canvas.tag_bind(black_pawn6, "<Button-1>", lambda event, item_id=black_pawn6: self.movement_of_indiv.black_pawns_movement(event, pawn_x_position=new_x_for_each_pawn[5], pawn_y_position=self.CENTER_Y, pawn_item_id=item_id))

        black_pawn7 = self.canvas.create_image(new_x_for_each_pawn[6], self.CENTER_Y, image=img_ref_black_pawn)
        self.canvas.tag_bind(black_pawn7, "<Button-1>", lambda event, item_id=black_pawn7: self.movement_of_indiv.black_pawns_movement(event, pawn_x_position=new_x_for_each_pawn[6], pawn_y_position=self.CENTER_Y, pawn_item_id=item_id))

        black_pawn8 = self.canvas.create_image(new_x_for_each_pawn[7], self.CENTER_Y, image=img_ref_black_pawn)
        self.canvas.tag_bind(black_pawn8, "<Button-1>", lambda event, item_id=black_pawn8: self.movement_of_indiv.black_pawns_movement(event, pawn_x_position=new_x_for_each_pawn[7], pawn_y_position=self.CENTER_Y, pawn_item_id=item_id))

    def white_pawn(self):
        global img_ref_white_pawn
        img_ref_white_pawn = self.image_taketh_and_changeth(".\\WhitePawn.png")
        # new_x_for_each_pawn = self.CENTER_X
        new_y_for_each_pawn = 1000 - self.CENTER_Y
        
        new_x_for_each_pawn = []

        new_x_for_each_pawn.append(self.CENTER_X)

        for i in range(1, 8):
            prev_value = new_x_for_each_pawn[i-1]
            new_x_for_each_pawn.append(prev_value + 125)

        white_pawn1 = self.canvas.create_image(new_x_for_each_pawn[0], new_y_for_each_pawn, image=img_ref_white_pawn)
        self.canvas.tag_bind(white_pawn1, "<Button-1>", lambda event: self.movement_of_indiv.white_pawns_movement(event=event, pawn_x_position=new_x_for_each_pawn[0], pawn_y_position=new_y_for_each_pawn))

        white_pawn2 = self.canvas.create_image(new_x_for_each_pawn[1], new_y_for_each_pawn, image=img_ref_white_pawn)
        self.canvas.tag_bind(white_pawn2, "<Button-1>", lambda event: self.movement_of_indiv.white_pawns_movement(event=event, pawn_x_position=new_x_for_each_pawn[1], pawn_y_position=new_y_for_each_pawn))

        white_pawn3 = self.canvas.create_image(new_x_for_each_pawn[2], new_y_for_each_pawn, image=img_ref_white_pawn)
        self.canvas.tag_bind(white_pawn3, "<Button-1>", lambda event: self.movement_of_indiv.white_pawns_movement(event=event, pawn_x_position=new_x_for_each_pawn[2], pawn_y_position=new_y_for_each_pawn))

        white_pawn3 = self.canvas.create_image(new_x_for_each_pawn[3], new_y_for_each_pawn, image=img_ref_white_pawn)
        self.canvas.tag_bind(white_pawn3, "<Button-1>", lambda event: self.movement_of_indiv.white_pawns_movement(event=event, pawn_x_position=new_x_for_each_pawn[3], pawn_y_position=new_y_for_each_pawn))

        white_pawn4 = self.canvas.create_image(new_x_for_each_pawn[4], new_y_for_each_pawn, image=img_ref_white_pawn)
        self.canvas.tag_bind(white_pawn4, "<Button-1>", lambda event: self.movement_of_indiv.white_pawns_movement(event=event, pawn_x_position=new_x_for_each_pawn[4], pawn_y_position=new_y_for_each_pawn))

        white_pawn5 = self.canvas.create_image(new_x_for_each_pawn[5], new_y_for_each_pawn, image=img_ref_white_pawn)
        self.canvas.tag_bind(white_pawn5, "<Button-1>", lambda event: self.movement_of_indiv.white_pawns_movement(event=event, pawn_x_position=new_x_for_each_pawn[5], pawn_y_position=new_y_for_each_pawn))

        white_pawn6 = self.canvas.create_image(new_x_for_each_pawn[6], new_y_for_each_pawn, image=img_ref_white_pawn)
        self.canvas.tag_bind(white_pawn6, "<Button-1>", lambda event: self.movement_of_indiv.white_pawns_movement(event=event, pawn_x_position=new_x_for_each_pawn[6], pawn_y_position=new_y_for_each_pawn))

        white_pawn7 = self.canvas.create_image(new_x_for_each_pawn[7], new_y_for_each_pawn, image=img_ref_white_pawn)
        self.canvas.tag_bind(white_pawn7, "<Button-1>", lambda event: self.movement_of_indiv.white_pawns_movement(event=event, pawn_x_position=new_x_for_each_pawn[7], pawn_y_position=new_y_for_each_pawn))
        
    def black_rook(self):
        global img_ref_black_rook
        img_ref_black_rook = self.image_taketh_and_changeth(".\\blackRook.png")
        new_y_for_each_rook = 150 // 2
        new_x_for_each_rook = self.CENTER_X
        
        black_rook1 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_black_rook)
        self.canvas.tag_bind(black_rook1, "<Button-1>", self.on_button_click)

        new_x_for_each_rook = 1000 - new_x_for_each_rook

        black_rook2 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_black_rook)
        self.canvas.tag_bind(black_rook2, "<Button-1>", self.on_button_click)

    def white_rook(self):
        global img_ref_white_rook
        img_ref_white_rook = self.image_taketh_and_changeth(".\\WhiteRook.png")
        new_y_for_each_rook = 1000 - 150 // 2
        new_x_for_each_rook = self.CENTER_X
        
        white_rook1 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_white_rook)
        self.canvas.tag_bind(white_rook1, "<Button-1>", self.on_button_click)

        new_x_for_each_rook = 1000 - new_x_for_each_rook

        white_rook2 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_white_rook)
        self.canvas.tag_bind(white_rook2, "<Button-1>", self.on_button_click)

    def black_horse(self):
        global img_ref_black_horse
        img_ref_black_horse = self.image_taketh_and_changeth(".\\BlackHorse.png")
        new_y_for_each_rook = 150 // 2
        new_x_for_each_rook = self.CENTER_X + 125
        
        black_horse1 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_black_horse)
        self.canvas.tag_bind(black_horse1, "<Button-1>", self.on_button_click)

        new_x_for_each_rook = 1000 - new_x_for_each_rook

        black_horse2 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_black_horse)
        self.canvas.tag_bind(black_horse2, "<Button-1>", self.on_button_click)


    def white_horse(self):
        global img_ref_white_horse
        img_ref_white_horse = self.image_taketh_and_changeth(".\\WhiteHorse.png")
        new_y_for_each_rook = 1000 - 150 // 2
        new_x_for_each_rook = self.CENTER_X + 125
        
        white_horse1 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_white_horse)
        self.canvas.tag_bind(white_horse1, "<Button-1>", self.on_button_click)

        new_x_for_each_rook = 1000 - new_x_for_each_rook

        white_horse2 = self.canvas.create_image(new_x_for_each_rook, new_y_for_each_rook, image=img_ref_white_horse)
        self.canvas.tag_bind(white_horse2, "<Button-1>", self.on_button_click)

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
