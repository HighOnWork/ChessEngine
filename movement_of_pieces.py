# from chess_pieces import ChessPieces
# import tkinter as tk

from tkinter import FALSE, LAST, TRUE
from typing import Sized


class movement_of_indivisual_pieces:
    def __init__(self, canvas):
        self.first_turn_done = False
        self.canvas = canvas
        self.spaces_to_move = []
        self.spaces_to_take = []
        self.move_count = 1
        self.lastID = None
        self.destroyPiece = False
        self.check_flag = False
        self.Flag = False
        self.RightFlag = False
        self.LeftFlag = False
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


    def get_king_coords(self, king_color):
        # king_color should be 'w' or 'b'
        # Construct the tag, e.g., 'wk' or 'bk'
        king_tag = f"{king_color}k" 
        
        # Find the item on canvas with this tag
        king_ids = self.canvas.find_withtag(king_tag)
        
        if not king_ids:
            print(f"Error: Could not find King with tag {king_tag}")
            return None, None

        # We assume there is only one King of that color; take the first ID
        king_id = king_ids[0]
        
        # Get coordinates [x1, y1, x2, y2]
        coords = self.canvas.coords(king_id)
        
        # Calculate center point
        center_x = coords[0] // 2
        center_y = coords[1] // 2
        
        return center_x, center_y


    def is_king_in_check(self, ccd, size):
        """
        ccd: Color of the current turn (e.g. 'wp' -> we need to check 'w' King)
        size: Square size for calculations
        """
        # 1. Determine King Color ('w' or 'b')
        king_color = ccd[0] # Assumes ccd is something like 'wp', 'br', etc.
        enemy_color = 'b' if king_color == 'w' else 'w'
        
        # 2. GET ACTUAL KING COORDINATES
        king_x, king_y = self.get_king_coords(king_color)
        
        if king_x is None: return False # Safety check if King is missing

        # Iterate through every piece type to see if that piece type is attacking the King
        for piece_type, rules in self.MOVE_RULES.items():
            
            # --- 1. PAWN LOGIC ---
            if piece_type == "p":
                # If I am white, I look "Up" (negative Y) for Black pawns ready to strike "Down"
                # If I am black, I look "Down" (positive Y) for White pawns ready to strike "Up"
                look_dir = -1 if king_color == 'w' else 1 
                
                pawn_attacks = [
                    (king_x - size, king_y + (look_dir * size)), # Left corner
                    (king_x + size, king_y + (look_dir * size))  # Right corner
                ]

                for px, py in pawn_attacks:
                    overlapping = self.canvas.find_overlapping(px - 5, py - 5, px + 5, py + 5)
                    for item in overlapping:
                        tags = self.canvas.gettags(item)
                        # Check for Enemy Color + Pawn Tag
                        if f'{enemy_color}p' in tags:
                            return True

            # --- 2. STANDARD PIECE LOGIC (R, B, N, Q, K) ---
            else:
                vectors = rules['vectors']
                max_steps = 8 if rules['sliding'] else 2 
                
                for vx, vy in vectors:
                    # RESET RAYCAST TO KING POSITION
                    cur_x, cur_y = king_x, king_y
                    
                    for _ in range(1, max_steps):
                        cur_x += vx * size 
                        cur_y += vy * size 
                        
                        # Stop if off board (Assuming board is 0-800 pixels)
                        if not (0 < cur_x < size * 8 and 0 < cur_y < size * 8):
                            break

                        # Check collision
                        items = self.canvas.find_overlapping(cur_x - 5, cur_y - 5, cur_x + 5, cur_y + 5)
                        
                        piece_found = False
                        for item in items:
                            tags = self.canvas.gettags(item)
                            
                            # Skip board squares
                            if any(t in tags for t in ['current', 'square']): continue 
                            
                            # Check for pieces
                            if any(t.startswith('w') or t.startswith('b') for t in tags):
                                piece_found = True
                                
                                # 1. Is it friendly? (Blocker)
                                if any(t.startswith(king_color) for t in tags):
                                    break 
                                
                                # 2. Is it an enemy?
                                if any(t.startswith(enemy_color) for t in tags):
                                    # Check exact piece type
                                    enemy_piece_tag = next(t for t in tags if t.startswith(enemy_color))
                                    found_type = enemy_piece_tag[1] # 'r', 'b', 'q' etc.

                                    if found_type == piece_type or found_type == 'q':
                                        return True
                                    else:
                                        break # Enemy blocks, but is wrong type (e.g. found Knight while looking for Rook)
                        
                        if piece_found: break # Stop ray in this direction

        return False



    def piece_to_the_side(self, x, y, size, unique_id, ccd):
        """ Checks for enemies diagonally in front of the pawn """
        # Calculate diagonal coordinates based on color
        direction = -1 if ccd[0] == 'w' else 1
        
        # Diagonal offsets: (Left-Diagonal, Right-Diagonal)
        diagonals = [
            (x - size, y + (direction * size)), # Left
            (x + size, y + (direction * size))  # Right
        ]
        for dx, dy in diagonals:
    # Only check if the coordinates are actually on the 8x8 board
            if 0 < dx < (size * 8) and 0 < dy < (size * 8):
                overlapping = self.canvas.find_overlapping(dx - 5, dy - 5, dx + 5, dy + 5)
                for item in overlapping:
                    tags = self.canvas.gettags(item)
                    if "pieces" in tags:
                        # Check if it's an enemy
                        if (ccd[0] == 'w' and 'bp' in tags) or (ccd[0] == 'b' and 'wp' in tags):
                            self.draw_capture_indicator(dx, dy, size, unique_id, item)

    def draw_capture_indicator(self, x, y, size, ID, target_piece_id):
        """ Creates the red square for captures and binds the click event """
        square = self.canvas.create_rectangle(
            x - size // 2, y - size // 2,
            x + size // 2, y + size // 2,
            fill="red", stipple="gray50", width=2
        )
        self.spaces_to_move.append(square)
        # Crucial: Bind the click to destroy the enemy piece
        self.canvas.tag_bind(square, "<Button-1>", 
            lambda event, s=square, id=ID, target=target_piece_id: 
            self.button_clicked(event, s, id, special_flag=True, lpi=target))



    def item_destroyed(self, event, square_id, unique_id):
        pass

    def piece_infront(self, square_id):
        square_coords = self.canvas.coords(square_id)  
        overlapping = self.canvas.find_overlapping(*square_coords)
        for item in overlapping:
            tags = self.canvas.gettags(item)
            if "pieces" in tags:
                self.Flag = True
                return tags, item
        return None

    def button_clicked(self, event, square_id, unique_id,  lpi=None, special_flag=False):
        self.check_flag = False
        print("Clicked on indicator")
        tags = self.canvas.gettags(unique_id)
        if "unmoved" in tags:
            self.canvas.dtag(unique_id, "unmoved")
        if special_flag and lpi:
            self.canvas.delete(lpi)
        square_id_coords = self.canvas.coords(square_id)
        print(square_id_coords)
        center_x = (square_id_coords[0] + square_id_coords[2]) / 2
        center_y = (square_id_coords[1] + square_id_coords[3]) / 2
        self.canvas.move(unique_id ,center_x - self.canvas.coords(unique_id)[0], center_y - self.canvas.coords(unique_id)[1])
        self.move_count += 1
        self.remove_spaces()

    def draw_indicator(self, x, y, size, ID, ccd):
        self.Flag = False
        self.RightFlag = False
        self.LeftFlag = False
        last_piece_id = None
        niche_id = None

        square = (self.canvas.create_rectangle(x - size // 2, 
                                                    y - size // 2, 
                                                    x + size // 2, 
                                                    y + size // 2, 
                                                    fill="orange", 
                                                    stipple="gray50",
                                                    width=2))
        self.spaces_to_move.append(square)
        self.canvas.tag_bind(square, "<Button-1>", lambda event, s=square, id=ID: self.button_clicked(event, s, id))

        result = self.piece_infront(square_id=square)

        tags = self.canvas.gettags(ID)

        orig_index = self.spaces_to_move.index(square)
        item = self.spaces_to_move[orig_index]
        

        if result is not None:
            last_piece_id, niche_id = result
        
        if last_piece_id is not None:
            print(last_piece_id)

            piece_color = last_piece_id[0][0] if last_piece_id and last_piece_id[0] else None

            if piece_color == ccd[0] or ccd[1] == "p":

                self.spaces_to_move.pop(orig_index)
                self.canvas.delete(item)
 
            elif piece_color != ccd[0]:
                self.canvas.itemconfig(square, fill="red")
                self.canvas.tag_bind(item, "<Button-1>", lambda event, s=square, id=ID: self.button_clicked(event, s, id, special_flag = True, lpi=niche_id))

        

    def move_pieces(self, event, unique_id, ccd, square_size):
        self.check_flag = False
        self.remove_spaces()
        
        # Get clicked piece coords (keep this for standard movement logic later)
        coords = self.canvas.coords(unique_id)
        start_x, start_y = coords[0], coords[1]
        is_white = ccd[0] == 'w'

        # --- CHANGED LINE BELOW ---
        # No longer passing start_x/y to the check function
        if self.is_king_in_check(ccd=ccd, size=square_size):
            self.check_flag = True
            print("KING IS IN CHECK")
        
        if self.check_flag and ccd[1] == "k" or not self.check_flag:
            # 2. HANDLE STANDARD MOVEMENT (Forward/Vectors)
            if (self.move_count % 2 == 0 and not is_white) or (self.move_count % 2 != 0 and is_white):
                rules = self.MOVE_RULES[ccd[1]]
                key = "vectors_black" if (not is_white and rules.get("black")) else "vectors"

                for vx, vy in rules[key]:
                    cur_x, cur_y = start_x, start_y
                
                    # For pawns, we only check 1 or 2 squares forward
                    max_steps = 1
                    if ccd[1] == 'p' and "unmoved" in self.canvas.gettags(unique_id):
                        max_steps = 2
                
                    # For sliding pieces (Rook/Queen), use a high number
                    if rules.get("sliding"): max_steps = 8

                    for step in range(max_steps):
                        cur_x += (vx * square_size)
                        cur_y += (vy * square_size)
                    
                        if not (0 < cur_x < 1000 and 0 < cur_y < 1000): break

                        # Pawns cannot move forward if blocked (Flag logic)
                        self.Flag = False
                        self.draw_indicator(cur_x, cur_y, square_size, unique_id, ccd)
                    
                        if self.Flag: # If square is blocked
                            # If it's a pawn moving forward, delete the orange indicator (can't jump)
                            
                            break 
                    
                        if not rules.get("sliding") and ccd[1] != 'p':
                            break

                
                    