class movement_of_indivisual_pieces:
    def __init__(self, canvas):
        self.first_turn_done = False
        self.canvas = canvas
        # self.X1, self.Y1 = 0, 250
        self.SIDE_LENGTH = 125
        # self.X2, self.Y2 = self.X1 + self.SIDE_LENGTH, self.Y1 + self.SIDE_LENGTH
    
    def button_click(self, event):
        print("Button Clicked")

    def black_pawns_movement(self, event, pawn_y_position, pawn_x_position):

        if self.first_turn_done:

            spaces_to_move = []

            X1, Y1 = pawn_x_position - 127 // 2, (pawn_y_position - 130 // 2) + self.SIDE_LENGTH
            X2, Y2 = X1 + self.SIDE_LENGTH, Y1 + self.SIDE_LENGTH

            if pawn_y_position <= 190:
                for _ in range(2):
                    spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))
                    Y1 += 125
                    Y2 += 125
            else:
                spaces_to_move.append(self.canvas.create_rectangle(X1, Y1, X2, Y2, fill="orange", width=2))

            for spaces in spaces_to_move:
                self.canvas.tag_bind(spaces, "<Button-1>", self.button_click)
    
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
        