# logic/pieces.py
import random
from components.passive.passive_manager import PassiveManager
from components.hidden_passive import HiddenPassive

class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.item = None
        self.has_moved = False
        
        # ระบบ Passive แฝง
        self.hidden_passive = HiddenPassive()
        default_points, default_coins = 5, 3
        self.base_points, self.coins = self.hidden_passive.apply_passive(default_points, default_coins)

    def is_path_clear(self, start, end, board):
        sr, sc, er, ec = start[0], start[1], end[0], end[1]
        step_r = 0 if sr == er else (1 if er > sr else -1)
        step_c = 0 if sc == ec else (1 if ec > sc else -1)
        
        cr, cc = sr + step_r, sc + step_c
        while (cr, cc) != (er, ec):
            if board[cr][cc] is not None: 
                return False
            cr += step_r
            cc += step_c
        return True

    def check_knight_move(self, start, end):
        """Helper สำหรับไอเทม Pegasus Boots (ID 9)"""
        rd, cd = abs(start[0]-end[0]), abs(start[1]-end[1])
        return (rd == 2 and cd == 1) or (rd == 1 and cd == 2)

class Rook(Piece):
    def __init__(self, color, tribe='medieval'): 
        super().__init__(color, 'R' if color == 'white' else 'r')
        self.tribe = tribe
        passive = PassiveManager.get_passive_handler('rook', tribe)
        stats = passive['get_piece_stats']() if passive else {'dice': 0, 'coins': 0}
        self.base_points, self.coins = self.hidden_passive.apply_passive(stats['dice'], stats['coins'])
        self.max_stats = 12
        
    def is_valid_move(self, start, end, board):
        if start == end: return False
        # Item 9: ให้เดินแบบม้าได้
        if getattr(self, 'item', None) and self.item.id == 9:
            if self.check_knight_move(start, end): return True
            
        if start[0] == end[0] or start[1] == end[1]: 
            return self.is_path_clear(start, end, board)
        return False

class Knight(Piece):
    def __init__(self, color, tribe='medieval'): 
        super().__init__(color, 'N' if color == 'white' else 'n')
        self.tribe = tribe
        passive = PassiveManager.get_passive_handler('knight', tribe)
        stats = passive['get_piece_stats']() if passive else {'dice': 0, 'coins': 0}
        self.base_points, self.coins = self.hidden_passive.apply_passive(stats['dice'], stats['coins'])
        self.max_stats = 12
        
    def is_valid_move(self, start, end, board):
        if start == end: return False
        if self.check_knight_move(start, end):
            target = board[end[0]][end[1]]
            return target is None or target.color != self.color
        return False

class Bishop(Piece):
    def __init__(self, color, tribe='medieval'): 
        super().__init__(color, 'B' if color == 'white' else 'b')
        self.tribe = tribe
        passive = PassiveManager.get_passive_handler('bishop', tribe)
        stats = passive['get_piece_stats']() if passive else {'dice': 0, 'coins': 0}
        self.base_points, self.coins = self.hidden_passive.apply_passive(stats['dice'], stats['coins'])
        self.max_stats = 12
        
    def is_valid_move(self, start, end, board):
        if start == end: return False
        if getattr(self, 'item', None) and self.item.id == 9:
            if self.check_knight_move(start, end): return True
            
        if abs(start[0]-end[0]) == abs(start[1]-end[1]): 
            return self.is_path_clear(start, end, board)
        return False

class Queen(Piece):
    def __init__(self, color, tribe='medieval'): 
        super().__init__(color, 'Q' if color == 'white' else 'q')
        self.tribe = tribe
        passive = PassiveManager.get_passive_handler('queen', tribe)
        stats = passive['get_piece_stats']() if passive else {'dice': 0, 'coins': 0}
        self.base_points, self.coins = self.hidden_passive.apply_passive(stats['dice'], stats['coins'])
        self.max_stats = 12
        
    def is_valid_move(self, start, end, board):
        if start == end: return False
        # FIX: แก้บัค Queen วาร์ป (Item 9 ให้เดินแบบม้าได้ ไม่ใช่ teleport)
        if getattr(self, 'item', None) and self.item.id == 9:
            if self.check_knight_move(start, end): return True

        # เช็คการเดินแนวตรง (Rook)
        if start[0] == end[0] or start[1] == end[1]:
            return self.is_path_clear(start, end, board)
        # เช็คการเดินแนวทแยง (Bishop)
        if abs(start[0]-end[0]) == abs(start[1]-end[1]):
            return self.is_path_clear(start, end, board)
        return False

class King(Piece):
    def __init__(self, color, tribe='medieval'): 
        super().__init__(color, 'K' if color == 'white' else 'k')
        self.tribe = tribe
        passive = PassiveManager.get_passive_handler('king', tribe)
        stats = passive['get_piece_stats']() if passive else {'dice': 0, 'coins': 0}
        self.base_points, self.coins = self.hidden_passive.apply_passive(stats['dice'], stats['coins'])
        self.max_stats = 12
        
    def is_valid_move(self, start, end, board):
        if start == end: return False
        if getattr(self, 'item', None) and self.item.id == 9:
            if self.check_knight_move(start, end): return True
        return max(abs(start[0]-end[0]), abs(start[1]-end[1])) == 1

class Pawn(Piece):
    def __init__(self, color, tribe='medieval'): 
        super().__init__(color, 'P' if color == 'white' else 'p')
        self.tribe = tribe
        passive = PassiveManager.get_passive_handler('pawn', tribe)
        stats = passive['get_piece_stats']() if passive else {'dice': 0, 'coins': 0}
        self.base_points, self.coins = self.hidden_passive.apply_passive(stats['dice'], stats['coins'])
        self.max_stats = 12
        self.variant = random.randint(6, 9)
        
    def is_valid_move(self, start, end, board, ep_target=None):
        if start == end: return False
        if getattr(self, 'item', None) and self.item.id == 9:
            if self.check_knight_move(start, end): return True
            
        sr, sc, er, ec = start[0], start[1], end[0], end[1]
        dir = -1 if self.color == 'white' else 1
        target = board[er][ec]
        
        # เดินตรง 1 ช่อง
        if sc == ec and er == sr + dir and not target: return True
        # เดินตรง 2 ช่องจากจุดเริ่มต้น
        if sc == ec and sr == (6 if self.color == 'white' else 1) and er == sr + 2*dir and not target and not board[sr+dir][sc]: return True
        # กินเฉียง
        if abs(sc - ec) == 1 and er == sr + dir and target: return True
        # กิน En Passant
        if ep_target and (er, ec) == ep_target and abs(sc - ec) == 1 and er == sr + dir: return True
        return False

class Obstacle(Piece):
    def __init__(self, name, lifespan):
        self.color = 'neutral'
        self.name = name
        self.item = None
        self.lifespan = lifespan
        self.base_points = 0
        self.coins = 0
        self.has_moved = False
    def is_valid_move(self, start, end, board):
        return False