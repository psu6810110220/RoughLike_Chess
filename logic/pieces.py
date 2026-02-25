# logic/pieces.py

class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.points = 0
        self.has_moved = False

    def is_path_clear(self, start, end, board):
        sr, sc, er, ec = start[0], start[1], end[0], end[1]
        step_r = 0 if sr == er else (1 if er > sr else -1)
        step_c = 0 if sc == ec else (1 if ec > sc else -1)
        
        # เริ่มเช็คจากช่องถัดไป
        cr, cc = sr + step_r, sc + step_c
        
        while (cr, cc) != (er, ec):
            if board[cr][cc] is not None: 
                return False
            # 🚨 ตรงนี้คือจุดที่แก้บั๊กเกมค้างครับ สั่งให้มันขยับช่องถัดไปเรื่อยๆ!
            cr += step_r
            cc += step_c
            
        return True

class Rook(Piece):
    def __init__(self, color): 
        super().__init__(color, 'R' if color == 'white' else 'r')
        self.points = 3
        self.flip_count = 3
        
    def is_valid_move(self, start, end, board):
        if start[0] == end[0] or start[1] == end[1]: 
            return self.is_path_clear(start, end, board)
        return False

class Knight(Piece):
    def __init__(self, color): 
        super().__init__(color, 'N' if color == 'white' else 'n')
        self.points = 2
        self.flip_count = 3
        
    def is_valid_move(self, start, end, board):
        rd, cd = abs(start[0]-end[0]), abs(start[1]-end[1])
        return (rd == 2 and cd == 1) or (rd == 1 and cd == 2)

class Bishop(Piece):
    def __init__(self, color): 
        super().__init__(color, 'B' if color == 'white' else 'b')
        self.points = 3
        self.flip_count = 2
        
    def is_valid_move(self, start, end, board):
        if abs(start[0]-end[0]) == abs(start[1]-end[1]): 
            return self.is_path_clear(start, end, board)
        return False

class Queen(Piece):
    def __init__(self, color): 
        super().__init__(color, 'Q' if color == 'white' else 'q')
        self.points = 1
        self.flip_count = 7
        
    def is_valid_move(self, start, end, board):
        return Rook(self.color).is_valid_move(start, end, board) or Bishop(self.color).is_valid_move(start, end, board)

class King(Piece):
    def __init__(self, color): 
        super().__init__(color, 'K' if color == 'white' else 'k')
        self.points = 2
        self.flip_count = 2
        
    def is_valid_move(self, start, end, board):
        return max(abs(start[0]-end[0]), abs(start[1]-end[1])) == 1

class Pawn(Piece):
    def __init__(self, color): 
        super().__init__(color, 'P' if color == 'white' else 'p')
        self.points = 2
        self.flip_count = 2
        
    def is_valid_move(self, start, end, board, ep_target=None):
        sr, sc, er, ec = start[0], start[1], end[0], end[1]
        dir = -1 if self.color == 'white' else 1
        target = board[er][ec]
        
        # เดินตรง 1 ช่อง
        if sc == ec and er == sr + dir and not target: 
            return True
        # เดินตรง 2 ช่องจากจุดเริ่มต้น
        if sc == ec and sr == (6 if self.color == 'white' else 1) and er == sr + 2*dir and not target and not board[sr+dir][sc]: 
            return True
        # กินเฉียง
        if abs(sc - ec) == 1 and er == sr + dir and target: 
            return True
        # กิน En Passant
        if ep_target and (er, ec) == ep_target and abs(sc - ec) == 1 and er == sr + dir: 
            return True
            
        return False