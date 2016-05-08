class ChessModel(object):
    SAFE_ZONE = 0
    DANGER_ZONE = 1

    ROOK = 2
    KNIGHT = 3
    KING = 4
    QUEEN = 5
    BISHOP = 6


    def bishop_danger_zones(self, table, origin_x, origin_y):
        """
        Finds bishop's threating tiles

        Args:
            table (List): Source table to find threats
            origin_x (int): x position of piece
            origin_y (int): x position of piece
        """

        possible_x = range(-self.x_size, self.x_size)
        possible_y = range(-self.y_size, self.y_size)

        for x_pos in possible_x:
            for y_pos in possible_y:
                if abs(x_pos) == abs(y_pos):
                    target_x = origin_x + x_pos
                    target_y = origin_y + y_pos

                    if not (origin_x == target_x and origin_y == target_y): #dont try to eat yourself
                        if target_y in range_y and target_x in range_x:
                            if table[target_x][target_y] in (self.SAFE_ZONE, DANGER_ZONE):
                                table[target_x][target_y] = DANGER_ZONE
                            else:
                                return False
        return table

    def rook_danger_zones(self, table, origin_x, origin_y):
        """
        Finds Rook's threating tiles

        Args:
            table (List): Source table to find threats
            origin_x (int): x position of piece
            origin_y (int): x position of piece
        """

        for target_x in range(0, self.x_size):
            if target_x != origin_x:
                if table[target_x][origin_y] == self.SAFE_ZONE or table[target_x][origin_y] == self.DANGER_ZONE:
                    table[target_x][origin_y] = self.DANGER_ZONE
                else:
                    return False

        for target_y in range(0, self.y_size):
            if target_y != origin_y:
                if table[origin_x][target_y] == self.SAFE_ZONE or table[origin_x][target_y] == self.DANGER_ZONE:
                    table[origin_x][target_y] = self.DANGER_ZONE
                else:
                    return False

        return table

    def king_danger_zones(self, table, origin_x, origin_y):
        """
        Finds King's threating tiles

        Args:
            table (List): Source table to find threats
            origin_x (int): x position of piece
            origin_y (int): x position of piece
        """

        older_thread = False
        for x_pos in [-1, 0, 1]:
            for y_pos in [-1, 0, 1]:
                target_y = origin_y + y_pos
                target_x = origin_x + x_pos

                if not (origin_x == target_x and origin_y == target_y): #because its like suicide
                    if target_y in range_y and target_x in range_x:
                        if table[target_x][target_y] in (self.SAFE_ZONE, self.DANGER_ZONE):
                            table[target_x][target_y] = self.DANGER_ZONE
                        else:
                            older_thread = True

        if older_thread:
            return False
        else:
            return table

    def knight_danger_zones(self, table, origin_x, origin_y):
        """
        Finds Knight's threating tiles

        Args:
            table (List): Source table to find threats
            origin_x (int): x position of piece
            origin_y (int): x position of piece
        """

        older_thread = False
        all_possible_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1],
                              [1, 2], [1, -2], [-1, 2], [-1, -2]]

        for move in all_possible_moves:
            target_x = origin_x + move[0]
            target_y = origin_y + move[1]

            if not (origin_x == target_x and origin_y == target_y): #suicide again
                if target_y in self.range_y and target_x in self.range_x:
                    if (table[target_x][target_y] == self.SAFE_ZONE
                            or table[target_x][target_y] == self.DANGER_ZONE):
                        table[target_x][target_y] = self.DANGER_ZONE
                    else:
                        older_thread = True

        if older_thread:
            return False
        else:
            return table

    def fill_danger_zones(self, table, piece, line):
        """
        Marks tiles that threatening by current piece as DANGER_ZONE.
        Returns False if position threating an already positioned piece.
        Converts table to 2D List and after calculations converts it again to 1D for
        ease of code.

        Args:
            table (List): Source table to find place
            piece (int): Kind of piece (ROOK,QUEEN etc.)
            line (int): Where to put current piece
        """

        table2d = [[0 for x_pos in range(self.x_size)] for y_pos in range(self.y_size)]
        index1d = 0
        for x_pos in range(0, self.x_size):
            for y_pos in range(0, self.y_size):
                if table[index1d] != 0:
                    table2d[x_pos][y_pos] = table[index1d]

                if index1d == line:
                    origin_x = x_pos
                    origin_y = y_pos
                index1d += 1

        if piece == self.ROOK:
            table2d = self.rook_danger_zones(table2d, origin_x, origin_y)

        elif piece == self.BISHOP:
            table2d = self.bishop_danger_zones(table2d, origin_x, origin_y)

        elif piece == self.QUEEN:
            table2d = self.bishop_danger_zones(table2d, origin_x, origin_y)
            if table2d:
                table2d = self.rook_danger_zones(table2d, origin_x, origin_y)

        elif piece == self.KING:
            table2d = self.king_danger_zones(table2d, origin_x, origin_y)

        elif piece == self.KNIGHT:
            table2d = self.knight_danger_zones(table2d, origin_x, origin_y)

        if not table2d:
            return False
        else:
            #take table back to 1Dimensional space
            index1d = 0
            for x_pos in range(0, self.x_size):
                for y_pos in range(0, self.y_size):
                    table[index1d] = table2d[x_pos][y_pos]
                    index1d += 1

            return table
