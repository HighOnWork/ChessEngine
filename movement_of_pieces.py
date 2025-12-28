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
        self.BLACK_PAWN_MOVE = [False] * 7

    def black_pawn_selector(self, ID, i):
        if ID == 49:
            if self.BLACK_PAWN_MOVE[0] and i == 1:
                return True
        elif ID == 50:
            if self.BLACK_PAWN_MOVE[1] and i ==1:
                return True

    def button_click(self, event, pawn_item_id, rectangles):
        self.canvas.move(pawn_item_id, 0, 125)
        for rec in rectangles:
            self.canvas.itemconfigure(rec, state='hidden')
        self.canvas.tag_unbind(self.current_event_tag1, '<Button-1>')
        self.current_event_tag1 = None
        if pawn_item_id == 49:
            self.BLACK_PAWN_MOVE[0] = True

    def pawn_button_click_first_time_second_way(self, event, pawn_item_id, rectangles):
        if pawn_item_id == 49:
            if self.BLACK_PAWN_MOVE[0] == False:
                self.canvas.move(pawn_item_id, 0, 125 * 2)
                for rec in rectangles:
                    self.canvas.itemconfigure(rec, state='hidden')
                self.canvas.tag_unbind(self.current_event_tag2, "<Button-1>")
                self.current_event_tag2 = None
                self.BLACK_PAWN_MOVE[0] = True

    def black_pawns_movement(self, event, pawn_item_id):
        
        coords = self.canvas.coords(pawn_item_id)
        print(coords)

        current_pawn_x = coords[0]
        current_pawn_y = coords[1]

        print(pawn_item_id)

        if self.first_turn_done:
            if current_pawn_y <= 900:

                spaces_to_move = []

                X1, Y1 = current_pawn_x - 127 // 2, (current_pawn_y - 130 // 2) + self.SIDE_LENGTH
                X2, Y2 = X1 + self.SIDE_LENGTH, Y1 + self.SIDE_LENGTH

                # if current_pawn_y <= 900:
                for i in range(2):
                                
                        if self.black_pawn_selector(ID=pawn_item_id, i=i):
                            continue
            
                        spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))
                        Y1 += 125
                        Y2 += 125
                    # tk.Misc.lift(spaces_to_move[i])
                # else:
                #     spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))
                
                if len(spaces_to_move) > 0 :
                    self.current_event_tag1 = spaces_to_move[0]
                    self.canvas.tag_bind(self.current_event_tag1, "<Button-1>", lambda event: self.button_click(event=event, pawn_item_id=pawn_item_id, rectangles=spaces_to_move))

                if len(spaces_to_move) > 1:
                    self.current_event_tag2 = spaces_to_move[1]
                    self.canvas.tag_bind(self.current_event_tag2, "<Button-1>", lambda event: self.pawn_button_click_first_time_second_way(event=event, pawn_item_id=pawn_item_id, rectangles=spaces_to_move))

    
    def white_pawns_movement(self, event, pawn_y_position, pawn_x_position):
        spaces_to_move = []

        X1, Y1 = (pawn_x_position - 125 // 2) - 1, (pawn_y_position - 125 - (120 // 2)) - self.SIDE_LENGTH
        X2, Y2 = X1 + self.SIDE_LENGTH, Y1 + self.SIDE_LENGTH

        if pawn_y_position >= (1000 - 190):
            for _ in range(2):
                spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))
                Y1 += 125
                Y2 += 125
        else:
            spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))

        for spaces in spaces_to_move:
            self.canvas.tag_bind(spaces, "<Button-1>", self.button_click)
        
        self.first_turn_done = True
        