# logic/history_logic.py
import copy

class HistoryManager:
    def __init__(self):
        self.state_history = []
        self.move_text_history = []

    @staticmethod
    def get_algebraic(r, c):
        cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
        return cols[c] + ranks[r]

    def generate_move_text(self, piece, sr, sc, er, ec, is_capture, is_castle):
        if is_castle: return "O-O" if ec > sc else "O-O-O"
        p_sym = "" if piece.__class__.__name__.lower() == 'pawn' else piece.name.upper()
        c_sym = "x" if is_capture else ""
        if piece.__class__.__name__.lower() == 'pawn' and is_capture:
            p_sym = self.get_algebraic(sr, sc)[0]
        return f"{p_sym}{c_sym}{self.get_algebraic(er, ec)}"

    def save_state(self, board_obj, move_text):
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
        if not self.state_history: return None
        self.move_text_history.pop()
        return self.state_history.pop()
        
    def add_suffix_to_last_move(self, suffix):
        if self.move_text_history: self.move_text_history[-1] += suffix