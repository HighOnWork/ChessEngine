import tkinter as tk
from PIL import Image, ImageTk
from movement_of_pieces import movement_of_indivisual_pieces
import os

global img_ref_black_pawn 
global img_ref_white_pawn
global img_ref_black_rook
global img_ref_white_rook
global img_ref_white_horse
global img_ref_black_horse
global img_ref_white_bishop
global img_ref_black_bishop
global img_ref_white_queen
global img_ref_black_queen
global img_ref_white_king
global img_ref_black_king

class ChessPieces:
    def __init__(self, canvas, square_size):
        self.canvas = canvas
        self.square_size = square_size
        self.images = {}
        self.load_assets()
    
    def load_assets(self):
        pieces = {
        "wp" : "WhitePawn.png", "bp" : "BlackPawn.png",
        "wr" : "WhiteRook.png", "br" : "BlackRook.png",
        "wh" : "WhiteHorse.png", "bh" : "BlackHorse.png",
        "wb": "WhiteBishop.png", "bb": "BlackBishop.png",
        "wq": "WhiteQueen.png", "bq": "BlackQueen.png",
        "wk": "WhiteKing.png", "bk": "BlackKing.png"
        }

        for code, filename in pieces.items():
            path = os.path.join(".", filename)
            img = Image.open(path)
            img = img.resize((75, 75), Image.Resampling.LANCZOS)
            self.images[code] = ImageTk.PhotoImage(img) 
    
    def spawn_pieces(self, code, grid_y, grid_x):
         pixel_x = (grid_x * self.square_size) + (self.square_size // 2)
         pixel_y = (grid_y * self.square_size) + (self.square_size // 2)

         return self.canvas.create_image(
              pixel_x, pixel_y,
              image=self.images[code],
              tags=(code, "pieces")
         )
    
    