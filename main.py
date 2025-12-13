import tkinter as tk
from chess_board import chess_board
from chess_pieces import ChessPieces

windowMaker = tk.Tk()
canvas = tk.Canvas(height=1000, width=1000)

new_chess_board = chess_board(windowMaker=windowMaker, canvas=canvas)
chess_pieces = ChessPieces(windowMaker=windowMaker, canvas=canvas)

new_chess_board.create_board()
new_chess_board.lining()
new_chess_board.numbers_and_alphabets()
chess_pieces.black_pawn()
chess_pieces.white_pawn()
new_chess_board.config()
