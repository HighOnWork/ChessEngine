import tkinter as tk
from chess_board import chess_board
from chess_pieces import ChessPieces
from movement_of_pieces import movement_of_indivisual_pieces



windowMaker = tk.Tk()
canvas = tk.Canvas(height=1000, width=1000)

new_chess_board = chess_board(windowMaker=windowMaker, canvas=canvas)
chess_pieces = ChessPieces(windowMaker=windowMaker, canvas=canvas)
# movement_of_indi = movement_of_indivisual_pieces(canvas=canvas)

new_chess_board.create_board()
new_chess_board.lining()
new_chess_board.numbers_and_alphabets()
chess_pieces.black_pawn()
chess_pieces.white_pawn()
chess_pieces.black_rook()
chess_pieces.white_rook()
chess_pieces.black_horse()
chess_pieces.white_horse()
chess_pieces.black_bishop()
chess_pieces.white_bishop()
chess_pieces.black_queen()
chess_pieces.white_queen()
chess_pieces.black_king()
chess_pieces.white_king()

new_chess_board.config()
