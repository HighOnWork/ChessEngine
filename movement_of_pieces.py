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
        self.type_checking = ""
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

    def is_still_in_check(self, ccd, x, y, item, size):
        # Safety Check: If the item was already removed by collision logic, stop.
        if item not in self.spaces_to_move:
            return

        all_intercepting_coords = []
        
        # Guard clause: If we don't know what checked us, we can't calculate the block
        if not self.type_checking: 
            return

        coords_for_checking_piece = self.canvas.coords(self.type_checking)
        
        # Calculate coordinates of the piece checking the king
        attacker_center_x = int(coords_for_checking_piece[0])
        attacker_center_y = int(coords_for_checking_piece[1])

        king_x, king_y = self.get_king_coords(ccd[0])
        if king_x is None: return
        king_x, king_y = int(king_x), int(king_y)

        move_rules = self.MOVE_RULES[self.type_checking[1]]
        
        if move_rules["black"]:
            rule = "vectors" if self.type_checking[0] == "w" else "vectors_black"
        else:
            rule = "vectors"
            
        turns = 8 if move_rules['sliding'] == True else 2
        
        for vx, vy in move_rules[rule]:
            cur_x = attacker_center_x
            cur_y = attacker_center_y

            current_ray = []

            current_ray.append((cur_x, cur_y))

            for turn in range(turns):
                if not (0 < cur_x < size * 8 and 0 < cur_y < size * 8): break
                cur_x += int(vx * size) 
                cur_y += int(vy * size)

                current_ray.append((cur_x, cur_y))

                if (king_x, king_y) in current_ray:
                    all_intercepting_coords.extend(current_ray)
        
        if (int(x), int(y)) not in all_intercepting_coords:
            # Safely remove specific item
            if item in self.spaces_to_move:
                self.spaces_to_move.remove(item)
                self.canvas.delete(item)
        else:
            pass

    def get_king_coords(self, king_color):
        king_tag = f"{king_color}k" 
        king_ids = self.canvas.find_withtag(king_tag)
        if not king_ids:
            return None, None
        king_id = king_ids[0]
        coords = self.canvas.coords(king_id)
        center_x = coords[0]
        center_y = coords[1]
        return center_x, center_y

    def is_king_in_check(self, ccd, size):
        king_color = ccd[0]
        enemy_color = 'b' if king_color == 'w' else 'w'
        king_x, king_y = self.get_king_coords(king_color)
        
        if king_x is None: return False

        for piece_type, rules in self.MOVE_RULES.items():
            if piece_type == "p":
                look_dir = -1 if king_color == 'w' else 1 
                pawn_attacks = [
                    (king_x - size, king_y + (look_dir * size)), 
                    (king_x + size, king_y + (look_dir * size)) 
                ]
                for px, py in pawn_attacks:
                    overlapping = self.canvas.find_overlapping(px - 5, py - 5, px + 5, py + 5)
                    for item in overlapping:
                        tags = self.canvas.gettags(item)
                        if f'{enemy_color}p' in tags:
                            self.type_checking = next(t for t in tags if t == f'{enemy_color}p')
                            return True
            else:
                vectors = rules['vectors']
                max_steps = 8 if rules['sliding'] else 2 
                for vx, vy in vectors:
                    cur_x, cur_y = king_x, king_y
                    for _ in range(1, max_steps):
                        cur_x += vx * size 
                        cur_y += vy * size 
                        if not (0 < cur_x < size * 8 and 0 < cur_y < size * 8):
                            break

                        items = self.canvas.find_overlapping(cur_x - 5, cur_y - 5, cur_x + 5, cur_y + 5)
                        piece_found = False
                        for item in items:
                            tags = self.canvas.gettags(item)
                            if any(t in tags for t in ['current', 'square']): continue 
                            
                            if any(t.startswith('w') or t.startswith('b') for t in tags):
                                piece_found = True
                                if any(t.startswith(king_color) for t in tags):
                                    break 
                                if any(t.startswith(enemy_color) for t in tags):
                                    enemy_piece_tag = next(t for t in tags if t.startswith(enemy_color))
                                    found_type = enemy_piece_tag[1]
                                    if found_type == piece_type or found_type == 'q':
                                        self.type_checking = enemy_piece_tag
                                        return True
                                    else:
                                        break 
                        if piece_found: break
        return False

    def piece_to_the_side(self, x, y, size, unique_id, ccd):
        """ Checks for enemies diagonally in front of the pawn """
        direction = -1 if ccd[0] == 'w' else 1
        
        # Diagonal offsets
        diagonals = [
            (x - size, y + (direction * size)), # Left
            (x + size, y + (direction * size))  # Right
        ]
        
        for dx, dy in diagonals:
            if 0 < dx < (size * 8) and 0 < dy < (size * 8):
                overlapping = self.canvas.find_overlapping(dx - 5, dy - 5, dx + 5, dy + 5)
                for item in overlapping:
                    tags = self.canvas.gettags(item)
                    # Check if it is a piece and NOT the board
                    if any(t.startswith('w') or t.startswith('b') for t in tags):
                        # Ensure it is an enemy
                        if (ccd[0] == 'w' and any(t.startswith('b') for t in tags)) or \
                           (ccd[0] == 'b' and any(t.startswith('w') for t in tags)):
                            self.draw_capture_indicator(dx, dy, size, unique_id, item, ccd)

    def draw_capture_indicator(self, x, y, size, ID, target_piece_id, ccd):
        square = self.canvas.create_rectangle(
            x - size // 2, y - size // 2,
            x + size // 2, y + size // 2,
            fill="red", stipple="gray50", width=2
        )
        self.spaces_to_move.append(square)
        self.canvas.tag_bind(square, "<Button-1>", 
            lambda event, s=square, id=ID, target=target_piece_id: 
            self.button_clicked(event, s, id, ccd=ccd, size=size, special_flag=True, lpi=target))

    def piece_infront(self, square_id):
        square_coords = self.canvas.coords(square_id)  
        overlapping = self.canvas.find_overlapping(*square_coords)
        for item in overlapping:
            tags = self.canvas.gettags(item)
            # Looking for chess pieces, not the board squares or the indicator itself
            if any(t.startswith('w') or t.startswith('b') for t in tags) and item != square_id:
                self.Flag = True
                return tags, item
        return None

    def button_clicked(self, event, square_id, unique_id, ccd, size, lpi=None, special_flag=False):
        self.check_flag = False
        print("Clicked on indicator")
        tags = self.canvas.gettags(unique_id)
        
        if "unmoved" in tags:
            self.canvas.dtag(unique_id, "unmoved")
        
        if special_flag and lpi:
            self.canvas.delete(lpi)
            
        square_id_coords = self.canvas.coords(square_id)
        
        # Calculate new center
        dest_x = (square_id_coords[0] + square_id_coords[2]) / 2
        dest_y = (square_id_coords[1] + square_id_coords[3]) / 2
        
        # Calculate current center
        curr_coords = self.canvas.coords(unique_id)
        curr_x = curr_coords[0]
        curr_y = curr_coords[1]
        
        # Move piece
        self.canvas.move(unique_id, dest_x - curr_x, dest_y - curr_y)
        if self.is_king_in_check(ccd=ccd, size=size):
            self.canvas.move(unique_id, -(dest_x - curr_x), -(dest_y - curr_y))
        else:
            self.move_count += 1
            self.remove_spaces()

    def draw_indicator(self, x, y, size, ID, ccd):
        self.Flag = False
        square = (self.canvas.create_rectangle(x - size // 2, 
                                               y - size // 2, 
                                               x + size // 2, 
                                               y + size // 2, 
                                               fill="orange", 
                                               stipple="gray50",
                                               width=2))
        self.spaces_to_move.append(square)
        self.canvas.tag_bind(square, "<Button-1>", lambda event, s=square, id=ID: self.button_clicked(event, s, id, ccd=ccd, size=size))

        result = self.piece_infront(square_id=square)
        
        # We must keep track of whether the square is still valid
        square_valid = True

        if result is not None:
            last_piece_tags, niche_id = result
            # Get the color of the piece in front
            # Assumes tags like ['wp', 'unmoved', ...] or ['br', ...]
            piece_tag = next((t for t in last_piece_tags if t.startswith('w') or t.startswith('b')), None)
            
            if piece_tag:
                piece_color = piece_tag[0]
                
                # If friendly piece OR if it's a pawn (pawns can't take forward)
                if piece_color == ccd[0] or ccd[1] == "p":
                    if square in self.spaces_to_move:
                        self.spaces_to_move.remove(square)
                    self.canvas.delete(square)
                    square_valid = False # Mark as invalid

                # If enemy piece (and not a pawn moving forward) -> Capture logic
                elif piece_color != ccd[0] and ccd[1] != "p":
                    self.canvas.itemconfig(square, fill="red")
                    self.canvas.tag_bind(square, "<Button-1>", lambda event, s=square, id=ID: self.button_clicked(event, s, id, special_flag = True, lpi=niche_id, ccd=ccd, size=size))

        # Only check for checkmate constraints if the square still exists
        if self.check_flag and square_valid:
            self.is_still_in_check(ccd, x, y, square, size)

    def move_pieces(self, event, unique_id, ccd, square_size):
        self.check_flag = False
        self.remove_spaces()
        
        coords = self.canvas.coords(unique_id)
        # Use center point for clearer math
        start_x = coords[0]
        start_y = coords[1]
        
        is_white = ccd[0] == 'w'

        if self.is_king_in_check(ccd=ccd, size=square_size):
            self.check_flag = True
            print("KING IS IN CHECK")
        
        # Turn enforcement
        if (self.move_count % 2 == 0 and not is_white) or (self.move_count % 2 != 0 and is_white):
            
            # --- FIX: Handle Pawn Diagonal Captures ---
            if ccd[1] == 'p':
                self.piece_to_the_side(start_x, start_y, square_size, unique_id, ccd)

            # Standard Movements
            rules = self.MOVE_RULES[ccd[1]]
            key = "vectors_black" if (not is_white and rules.get("black")) else "vectors"

            for vx, vy in rules[key]:
                cur_x, cur_y = start_x, start_y
                
                max_steps = 1
                if ccd[1] == 'p' and "unmoved" in self.canvas.gettags(unique_id):
                    max_steps = 2
                
                if rules.get("sliding"): max_steps = 8

                for step in range(max_steps):
                    cur_x += (vx * square_size)
                    cur_y += (vy * square_size)
                    
                    if not (0 < cur_x < square_size * 8 and 0 < cur_y < square_size * 8): break

                    self.Flag = False
                    self.draw_indicator(cur_x, cur_y, square_size, unique_id, ccd)
                    
                    # If blocked, stop rays for pawns and non-sliding pieces
                    if self.Flag: 
                        break 
                    
                    if not rules.get("sliding") and ccd[1] != 'p':
                        break