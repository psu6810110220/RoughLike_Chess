# logic/ai_logic.py
import random
from kivy.app import App # นำเข้า App เพื่อดึงค่าระดับความยากจากหน้า Options

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
        return ChessAI.PIECE_VALUES.get(piece_name, 10)

    @staticmethod
    def get_best_move(board_obj, ai_color='black'):
        # 1. ดึงค่าระดับความยากปัจจุบันจากตัวเกมหลัก
        try:
            app = App.get_running_app()
            difficulty = getattr(app, 'ai_difficulty', 'normal')
        except:
            difficulty = 'normal' # ค่าเริ่มต้นกันเหนียว

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

        # 🟢 ระดับ EASY: สุ่มเดินมั่ว 100% ไม่คิดอะไรเลย
        if difficulty == 'easy':
            return random.choice(all_legal_moves)

        # 🟡/🔴 ระดับ NORMAL และ HARD: ประเมินคะแนนแต่ละตาเดิน
        for start_pos, end_pos in all_legal_moves:
            sr, sc = start_pos
            er, ec = end_pos
            
            score = 0
            target_piece = board_obj.board[er][ec]
            our_piece = board_obj.board[sr][sc]
            
            # 1. ถ้าตาเดินนี้กินหมากศัตรูได้ ให้คะแนนตามมูลค่าหมากศัตรู
            if target_piece and target_piece.color != ai_color:
                score += ChessAI.get_piece_value(target_piece)
            
            # 2. ให้โบนัสเล็กน้อยถ้าเดินไปคุมพื้นที่ตรงกลางกระดาน
            if 3 <= er <= 4 and 3 <= ec <= 4:
                score += 2

            # 🔴 ระดับ HARD: คิดล่วงหน้า 1 สเต็ป (ป้องกันการเดินไปแจกฟรี)
            if difficulty == 'hard':
                # จำลองย้ายหมากชั่วคราวไปที่เป้าหมาย
                board_obj.board[sr][sc] = None
                board_obj.board[er][ec] = our_piece
                
                is_safe = True
                enemy_color = 'white' if ai_color == 'black' else 'black'
                
                # สแกนดูว่าตาหน้า ศัตรูสามารถเดินมากินช่องนี้ได้ไหม
                for rr in range(8):
                    for cc in range(8):
                        epiece = board_obj.board[rr][cc]
                        if epiece and epiece.color == enemy_color:
                            if epiece.is_valid_move((rr, cc), (er, ec), board_obj.board):
                                is_safe = False
                                break
                    if not is_safe: break
                
                # ถอยหมากจำลองกลับที่เดิม
                board_obj.board[er][ec] = target_piece
                board_obj.board[sr][sc] = our_piece
                
                # หักคะแนนอย่างหนักถ้าเดินไปแล้วโดนกินฟรี / ให้โบนัสถ้าเป็นช่องปลอดภัย
                if not is_safe:
                    score -= ChessAI.get_piece_value(our_piece) 
                else:
                    score += 3

            # เก็บตาเดินที่คะแนนดีที่สุดไว้
            if score > highest_score:
                highest_score = score
                best_moves = [(start_pos, end_pos)]
            elif score == highest_score:
                best_moves.append((start_pos, end_pos))

        return random.choice(best_moves)