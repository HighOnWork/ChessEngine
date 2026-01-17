from tkinter import FALSE, LAST, TRUE, messagebox
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
        self.type_checking_ccd = ""
        self.Flag = False
        self.all_intercepting_coords = []
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

    def show_game_over(self, winner):
        messagebox.showinfo("Game over", f"CHECKMATE! {winner} wins the match.")
        self.canvas.master.destroy()

    def can_castle(self, ccd, size):
        # 1. Basic Requirements: King must not have moved
        king_id = self.canvas.find_withtag(ccd)[0]
        king_tags = self.canvas.gettags(king_id)
        
        # We assume you add the tag "unmoved" when creating pieces
        if "unmoved" not in king_tags:
            return

        king_coords = self.canvas.coords(king_id)
        k_x, k_y = king_coords[0], king_coords[1]

        # 2. Check both sides (Left/Queen-side and Right/King-side)
        # Directions: -1 is Left, +1 is Right
        sides = [
            {"dir": -1, "rook_col": 0, "empty_cols": [1, 2, 3], "type": "long"},
            {"dir": 1, "rook_col": 7, "empty_cols": [5, 6], "type": "short"}
        ]

        for side in sides:
            # Find the Rook at the expected location
            # Note: We calculate rook X based on column index (0 or 7)
            # Center of a square = (col * size) + (size / 2)
            rook_target_x = (side["rook_col"] * size) + (size / 2)
            
            # Find items at that specific rook location
            items_at_rook = self.canvas.find_overlapping(
                rook_target_x - 5, k_y - 5, rook_target_x + 5, k_y + 5
            )

            rook_id = None
            for item in items_at_rook:
                tags = self.canvas.gettags(item)
                # Check for friendly Rook with "unmoved" tag
                if f"{ccd[0]}r" in tags and "unmoved" in tags:
                    rook_id = item
                    break
            
            if rook_id:
                # 3. Check if path is clear
                path_blocked = False
                for col in side["empty_cols"]:
                    check_x = (col * size) + (size / 2)
                    # Check a small box in the center of the square
                    overlapping = self.canvas.find_overlapping(
                        check_x - 10, k_y - 10, check_x + 10, k_y + 10
                    )
                    
                    for item in overlapping:
                        tags = self.canvas.gettags(item)
                        # If a piece (white or black) is here, path is blocked
                        if any(t.startswith('w') or t.startswith('b') for t in tags):
                            path_blocked = True
                            break
                    if path_blocked: break

                if not path_blocked:
                    # 4. Create the Move Indicator
                    # King moves 2 squares: Current X + (Direction * 2 * Size)
                    dest_x = k_x + (side["dir"] * 2 * size)
                    
                    square = self.canvas.create_rectangle(
                        dest_x - size // 2, k_y - size // 2,
                        dest_x + size // 2, k_y + size // 2,
                        fill="orange", stipple="gray50", width=2
                    )
                    self.spaces_to_move.append(square)

                    # Pass specific arguments to button_clicked to handle the rook
                    # We pass the Rook ID (rID) and the direction (side)
                    self.canvas.tag_bind(square, "<Button-1>", 
                        lambda event, s=square, kid=king_id, rid=rook_id, direction=side["dir"]: 
                        self.button_clicked(event, s, kid, ccd=ccd, size=size, castle_rook_id=rid, castle_dir=direction)
                    )

    def get_potential_moves(self, piece_id, piece_tag, size):
        """Calculates all squares a piece can move to (ignoring check for now)."""
        moves = []
        coords = self.canvas.coords(piece_id)
        start_x, start_y = coords[0], coords[1]
    
        p_type = piece_tag[1]
        p_color = piece_tag[0]
        rules = self.MOVE_RULES[p_type]
    
        # Handle Pawn differently (they have unique move vs capture rules)
        if p_type == 'p':
            dir = -1 if p_color == 'w' else 1
            # Forward moves
            for step in [1, 2] if "unmoved" in self.canvas.gettags(piece_id) else [1]:
                tx, ty = start_x, start_y + (dir * size * step)
                if self.get_piece_at(tx, ty, piece_id): break # Blocked
                moves.append((tx, ty))
            # Diagonal captures
            for dx in [-size, size]:
                tx, ty = start_x + dx, start_y + (dir * size)
                target = self.get_piece_at(tx, ty, piece_id)
                if target and not self.canvas.gettags(target)[0].startswith(p_color):
                    moves.append((tx, ty))
        else:
            # Sliding and Jumping pieces
            vectors = rules['vectors']
            max_steps = 8 if rules['sliding'] else 2
            for vx, vy in vectors:
                for step in range(1, max_steps):
                    tx, ty = start_x + (vx * size * step), start_y + (vy * size * step)
                    if not (0 < tx < size * 8 and 0 < ty < size * 8): break
                
                    target = self.get_piece_at(tx, ty, piece_id)
                    if target:
                        if not self.canvas.gettags(target)[0].startswith(p_color):
                            moves.append((tx, ty)) # Can capture
                        break # Blocked regardless of color
                    moves.append((tx, ty))
        return moves

    def checkmate(self, ccd, size):
        """Checks if the player whose turn it just became is in checkmate."""
        # The opponent is the one who might be mated
        current_color = 'b' if ccd[0] == 'w' else 'w'
    
        # 1. If the king isn't even in check, it can't be checkmate
        if not self.is_king_in_check([current_color, 'k'], size):
            return False

        # 2. Try EVERY move for EVERY piece of the current_color
        all_pieces = self.canvas.find_withtag("pieces")
        for piece in all_pieces:
            tags = self.canvas.gettags(piece)
            if not tags[0].startswith(current_color):
                continue
            
            # Get all squares this piece could theoretically move to
            potential_moves = self.get_potential_moves(piece, tags[0], size)
        
            for move_x, move_y in potential_moves:
                # Simulation: Temporarily move the piece
                orig_coords = self.canvas.coords(piece)
            
                # Check for a piece to "capture" at the destination
                target = self.get_piece_at(move_x, move_y, piece)
                target_state = None
                if target:
                    target_state = self.canvas.itemcget(target, 'state')
                    self.canvas.itemconfig(target, state='hidden')
            
                # Move the piece
                self.canvas.coords(piece, move_x, move_y)
            
                # Is the king STILL in check after this move?
                still_in_check = self.is_king_in_check([current_color, 'k'], size)
            
                # Undo simulation
                self.canvas.coords(piece, orig_coords[0], orig_coords[1])
                if target:
                    self.canvas.itemconfig(target, state=target_state)
            
                # If we found even ONE move that saves the king, it's not mate
                if not still_in_check:
                    return False

        # If no piece had a move that escaped check:
        winner = "White" if ccd[0] == 'w' else "Black"
        print(f"CHECKMATE! {winner} wins!")
        winner = "White" if ccd[0] == 'w' else "Black"
    
        # Trigger the Popup
        self.show_game_over(winner)
        return True

    def get_piece_at(self, x, y, exclude_id):
        """Helper to find if a piece exists at specific coordinates."""
        items = self.canvas.find_overlapping(x-2, y-2, x+2, y+2)
        for item in items:
            tags = self.canvas.gettags(item)
            if any(t.startswith('w') or t.startswith('b') for t in tags) and item != exclude_id:
                return item
        return None

    def is_still_in_check(self, ccd, x, y, item, size):
        # Safety Check: If the item was already removed by collision logic, stop.
        if item not in self.spaces_to_move:
            return

        
        
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

        move_rules = self.MOVE_RULES[self.type_checking_ccd[1]]
        
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
                    self.all_intercepting_coords.extend(current_ray)
        
        if (int(x), int(y)) not in self.all_intercepting_coords:
            # Safely remove specific item
            if item in self.spaces_to_move:
                if self.checkmate(ccd, size):
                    winner = "White" if ccd[0] == "b" else "Black"
                    print(f"{winner} wins")
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
                            self.type_checking = item
                            self.type_checking_ccd = next(t for t in tags if t == f'{enemy_color}p')
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
                                        self.type_checking = item
                                        self.type_checking_ccd = enemy_piece_tag
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

    def button_clicked(self, event, square_id, unique_id, ccd, size, lpi=None, special_flag=False, castle_rook_id=None, castle_dir=None):
        self.check_flag = False
        tags = self.canvas.gettags(unique_id)
        
        curr_coords = self.canvas.coords(unique_id)
        curr_x, curr_y = curr_coords[0], curr_coords[1]
        
        square_coords = self.canvas.coords(square_id)
        dest_x = (square_coords[0] + square_coords[2]) / 2
        dest_y = (square_coords[1] + square_coords[3]) / 2

        # --- 1. Move King ---
        dx = dest_x - curr_x
        dy = dest_y - curr_y
        self.canvas.move(unique_id, dx, dy)

        # --- 2. Handle Castling (Move the Rook) ---
        rook_start_coords = None
        rook_dx = 0
        if castle_rook_id:
            rook_start_coords = self.canvas.coords(castle_rook_id)
            # The rook needs to end up on the OTHER side of the King
            # If King moved Right (+2), Rook ends at King X - 1
            # If King moved Left (-2), Rook ends at King X + 1
            rook_dest_x = dest_x - (castle_dir * size)
            
            rook_dx = rook_dest_x - rook_start_coords[0]
            # Move Rook
            self.canvas.move(castle_rook_id, rook_dx, 0)

        # --- 3. Handle Capture (Hide piece for check validation) ---
        captured_piece_state = None
        if special_flag and lpi:
            captured_piece_state = self.canvas.itemcget(lpi, 'state')
            self.canvas.itemconfig(lpi, state='hidden')

        # --- 4. Validate Move (Is King in Check?) ---
        if self.is_king_in_check(ccd=ccd, size=size):
            # ILLEGAL: Undo everything
            self.canvas.move(unique_id, -dx, -dy) # Undo King
            if castle_rook_id:
                self.canvas.move(castle_rook_id, -rook_dx, 0) # Undo Rook
            if lpi:
                self.canvas.itemconfig(lpi, state=captured_piece_state) # Undo Capture
            print("Move illegal: King remains in check")
        else:
            # LEGAL: Finalize
            
            # Remove "unmoved" tag from King
            if "unmoved" in tags:
                self.canvas.dtag(unique_id, "unmoved")
            
            # Remove "unmoved" tag from Rook if castled
            if castle_rook_id:
                self.canvas.dtag(castle_rook_id, "unmoved")

            if lpi:
                self.canvas.delete(lpi)
            
            self.move_count += 1
            self.remove_spaces()
            self.checkmate(ccd, size)

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

            if ccd[1] == 'k':
                print("Works")
                self.can_castle(ccd, square_size)

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