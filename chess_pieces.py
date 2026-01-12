from PIL import Image, ImageTk
import os
from movement_of_pieces import movement_of_indivisual_pieces

class ChessPieces:
    def __init__(self, canvas, square_size):
        self.canvas = canvas
        self.indivisualPieces = movement_of_indivisual_pieces(self.canvas)
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
    
    def spawn_pieces(self, code, grid_x, grid_y):
         pixel_x = (grid_x * self.square_size) + (self.square_size // 2)
         pixel_y = (grid_y * self.square_size) + (self.square_size // 2)

         unique_id = self.canvas.create_image(
              pixel_x, pixel_y,
              image=self.images[code],
              tags=(code, "pieces", "unmoved")
         )
         self.canvas.tag_bind(unique_id, 
                              "<Button-1>",
                                lambda event,
                                item_id = unique_id,
                                square_size = self.square_size,
                                collective_id = code: 
                                self.indivisualPieces.move_pieces(event=event, unique_id=item_id, ccd=collective_id, square_size=square_size)
        )
         return unique_id 
    
    