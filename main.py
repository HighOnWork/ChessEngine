import tkinter as tk
from chess_board import ChessBoard
from chess_pieces import ChessPieces
from movement_of_pieces import movement_of_indivisual_pieces



windowMaker = tk.Tk()
canvas = tk.Canvas(height=1000, width=1000)

new_chess_board = ChessBoard(windowMaker=windowMaker, canvas=canvas)
chess_pieces = ChessPieces(canvas=canvas, square_size=125)
# movement_of_indi = movement_of_indivisual_pieces(canvas=canvas)

def config():
        canvas.grid(column=0, row=0)
        windowMaker.mainloop()

new_chess_board.create_board()
new_chess_board.lining()
new_chess_board.numbers_and_alphabets()

for i in range(8):
    chess_pieces.spawn_pieces("bp", i, 0)
    chess_pieces.spawn_pieces("wp", i, 7)
for i in range(2):
    chess_pieces.spawn_pieces("wr" ,i, 1)
    chess_pieces.spawn_pieces("br" ,i, 6)
    chess_pieces.spawn_pieces("wh" ,i, 1)
    chess_pieces.spawn_pieces("bh" ,i, 6)
    chess_pieces.spawn_pieces("wb" ,i, 1)
    chess_pieces.spawn_pieces("bb" ,i, 6)
    chess_pieces.spawn_pieces("wq" ,i, 1)
    chess_pieces.spawn_pieces("bq" ,i, 6)
    chess_pieces.spawn_pieces("wk" ,i, 1)
    chess_pieces.spawn_pieces("bk" ,i, 6)

config()
