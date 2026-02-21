# ไฟล์: history_manager.py
import copy

class HistoryManager:
    def __init__(self):
        self.state_history = []
        self.move_text_history = []

    @staticmethod
    def get_algebraic(r, c):
        """แปลพิกัดอาร์เรย์ (0,0) เป็นภาษาหมากรุกสากล (a8)"""
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
        return cols[c] + ranks[r]

    def generate_move_text(self, piece, sr, sc, er, ec, is_capture, is_castle):
        """สร้างข้อความประวัติการเดิน (Chess Notation)"""
        if is_castle:
            return "O-O" if ec > sc else "O-O-O"
            
        p_sym = "" if piece.__class__.__name__.lower() == 'pawn' else piece.name.upper()
        c_sym = "x" if is_capture else ""
        
        # เบี้ยกินต้องบอกว่ามาจากคอลัมน์ไหน (เช่น exd5)
        if piece.__class__.__name__.lower() == 'pawn' and is_capture:
            p_sym = self.get_algebraic(sr, sc)[0]
            
        return f"{p_sym}{c_sym}{self.get_algebraic(er, ec)}"

    def save_state(self, board_obj, move_text):
        """สำรองข้อมูลกระดาน (Snapshot) เก็บลง Stack"""
        state = {
            'board': copy.deepcopy(board_obj.board),
            'current_turn': board_obj.current_turn,
            'last_move': board_obj.last_move,
            'en_passant_target': board_obj.en_passant_target,
            'game_result': board_obj.game_result
        }
        self.state_history.append(state)
        self.move_text_history.append(move_text)

    def pop_state(self):
        """ดึงข้อมูล Snapshot ล่าสุดออกมาเพื่อย้อนกลับ (Undo)"""
        if not self.state_history:
            return None
        self.move_text_history.pop()
        return self.state_history.pop()
        
    def add_suffix_to_last_move(self, suffix):
        """เติมสัญลักษณ์รุก (+) หรือ รุกฆาต (#) ท้ายข้อความ"""
        if self.move_text_history:
            self.move_text_history[-1] += suffix