# from chess_pieces import ChessPieces
# import tkinter as tk

class movement_of_indivisual_pieces:
    def __init__(self, canvas):
        # self.chessPieces = ChessPieces()
        self.first_turn_done = False
        self.canvas = canvas
        # self.X1, self.Y1 = 0, 250
        # self.SIDE_LENGTH = 125
        # self.X2, self.Y2 = self.X1 + self.SIDE_LENGTH, self.Y1 + self.SIDE_LENGTH
        # self.y_max = 900
        # self.current_event_tag1 = None
        # self.current_event_tag2 = None
        # self.current_event_tag3 = None
        # self.current_event_tag4 = None
        # self.BLACK_PAWN_MOVE = [False] * 8
        # self.WHITE_PAWN_MOVE = [False] * 8
        self.spaces_to_move = []
        self.spaces_to_take = []
        # self.which_side_can_take = ""
        self.move_count = 1
        # self.pieces = (
        # "wp", "bp",
        # "wr",  "br",
        # "wh",  "bh", 
        # "wb", "bb", 
        # "wq", "bq", 
        # "wk", "bk",
        # )
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

    def button_clicked(self, event, square_id, unique_id):
        print("Clicked on indicator")
        square_id_coords = self.canvas.coords(square_id)
        print(square_id_coords)
        center_x = (square_id_coords[0] + square_id_coords[2]) / 2
        center_y = (square_id_coords[1] + square_id_coords[3]) / 2
        self.canvas.move(unique_id ,center_x - self.canvas.coords(unique_id)[0], center_y - self.canvas.coords(unique_id)[1])
        self.move_count += 1
        self.remove_spaces()

    def draw_indicator(self, x, y, size, ID):
        self.spaces_to_move.append(self.canvas.create_rectangle(x - size // 2, 
                                                    y - size // 2, 
                                                    x + size // 2, 
                                                    y + size // 2, 
                                                    fill="orange", 
                                                    stipple="gray50",
                                                    width=2))
        for square in self.spaces_to_move:
            self.canvas.tag_bind(square, "<Button-1>", lambda event, s=square, id=ID: self.button_clicked(event, s, id))

    def move_pieces(self, event, unique_id, ccd, square_size):
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
                   
                    self.draw_indicator(cur_x, cur_y, square_size, unique_id)

                    if not rules.get("sliding"):
                         break

            