# logic/ai_logic.py
import random

class ChessAI:
    # กำหนดมูลค่าให้หมากแต่ละตัว เพื่อให้ AI รู้ว่าควรหวงตัวไหน หรือควรเล็งกินตัวไหน
    PIECE_VALUES = {
        'pawn': 10,
        'knight': 30,
        'bishop': 30,
        'rook': 50,
        'queen': 90,
        'king': 900
    }

    @staticmethod
    def get_piece_value(piece):
        if not piece:
            return 0
        piece_name = piece.__class__.__name__.lower()
        return ChessAI.PIECE_VALUES.get(piece_name, 10) # ถ้าเป็นตัวละครใหม่ในอนาคต จะมีค่าพื้นฐานที่ 10

    @staticmethod
    def get_best_move(board_obj, ai_color='black'):
        """
        AI แบบปรับตัวได้: 
        1. หาตาเดินทั้งหมดที่เป็นไปได้
        2. ให้คะแนนตาเดินนั้น (ถ้ากินหมากศัตรูได้ จะได้คะแนนเยอะ)
        3. สุ่มเลือกจากตาเดินที่ได้คะแนนสูงสุด
        """
        best_moves = []
        highest_score = -9999

        # ดึงตาเดินที่ถูกกฎทั้งหมดของ AI
        all_legal_moves = []
        for r in range(8):
            for c in range(8):
                piece = board_obj.board[r][c]
                if piece and piece.color == ai_color:
                    moves = board_obj.get_legal_moves((r, c))
                    for move in moves:
                        all_legal_moves.append(((r, c), move))

        if not all_legal_moves:
            return None # จนมุม หรือเดินไม่ได้แล้ว

        # ประเมินคะแนนแต่ละตาเดิน
        for start_pos, end_pos in all_legal_moves:
            sr, sc = start_pos
            er, ec = end_pos
            
            score = 0
            target_piece = board_obj.board[er][ec]
            
            # 1. ถ้าตาเดินนี้กินหมากศัตรูได้ ให้คะแนนตามมูลค่าหมากศัตรู
            if target_piece and target_piece.color != ai_color:
                score += ChessAI.get_piece_value(target_piece)
            
            # 2. ให้โบนัสเล็กน้อยถ้าเดินไปคุมพื้นที่ตรงกลางกระดาน (แถว 3-4, คอลัมน์ 3-4)
            if 3 <= er <= 4 and 3 <= ec <= 4:
                score += 2

            # เก็บตาเดินที่คะแนนดีที่สุดไว้
            if score > highest_score:
                highest_score = score
                best_moves = [(start_pos, end_pos)]
            elif score == highest_score:
                best_moves.append((start_pos, end_pos))

        # สุ่มเลือก 1 ตาเดินจากกลุ่มที่คะแนนดีที่สุด (เพื่อไม่ให้ AI เดินซ้ำซากจำเจ)
        return random.choice(best_moves)