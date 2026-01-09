# from chess_pieces import ChessPieces
# import tkinter as tk

class movement_of_indivisual_pieces:
    def __init__(self, canvas):
        # self.chessPieces = ChessPieces()
        self.first_turn_done = False
        self.canvas = canvas
        # self.X1, self.Y1 = 0, 250
        self.SIDE_LENGTH = 125
        # self.X2, self.Y2 = self.X1 + self.SIDE_LENGTH, self.Y1 + self.SIDE_LENGTH
        self.y_max = 900
        self.current_event_tag1 = None
        self.current_event_tag2 = None
        self.current_event_tag3 = None
        self.current_event_tag4 = None
        self.BLACK_PAWN_MOVE = [False] * 8
        self.WHITE_PAWN_MOVE = [False] * 8
        self.spaces_to_move = []
        self.spaces_to_take = []
        self.which_side_can_take = ""
        self.move_count = 1
        self.pieces = (
        "wp", "bp",
        "wr",  "br",
        "wh",  "bh", 
        "wb", "bb", 
        "wq", "bq", 
        "wk", "bk",
        )
        self.MOVE_RULES = {
            "p" : {'vectors': [(0, -1)], 'vectors_black': [(0, 1)], "sliding" : False, "black": True},
            "r" : {"vectors": [(0,1), (0,-1), (1,0), (-1,0)], "sliding": True, "black": False},
            "b" : {"vectors": [(1,1), (1,-1), (-1,1), (-1,-1)], "sliding": True, "black": False},
            "h" : {"vectors": [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)], "sliding": False, "black": False},
            "k" : {'vectors': [(1,1), (1,-1), (-1,1), (-1,-1), (0,1), (0,-1), (1,0), (-1,0)], "sliding" : False, "black": False},
            "q" : {"vectors": [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)], "sliding": True, "black": False},
        }

    def draw_indicator(self, x, y, size):
        self.spaces_to_move.append(self.canvas.create_rectangle(x - size // 2, 
                                                    y - size // 2, 
                                                    x + size // 2, 
                                                    y + size // 2, 
                                                    fill="orange", 
                                                    stipple="gray50",
                                                    width=2))


    def remove_spaces(self):
        if self.spaces_to_take:
                for space in self.spaces_to_take:
                    self.canvas.delete(space)
                self.spaces_to_take.clear()
        
        if self.spaces_to_move:
                for space in self.spaces_to_move:
                    self.canvas.delete(space)
                self.spaces_to_move.clear()

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
                   
                    self.draw_indicator(cur_x, cur_y, square_size)

                    if not rules.get("sliding"):
                         break
                        # self.canvas.coords(unique_id, target_x, target_y)

            self.move_count += 1

    

    # def button_clicked_for_black_rooks(self, event, pawn_item_id, clicked_square_id):
    #     target_coords = self.canvas.coords(clicked_square_id)
    #     rook_coords = self.canvas.coords(pawn_item_id)

    #     if target_coords and rook_coords:
            
    #         dx = target_coords[0] - (rook_coords[0] - 127 // 2)
    #         dy = target_coords[1] - (rook_coords[1] - 150 // 2)
    #         self.canvas.move(pawn_item_id, dx, dy)

    #     self.remove_spaces()
    #     self.move_count += 1

    # def is_something_behind_black_rook(self, rook_x, rook_y):
    #     should_make_square = False
    #     all_white_pawns = self.canvas.find_withtag("white_pawn")
    #     all_black_pawns = self.canvas.find_withtag("black_pawn")
        
    #     for pawn_id in all_white_pawns:
    #         coords = self.canvas.coords(pawn_id)
            
    #         if not coords:
    #             continue
                
    #         white_x = coords[0]
    #         white_y = coords[1]

    #         same_column = abs(rook_x - white_x) < 20
    #         directly_below = abs(white_y - (rook_y - 125)) < 20
    #         if same_column and directly_below:
    #             print("White pawn in the way back") 
    #             return False
            
    #     for pawn_id in all_black_pawns:
    #         coords = self.canvas.coords(pawn_id)
            
    #         if not coords:
    #             continue
                
    #         black_x = coords[0]
    #         black_y = coords[1]

    #         same_column = abs(rook_x - black_x) < 20
    #         directly_below = abs(black_y - (rook_y - 125)) < 20
    #         if same_column and directly_below:
    #             print("Black pawn in the way back")
    #             return False
    #         else:
    #             should_make_square = True
    #     return should_make_square
    
    # def is_something_ahead_for_black_rook(self, rook_x, rook_y):
    #     should_make_square = False
    #     all_white_pawns = self.canvas.find_withtag("white_pawn")
    #     all_black_pawns = self.canvas.find_withtag("black_pawn")
        
    #     for pawn_id in all_white_pawns:
    #         coords = self.canvas.coords(pawn_id)
            
    #         if not coords:
    #             continue
                
    #         white_x = coords[0]
    #         white_y = coords[1]

    #         same_column = abs(rook_x - white_x) < 20
    #         directly_above = abs(white_y - (rook_y + 125)) < 20
    #         if same_column and directly_above:
    #             print("White pawn in the way") 
    #             return False
            
    #     for pawn_id in all_black_pawns:
    #         coords = self.canvas.coords(pawn_id)
            
    #         if not coords:
    #             continue
                
    #         black_x = coords[0]
    #         black_y = coords[1]

    #         same_column = abs(rook_x - black_x) < 20
    #         directly_above = abs(black_y - (rook_y + 125)) < 20
    #         if same_column and directly_above:
    #             print("Black pawn in the way")
    #             return False
    #         else:
    #             should_make_square = True
    #     return should_make_square
    
    # def whitePawnAttack(self, event, ID):
    #     all_black_pawns = self.canvas.find_withtag("black_pawn")

    #     if self.which_side_can_take == "right" or self.which_side_can_take == "both":
    #         self.canvas.move(ID, 125, -125)
    #         white_pawn_coord = self.canvas.coords(ID)

    #         for pawn_id in all_black_pawns:
    #             coords = self.canvas.coords(pawn_id)

    #             if not coords:
    #                 continue

    #             black_x = coords[0]
    #             black_y = coords[1]

    #             if abs(black_x - white_pawn_coord[0]) < 20 and abs(black_y - white_pawn_coord[1]) < 20:
    #                 self.canvas.delete(pawn_id)

    #     elif self.which_side_can_take == "left":
    #         self.canvas.move(ID, -125, -125)
    #         white_pawn_coord = self.canvas.coords(ID)
    #         for pawn_id in all_black_pawns:
    #             coords = self.canvas.coords(pawn_id)

    #             if not coords:
    #                 continue

    #             black_x = coords[0]
    #             black_y = coords[1]

    #             if abs(black_x - white_pawn_coord[0]) < 20 and abs(black_y - white_pawn_coord[1]) < 20:
    #                 self.canvas.delete(pawn_id)

    #     self.remove_spaces()

    #     self.move_count += 1
    
    # def attack_left_for_white_pawn(self, event, ID):
    #     all_black_pawns = self.canvas.find_withtag("black_pawn")

    #     self.canvas.move(ID, -125, -125)

    #     white_pawn_coord = self.canvas.coords(ID)

    #     for pawn_id in all_black_pawns:
    #             coords = self.canvas.coords(pawn_id)

    #             if not coords:
    #                 continue

    #             black_x = coords[0]
    #             black_y = coords[1]

    #             if abs(black_x - white_pawn_coord[0]) < 20 and abs(black_y - white_pawn_coord[1]) < 20:
    #                 self.canvas.delete(pawn_id)
        
    #     self.remove_spaces()

    #     self.move_count += 1

    #     print("Attack")

    # def blackPawnAttack(self, event, ID):
    #     all_white_pawns = self.canvas.find_withtag("white_pawn")

    #     if self.which_side_can_take == "right" or self.which_side_can_take == "both":
    #         self.canvas.move(ID, 125, 125)
    #         black_pawn_coord = self.canvas.coords(ID)

    #         for pawn_id in all_white_pawns:
    #             coords = self.canvas.coords(pawn_id)

    #             if not coords:
    #                 continue

    #             white_x = coords[0]
    #             white_y = coords[1]

    #             if abs(white_x - black_pawn_coord[0]) < 20 and abs(white_y - black_pawn_coord[1]) < 20:
    #                 self.canvas.delete(pawn_id)

    #     elif self.which_side_can_take == "left":
    #         self.canvas.move(ID, -125, 125)
    #         black_pawn_coord = self.canvas.coords(ID)
    #         for pawn_id in all_white_pawns:
    #             coords = self.canvas.coords(pawn_id)

    #             if not coords:
    #                 continue

    #             white_x = coords[0]
    #             white_y = coords[1]

    #             if abs(white_x - black_pawn_coord[0]) < 20 and abs(white_y - black_pawn_coord[1]) < 20:
    #                 self.canvas.delete(pawn_id)

    #     self.remove_spaces()

    #     self.move_count += 1
    

    # def attack_left_for_black_pawn(self, event, ID):
    #     all_white_pawns = self.canvas.find_withtag("white_pawn")

    #     self.canvas.move(ID, -125, 125)

    #     black_pawn_coord = self.canvas.coords(ID)

    #     for pawn_id in all_white_pawns:
    #             coords = self.canvas.coords(pawn_id)

    #             if not coords:
    #                 continue

    #             white_x = coords[0]
    #             white_y = coords[1]

    #             if abs(white_x - black_pawn_coord[0]) < 20 and abs(white_y - black_pawn_coord[1]) < 20:
    #                 self.canvas.delete(pawn_id)
        
    #     self.remove_spaces()

    #     self.move_count += 1

    #     print("Attack")

    # def is_black_pawn_left_or_right(self, coord_point_x, coord_point_y):

    #     left_true = False
    #     right_true = False

    #     all_black_pawns = self.canvas.find_withtag("black_pawn")
        
    #     for pawn_id in all_black_pawns:
    #         coords = self.canvas.coords(pawn_id)
            
    #         if not coords:
    #             continue
                
    #         black_x = coords[0]
    #         black_y = coords[1]

    #         #Basically the difference in x and y coordinates should be less than 20 to be considered the same spot. 
    #         #So lets say if a pawn is at (125, 625) and we are checking (130, 625) then the difference in x is 5 which is less than 20 so its the same spot.
    #         is_left_column = abs((coord_point_x - 125) - black_x) < 20
    #         is_right_column = abs((coord_point_x + 125) - black_x) < 20
            
    #         is_directly_below = abs(black_y - (coord_point_y - 125)) < 20
            
    #         if is_left_column and is_directly_below:
    #             print("White pawn can capture!")
    #             self.which_side_can_take = "left"
    #             print(self.which_side_can_take)
    #             left_true = True
            
    #         elif is_right_column and is_directly_below:
    #             print("White pawn can capture!")
    #             self.which_side_can_take = "right"
    #             print(self.which_side_can_take)
    #             right_true = True

    #     if left_true and right_true:
    #         print("Black pawn can capture on both sides!")
    #         self.which_side_can_take = "both"
    #         print(self.which_side_can_take)
    #         return True
    #     elif left_true or right_true:
    #         return True
    #     else:
    #         return False

    # def is_white_pawn_left_or_right(self, coord_point_x, coord_point_y):

    #     left_true = False
    #     right_true = False

    #     all_white_pawns = self.canvas.find_withtag("white_pawn")
        
    #     for pawn_id in all_white_pawns:
    #         coords = self.canvas.coords(pawn_id)
            
    #         if not coords:
    #             continue
                
    #         white_x = coords[0]
    #         white_y = coords[1]

    #         #Basically the difference in x and y coordinates should be less than 20 to be considered the same spot. 
    #         #So lets say if a pawn is at (125, 625) and we are checking (130, 625) then the difference in x is 5 which is less than 20 so its the same spot.
    #         is_left_column = abs((coord_point_x - 125) - white_x) < 20
    #         is_right_column = abs((coord_point_x + 125) - white_x) < 20
            
    #         is_directly_above = abs(white_y - (coord_point_y + 125)) < 20
            
    #         if is_left_column and is_directly_above:
    #             print("Black pawn can capture!")
    #             self.which_side_can_take = "left"
    #             print(self.which_side_can_take)
    #             left_true = True
            
    #         elif is_right_column and is_directly_above:
    #             print("Black pawn can capture!")
    #             self.which_side_can_take = "right"
    #             print(self.which_side_can_take)
    #             right_true = True

    #     if left_true and right_true:
    #         print("Black pawn can capture on both sides!")
    #         self.which_side_can_take = "both"
    #         print(self.which_side_can_take)
    #         return True
    #     elif left_true or right_true:
    #         return True
    #     else:
    #         return False

    # def is_white_pawn_there(self, coord_point_x, coord_point_y):
        
    #     all_white_pawns = self.canvas.find_withtag("white_pawn")
        
    #     for pawn_id in all_white_pawns:
    #         coords = self.canvas.coords(pawn_id)
            
    #         if not coords:
    #             continue
                
    #         white_x = coords[0]
    #         white_y = coords[1]

    #         #Basically the difference in x and y coordinates should be less than 20 to be considered the same spot. 
    #         #So lets say if a pawn is at (125, 625) and we are checking (130, 625) then the difference in x is 5 which is less than 20 so its the same spot.
    #         same_column = abs(coord_point_x - white_x) < 20
            
    #         is_directly_below = abs(white_y - (coord_point_y + 125)) < 20
            
    #         if same_column and is_directly_below:
    #             print("Blocked by white pawn!")
    #             return True

    #     return False
        
    # def is_black_pawn_there(self, coord_point_x, coord_point_y):
        
    #     all_black_pawns = self.canvas.find_withtag("black_pawn")
        
    #     for pawn_id in all_black_pawns:
    #         coords = self.canvas.coords(pawn_id)
            
    #         if not coords:
    #             continue
                
    #         black_x = coords[0]
    #         black_y = coords[1]

    #         #Basically the difference in x and y coordinates should be less than 20 to be considered the same spot. 
    #         #So lets say if a pawn is at (125, 625) and we are checking (130, 625) then the difference in x is 5 which is less than 20 so its the same spot.
    #         same_column = abs(coord_point_x - black_x) < 20
            
    #         is_directly_below = abs(black_y - (coord_point_y - 125)) < 20
            
    #         if same_column and is_directly_below:
    #             print("Blocked by black pawn!")
    #             return True

    #     return False

    # def white_pawn_selector(self, ID, i):
    #     index_number = 0
    #     for x in range(57, 66):
    #         if ID == x:
    #             if self.WHITE_PAWN_MOVE[index_number] and i == 1:
    #                 return True
    #         else:
    #             index_number += 1
    
    # def black_pawn_selector(self, ID, i):
    #     index_number = 0
    #     for x in range(49, 58):
    #         if ID == x:
    #             if self.BLACK_PAWN_MOVE[index_number] and i == 1:
    #                 return True
    #         else:
    #             index_number += 1
    #     # if ID == 49:
    #     #     if self.BLACK_PAWN_MOVE[0] and i == 1:
    #     #         return True
    #     # elif ID == 50:
    #     #     if self.BLACK_PAWN_MOVE[1] and i ==1:
    #     #         return True

    # def button_clicked_for_white_pawns(self, event, pawn_item_id, rectangles):
    #     index = 0
    #     self.canvas.move(pawn_item_id, 0, -125)
    #     self.remove_spaces()
    #     self.current_event_tag1 = None
    #     for x in range(57, 65):
    #     # if pawn_item_id == 49:
    #         if pawn_item_id == x:
    #             self.WHITE_PAWN_MOVE[index] = True
    #         else:
    #             index += 1
    #     print("should work")
    #     self.first_turn_done = True
    #     self.move_count += 1

    # def pawn_button_clicked_for_white_pawns_first_time_second_way(self, event, pawn_item_id, rectangles):
    #     index = 0
    #     for x in range(57, 65):
    #         if pawn_item_id == x:
    #             if self.WHITE_PAWN_MOVE[index] == False:
    #     # if pawn_item_id == 49:
    #     #     if self.BLACK_PAWN_MOVE[0] == False:
    #                 self.canvas.move(pawn_item_id, 0, -125 * 2)
    #                 self.remove_spaces()
    #                 self.current_event_tag2 = None
    #                 self.WHITE_PAWN_MOVE[index] = True
    #         else:
    #             index += 1

    #     self.first_turn_done = True
    #     self.move_count += 1

    # def button_clicked_for_black_pawns(self, event, pawn_item_id, rectangles, attack_thingys):
    #     index = 0
    #     self.canvas.move(pawn_item_id, 0, 125)
    #     self.remove_spaces()
    #     self.current_event_tag1 = None
    #     for x in range(49, 58):
    #     # if pawn_item_id == 49:
    #         if pawn_item_id == x:
    #             self.BLACK_PAWN_MOVE[index] = True
    #         else:
    #             index += 1
    #     self.move_count += 1

    # def pawn_button_clicked_for_black_pawns_first_time_second_way(self, event, pawn_item_id, rectangles, attack_thingys):
    #     index = 0
    #     for x in range(49, 58):
    #         if pawn_item_id == x:
    #             if self.BLACK_PAWN_MOVE[index] == False:
    #     # if pawn_item_id == 49:
    #     #     if self.BLACK_PAWN_MOVE[0] == False:
    #                 self.canvas.move(pawn_item_id, 0, 125 * 2)
    #                 self.remove_spaces()
    #                 self.current_event_tag2 = None
    #                 self.BLACK_PAWN_MOVE[index] = True
    #         else:
    #             index += 1
    #     self.move_count += 1


    # def black_rook_movement(self, event, rook_item_id):
    #     if self.move_count % 2 == 0:

    #         Flag = True
            
    #         coords = self.canvas.coords(rook_item_id)

    #         print(coords)

    #         current_rook_x = coords[0]
    #         current_rook_y = coords[1]

    #         forward_rook_y = current_rook_y
    #         backward_rook_y = current_rook_y

    #         while Flag == True:

    #             if self.is_something_ahead_for_black_rook(rook_x = current_rook_x, rook_y=forward_rook_y):
    #                 X1, Y1 = current_rook_x - 127 // 2, (forward_rook_y - 150 // 2) + self.SIDE_LENGTH
    #                 X2, Y2 = X1 + self.SIDE_LENGTH, Y1 + self.SIDE_LENGTH

    #                 self.spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))

    #                 forward_rook_y = forward_rook_y + self.SIDE_LENGTH

    #                 if forward_rook_y > 1000:
    #                     Flag = False
    #             else:
    #                 Flag = False

    #         Flag = True

    #         while Flag == True:

    #             if self.is_something_behind_black_rook(rook_x = current_rook_x, rook_y=backward_rook_y):
    #                 X1, Y1 = current_rook_x - 127 // 2, (backward_rook_y - 150 // 2) - self.SIDE_LENGTH
    #                 X2, Y2 = X1 + self.SIDE_LENGTH, Y1 + self.SIDE_LENGTH

    #                 self.spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))

    #                 backward_rook_y = backward_rook_y - self.SIDE_LENGTH

    #                 if backward_rook_y < 0:
    #                     Flag = False
    #             else:
    #                 Flag = False

    #         for square in self.spaces_to_move:
    #             self.canvas.tag_bind(square, "<Button-1>", lambda event, s=square: self.button_clicked_for_black_rooks(event=event, pawn_item_id=rook_item_id, clicked_square_id=s))

    # def black_pawns_movement(self, event, pawn_item_id):

    #     both_exist = False

    #     if self.move_count % 2 == 0:
            
    #         coords = self.canvas.coords(pawn_item_id)

    #         current_pawn_x = coords[0]
    #         current_pawn_y = coords[1]

    #         print(pawn_item_id)

    #         self.remove_spaces()

    #         if self.first_turn_done:
    #             if current_pawn_y <= 900:


    #                 X1, Y1 = current_pawn_x - 127 // 2, (current_pawn_y - 130 // 2) + self.SIDE_LENGTH
    #                 X2, Y2 = X1 + self.SIDE_LENGTH, Y1 + self.SIDE_LENGTH

    #                 # if current_pawn_y <= 900:
                    
    #                 if self.is_white_pawn_left_or_right(coord_point_x=current_pawn_x, coord_point_y=current_pawn_y):
    #                     y_can_take_at1 = (current_pawn_y - 130 // 2) + self.SIDE_LENGTH
    #                     if self.which_side_can_take == "left":
    #                         x_can_take_at1 = current_pawn_x - 93 * 2 - 1
    #                     elif self.which_side_can_take == "right":
    #                         x_can_take_at1 = current_pawn_x + 125 // 2
    #                     elif self.which_side_can_take == "both":
    #                         x_can_take_at1 = current_pawn_x - 93 * 2 - 1
    #                         other_x = current_pawn_x + 125 // 2
    #                         both_exist = True

                        
    #                     y_can_take_at2 = y_can_take_at1 + self.SIDE_LENGTH
    #                     x_can_take_at2 = x_can_take_at1 + self.SIDE_LENGTH

    #                     if both_exist:
    #                         other_x2 = other_x + self.SIDE_LENGTH
    #                         self.spaces_to_take.append(self.canvas.create_rectangle(other_x, y_can_take_at1, other_x2, y_can_take_at2, fill="orange", width=2))

    #                     self.spaces_to_take.append(self.canvas.create_rectangle(x_can_take_at1, y_can_take_at1, x_can_take_at2, y_can_take_at2, fill="orange", width=2))
                        

    #                 if not self.is_white_pawn_there(coord_point_x=current_pawn_x, coord_point_y=current_pawn_y):
                        

    #                     for i in range(2):
                                
                                        
    #                             if self.black_pawn_selector(ID=pawn_item_id, i=i):
    #                                 continue
                    
    #                             self.spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))
    #                             Y1 += 125
    #                             Y2 += 125
    #                         # tk.Misc.lift(spaces_to_move[i])
    #                     # else:
    #                     #     spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))
                        
    #                 if len(self.spaces_to_move) > 0 :
    #                     self.current_event_tag1 = self.spaces_to_move[0]
    #                     self.canvas.tag_bind(self.current_event_tag1, "<Button-1>", lambda event: self.button_clicked_for_black_pawns(event=event, pawn_item_id=pawn_item_id, rectangles=self.spaces_to_move, attack_thingys=self.spaces_to_take))

    #                 if len(self.spaces_to_move) > 1:
    #                     self.current_event_tag2 = self.spaces_to_move[1]
    #                     self.canvas.tag_bind(self.current_event_tag2, "<Button-1>", lambda event: self.pawn_button_clicked_for_black_pawns_first_time_second_way(event=event, pawn_item_id=pawn_item_id, rectangles=self.spaces_to_move, attack_thingys=self.spaces_to_take))

    #                 if len(self.spaces_to_take) > 0:
    #                     self.current_event_tag3 = self.spaces_to_take[0]
    #                     self.canvas.tag_bind(self.current_event_tag3, "<Button-1>", lambda event: self.blackPawnAttack(event=event, ID=pawn_item_id))

    #                 if len(self.spaces_to_take) > 1:
    #                     self.current_event_tag4 = self.spaces_to_take[1]
    #                     self.canvas.tag_bind(self.current_event_tag4, "<Button-1>", lambda event: self.attack_left_for_black_pawn(event=event, ID=pawn_item_id))
                        


        
    # def white_pawns_movement(self, event, ID):

    #     if self.move_count % 2 != 0:
    #         self.remove_spaces()

    #         both_exist = False

    #         print(ID)

    #         coords = self.canvas.coords(ID)

    #         pawn_x_position = coords[0]
    #         pawn_y_position = coords[1]

    #         X1, Y1 = (pawn_x_position - 125 // 2) - 1, (pawn_y_position - (120 // 2)) - self.SIDE_LENGTH
    #         X2, Y2 = X1 + self.SIDE_LENGTH, Y1 + self.SIDE_LENGTH

    #         if pawn_y_position >= 190:

    #             if self.is_black_pawn_left_or_right(coord_point_x=pawn_x_position, coord_point_y=pawn_y_position):
    #                     y_can_take_at1 = (pawn_y_position - 120 // 2) - self.SIDE_LENGTH
    #                     if self.which_side_can_take == "left":
    #                         x_can_take_at1 = pawn_x_position - 93 * 2 - 1
    #                     elif self.which_side_can_take == "right":
    #                         x_can_take_at1 = pawn_x_position + 125 // 2
    #                     elif self.which_side_can_take == "both":
    #                         x_can_take_at1 = pawn_x_position - 93 * 2 - 1
    #                         other_x = pawn_x_position + 125 // 2
    #                         both_exist = True

                        
    #                     y_can_take_at2 = y_can_take_at1 + self.SIDE_LENGTH
    #                     x_can_take_at2 = x_can_take_at1 + self.SIDE_LENGTH

    #                     if both_exist:
    #                         other_x2 = other_x + self.SIDE_LENGTH
    #                         self.spaces_to_take.append(self.canvas.create_rectangle(other_x, y_can_take_at1, other_x2, y_can_take_at2, fill="orange", width=2))

    #                     self.spaces_to_take.append(self.canvas.create_rectangle(x_can_take_at1, y_can_take_at1, x_can_take_at2, y_can_take_at2, fill="orange", width=2))

    #             if not self.is_black_pawn_there(coord_point_x=pawn_x_position, coord_point_y=pawn_y_position):

    #                 for i in range(2):
    #                     if self.white_pawn_selector(ID=ID, i=i):
    #                         continue
                        
    #                     self.spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))
    #                     Y1 -= 125
    #                     Y2 -= 125
    #             # else:
    #             #     self.spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))

    #                 for spaces in self.spaces_to_move:
    #                     self.canvas.tag_bind(spaces, "<Button-1>", self.button_clicked_for_white_pawns)
                    
    #             if len(self.spaces_to_move) > 0 :
    #                         self.current_event_tag1 = self.spaces_to_move[0]
    #                         self.canvas.tag_bind(self.current_event_tag1, "<Button-1>", lambda event: self.button_clicked_for_white_pawns(event=event, pawn_item_id=ID, rectangles=self.spaces_to_move))

    #             if len(self.spaces_to_move) > 1:
    #                 self.current_event_tag2 = self.spaces_to_move[1]
    #                 self.canvas.tag_bind(self.current_event_tag2, "<Button-1>", lambda event: self.pawn_button_clicked_for_white_pawns_first_time_second_way(event=event, pawn_item_id=ID, rectangles=self.spaces_to_move))

    #             if len(self.spaces_to_take) > 0:
    #                     self.current_event_tag3 = self.spaces_to_take[0]
    #                     self.canvas.tag_bind(self.current_event_tag3, "<Button-1>", lambda event: self.whitePawnAttack(event=event, ID=ID))

    #             if len(self.spaces_to_take) > 1:
    #                 self.current_event_tag4 = self.spaces_to_take[1]
    #                 self.canvas.tag_bind(self.current_event_tag4, "<Button-1>", lambda event: self.attack_left_for_white_pawn(event=event, ID=ID))
                    
        