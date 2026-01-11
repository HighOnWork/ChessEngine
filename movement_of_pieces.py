# from chess_pieces import ChessPieces
# import tkinter as tk

from tkinter import LAST


class movement_of_indivisual_pieces:
    def __init__(self, canvas):
        self.first_turn_done = False
        self.canvas = canvas
        self.spaces_to_move = []
        self.spaces_to_take = []
        self.move_count = 1
        self.lastID = None
        self.Flag = False
        self.MOVE_RULES = {
            "p" : {'vectors': [(0, -1)], 'vectors_black': [(0, 1)], "sliding" : False, "black": True},
            "r" : {"vectors": [(0,1), (0,-1), (1,0), (-1,0)], "sliding": True, "black": False},
            "b" : {"vectors": [(1,1), (1,-1), (-1,1), (-1,-1)], "sliding": True, "black": False},
            "h" : {"vectors": [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)], "sliding": False, "black": False},
            "k" : {'vectors': [(1,1), (1,-1), (-1,1), (-1,-1), (0,1), (0,-1), (1,0), (-1,0)], "sliding" : False, "black": False},
            "q" : {"vectors": [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)], "sliding": True, "black": False},
        }

    def remove_spaces(self):
        if self.spaces_to_take:
                for space in self.spaces_to_take:
                    self.canvas.delete(space)
                self.spaces_to_take.clear()
        
        if self.spaces_to_move:
                for space in self.spaces_to_move:
                    self.canvas.delete(space)
                self.spaces_to_move.clear()

    def piece_infront(self, square_id):
        square_coords = self.canvas.coords(square_id)  
        overlapping = self.canvas.find_overlapping(*square_coords)
        for item in overlapping:
            if "pieces" in self.canvas.gettags(item):
                self.Flag = True
                return self.canvas.gettags(item)
        return None

    def button_clicked(self, event, square_id, unique_id):
        print("Clicked on indicator")
        square_id_coords = self.canvas.coords(square_id)
        print(square_id_coords)
        center_x = (square_id_coords[0] + square_id_coords[2]) / 2
        center_y = (square_id_coords[1] + square_id_coords[3]) / 2
        self.canvas.move(unique_id ,center_x - self.canvas.coords(unique_id)[0], center_y - self.canvas.coords(unique_id)[1])
        self.move_count += 1
        self.remove_spaces()

    def draw_indicator(self, x, y, size, ID, ccd):
        square = (self.canvas.create_rectangle(x - size // 2, 
                                                    y - size // 2, 
                                                    x + size // 2, 
                                                    y + size // 2, 
                                                    fill="orange", 
                                                    stipple="gray50",
                                                    width=2))
        self.spaces_to_move.append(square)
        self.canvas.tag_bind(square, "<Button-1>", lambda event, s=square, id=ID: self.button_clicked(event, s, id))

        last_piece_id = self.piece_infront(square_id=square)
        
        if last_piece_id is not None:
            piece_color = last_piece_id[0][0] if last_piece_id and last_piece_id[0] else None
            if piece_color == ccd[0]:
                self.canvas.delete(square)
                if self.spaces_to_move and self.spaces_to_move[-1] == square:
                    self.spaces_to_move.pop()
          
          
        

    def move_pieces(self, event, unique_id, ccd, square_size):
        self.Flag = False
        self.remove_spaces()
        coords = self.canvas.coords(unique_id)
        start_x = coords[0]
        start_y = coords[1]

        is_white = ccd[0] == 'w'

        if (self.move_count % 2 == 0 and not is_white) or (self.move_count % 2 != 0 and is_white):
            rules = self.MOVE_RULES[ccd[1]]

            key = "vectors_black" if (not is_white and rules.get("black")) else "vectors"

            for vx, vy in rules[key]:
                cur_x = start_x
                cur_y = start_y

                while True:
                    cur_x += (vx * square_size)
                    cur_y += (vy * square_size)
                    if not (0 < cur_x < 1000 and 0 < cur_y < 1000):
                        break
                   
                    self.draw_indicator(cur_x, cur_y, square_size, unique_id, ccd)

                    if not rules.get("sliding"):
                         break

                    if self.Flag:
                         break
                    
                    

            