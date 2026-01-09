import tkinter as tk
from chess_board import ChessBoard
from chess_pieces import ChessPieces
from movement_of_pieces import movement_of_indivisual_pieces

back_rank = ["r", "h", "b", "q", "k", "b", "h", "r"]

windowMaker = tk.Tk()
canvas = tk.Canvas(height=1000, width=1000)

new_chess_board = ChessBoard(windowMaker=windowMaker, canvas=canvas)
chess_pieces = ChessPieces(canvas=canvas, square_size=125)

def config():
        canvas.grid(column=0, row=0)
        windowMaker.mainloop()

new_chess_board.create_board()
new_chess_board.lining()
new_chess_board.numbers_and_alphabets()

for i in range(8):
    chess_pieces.spawn_pieces("bp", i, 1)
    chess_pieces.spawn_pieces("wp", i, 6)
    piece_type = back_rank[i]
    chess_pieces.spawn_pieces("b"+piece_type, i , 0)
    chess_pieces.spawn_pieces("w"+piece_type, i, 7)

config()
