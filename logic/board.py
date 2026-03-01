# logic/board.py
import copy 
from logic.pieces import Rook, Knight, Bishop, Queen, King, Pawn, Obstacle # ✨ เพิ่ม Obstacle ต่อท้าย
from logic.history_logic import HistoryManager

class ChessBoard:
    def __init__(self):
        self.board = self.create_initial_board()
        self.current_turn = 'white'
        self.last_move = None
        self.en_passant_target = None 
        self.game_result = None
        self.history = HistoryManager() 
        self.bg_image = '' 
        self.freeze_timer = 0  # ✨ เพิ่มตัวแปรเก็บจำนวนเทิร์นที่ถูกแช่แข็ง
        self.inventory_white = [] # ✨ กระเป๋าฝั่งขาว (สูงสุด 5)
        self.inventory_black = [] # ✨ กระเป๋าฝั่งดำ (สูงสุด 5)

    def handle_item_drop(self, attacker, defender):
        """จัดการการได้รับไอเทมเมื่อมีการกินหมาก"""
        # เงื่อนไข: ต้องเป็น Rook, Bishop หรือ Knight เท่านั้นที่กิน
        valid_harvesters = ['rook', 'bishop', 'knight']
        attacker_type = attacker.__class__.__name__.lower()
        
        if attacker_type in valid_harvesters:
            target_inv = self.inventory_white if attacker.color == 'white' else self.inventory_black
            
            # ถ้ากระเป๋ายังไม่เต็ม (ไม่เกิน 5 ชิ้น)
            if len(target_inv) < 5:
                # โอกาส 40% ที่จะได้รับไอเทมจากการกิน
                if random.random() < 0.40:
                    random_item_id = random.randint(1, 10)
                    item = ITEM_DATABASE[random_item_id]
                    target_inv.append(item)
                    print(f"{attacker.color} received {item.name}!")

    def create_initial_board(self):
        b = [[None for _ in range(8)] for _ in range(8)]
        b[0] = [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')]
        b[1] = [Pawn('black') for _ in range(8)]
        b[6] = [Pawn('white') for _ in range(8)]
        b[7] = [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')]
        return b

    def simulate_move(self, sr, sc, er, ec, color):
        p, t = self.board[sr][sc], self.board[er][ec]
        self.board[sr][sc], self.board[er][ec] = None, p
        check = self.is_in_check(color)
        self.board[sr][sc], self.board[er][ec] = p, t
        return check

    def get_legal_moves(self, pos):
        sr, sc = pos
        piece = self.board[sr][sc]
        if not piece: return []
        
        # ✨ เช็คสถานะแช่แข็งที่ระดับตัวหมาก (ถ้าหมากตัวนี้โดนแช่แข็งอยู่ จะขยับไม่ได้)
        if getattr(piece, 'freeze_timer', 0) > 0:
            return []

        moves = []
        for r in range(8):
            for c in range(8):
                target = self.board[r][c]
                if target and (target.color == piece.color or getattr(target, 'color', '') == 'neutral'): 
                    continue
                
                valid = piece.is_valid_move((sr, sc), (r, c), self.board, self.en_passant_target) if isinstance(piece, Pawn) else piece.is_valid_move((sr, sc), (r, c), self.board)
                if valid and not self.simulate_move(sr, sc, r, c, piece.color):
                    moves.append((r, c))
                    
        if isinstance(piece, King) and not piece.has_moved and not self.is_in_check(piece.color):
            for tc in [2, 6]:
                if self.check_castling_logic(sr, sc, sr, tc): 
                    moves.append((sr, tc))
        return moves

    def check_castling_logic(self, sr, sc, er, ec):
        p = self.board[sr][sc]
        rc = 0 if ec == 2 else 7
        rook = self.board[sr][rc]
        if not rook or not isinstance(rook, Rook) or rook.has_moved: 
            return False
        step = 1 if ec == 6 else -1
        for col in range(sc + step, rc, step):
            if self.board[sr][col]: 
                return False
        for col in [sc + step, sc + 2*step]:
            if self.simulate_move(sr, sc, sr, col, p.color): 
                return False
        return True

    def move_piece(self, sr, sc, er, ec, resolve_crash=False, crash_won=True):
        p = self.board[sr][sc]
        if not p or p.color != self.current_turn or self.game_result: 
            return False
            
        is_castle = isinstance(p, King) and abs(sc-ec) == 2
        is_ep = isinstance(p, Pawn) and (er, ec) == self.en_passant_target
        legal_moves = self.get_legal_moves((sr, sc))
        
        if (er, ec) not in legal_moves: 
            return False
            
        target = self.board[er][ec]
        is_capture = (target is not None) or is_ep

        # ---------------------------------------------------------
        # ✨ ระบบ CRASH (ส่งสัญญาณไปให้ UI เปิดหน้าต่างแทนที่จะทำเอง)
        # ---------------------------------------------------------
        if is_capture and not resolve_crash:
            captured_piece = target if not is_ep else self.board[sr][ec]
            # คืนค่าบอก UI ว่าเกิดการ "crash" พร้อมหมากทั้ง 2 ฝ่าย
            return ("crash", p, captured_piece)
            
        # ✨ ถ้ากลับมาจาก UI พร้อมผลลัพธ์แล้ว
        if is_capture and resolve_crash:
            if crash_won == "died":
                # หมากฝั่งผู้โจมตีถูกทำลาย (Distortion 2 ครั้ง)
                self.board[sr][sc] = None
                self.complete_turn()
                return "died"
            elif not crash_won:
                # ยกเลิกการโจมตี หมากถอยกลับไปช่องเดิม
                return False
        # ---------------------------------------------------------
        
        move_text = self.history.generate_move_text(p, sr, sc, er, ec, is_capture, is_castle)
        self.history.save_state(self, move_text)
        
        if is_ep: 
            self.board[sr][ec] = None 
            
        if is_castle:
            rc, nrc = (0, 3) if ec == 2 else (7, 5)
            self.board[sr][nrc], self.board[sr][rc] = self.board[sr][rc], None
            self.board[sr][nrc].has_moved = True
            
        if isinstance(p, Pawn) and abs(sr - er) == 2: 
            self.en_passant_target = ((sr + er) // 2, sc)
        else: 
            self.en_passant_target = None
            
        self.last_move = ((sr, sc), (er, ec))
        self.board[er][ec], self.board[sr][sc] = p, None
        p.has_moved = True
        
        if isinstance(p, Pawn) and (er == 0 or er == 7): 
            return "promote"
            
        self.complete_turn()
        return True

    def undo_move(self):
        state = self.history.pop_state()
        if not state: return False
        self.board = state['board']
        self.current_turn = state['current_turn']
        self.last_move = state['last_move']
        self.en_passant_target = state['en_passant_target']
        self.game_result = state['game_result']
        return True

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and isinstance(p, King) and p.color == color: 
                    return (r, c)
        return None

    def is_in_check(self, color):
        kp = self.find_king(color)
        if not kp: return False
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color != color and p.is_valid_move((r, c), kp, self.board): 
                    return True
        return False

    def check_insufficient_material(self):
        pieces = []
        for row in self.board:
            for p in row:
                if p: pieces.append(p.__class__.__name__)
        if len(pieces) <= 2: return True 
        if len(pieces) == 3 and ('Bishop' in pieces or 'Knight' in pieces): return True
        return False

    def complete_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        
        self.update_map_events()
        self.apply_map_effects()

        has_moves = False
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color == self.current_turn:
                    if self.get_legal_moves((r, c)): 
                        has_moves = True
                        break
            if has_moves: break
            
        is_check = self.is_in_check(self.current_turn)
        
        if not has_moves:
            # ✨ เช็คว่าเดินไม่ได้เพราะหมากโดนแช่แข็งหรือเปล่า
            is_frozen_locked = any(getattr(p, 'freeze_timer', 0) > 0 for row in self.board for p in row if p and getattr(p, 'color', '') == self.current_turn)
            
            if is_frozen_locked and not is_check:
                # ถ้าเดินไม่ได้เลยเพราะติดแช่แข็ง (และไม่ได้โดนรุก) ให้ข้ามเทิร์นเพื่อลดเวลา
                self.complete_turn()
                return
            elif is_check:
                winner = 'black' if self.current_turn == 'white' else 'white'
                self.game_result = f"CHECKMATE! {winner.upper()} WINS"
                self.history.add_suffix_to_last_move("#") 
            else: 
                self.game_result = "DRAW - STALEMATE" 
        elif self.check_insufficient_material(): 
            self.game_result = "DRAW - INSUFFICIENT MATERIAL"
        elif is_check: 
            self.history.add_suffix_to_last_move("+")

    # ✨ ฟังก์ชันใหม่สำหรับจัดการเวลาของ Event
    def update_map_events(self):
        # ✨ ลดอายุของ Event บนตัวหมากและสิ่งกีดขวาง
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p:
                    # 1. ลดเวลาสิ่งกีดขวาง
                    if getattr(p, 'color', '') == 'neutral':
                        p.lifespan -= 1
                        if p.lifespan <= 0:
                            self.board[r][c] = None 
                    
                    # 2. ลดเวลาแช่แข็งของหมากแต่ละตัว
                    if getattr(p, 'freeze_timer', 0) > 0:
                        p.freeze_timer -= 1

    def apply_map_effects(self):
        pass

    def promote_pawn(self, r, c, cls):
        color = self.board[r][c].color
        self.board[r][c] = cls(color)
        self.history.add_suffix_to_last_move(f"={self.board[r][c].name.upper()}")
        self.complete_turn()