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
        try:
            app = App.get_running_app()
            difficulty = getattr(app, 'ai_difficulty', 'normal')
        except:
            difficulty = 'normal'

        best_moves = []
        highest_score = -9999
        enemy_color = 'white' if ai_color == 'black' else 'black'

        # ดึงตาเดินที่ถูกกฎทั้งหมด
        all_legal_moves = []
        for r in range(8):
            for c in range(8):
                piece = board_obj.board[r][c]
                if piece and piece.color == ai_color:
                    moves = board_obj.get_legal_moves((r, c))
                    for move in moves:
                        all_legal_moves.append(((r, c), move))

        if not all_legal_moves:
            return None

        # 🟢 ระดับ EASY: มีโอกาส 50% ที่จะเดินมั่วๆ (เพื่อจำลองการเดินพลาด/ไม่ได้คิด)
        if difficulty == 'easy':
            import random
            if random.random() < 0.5:
                return random.choice(all_legal_moves)

        for start_pos, end_pos in all_legal_moves:
            sr, sc = start_pos
            er, ec = end_pos
            
            score = 0
            target_piece = board_obj.board[er][ec]
            our_piece = board_obj.board[sr][sc]
            
            # 1. คะแนนพื้นฐาน: เล็งกินหมากศัตรู
            if target_piece and target_piece.color != ai_color:
                score += ChessAI.get_piece_value(target_piece) * 10
            
            # 2. คะแนนโบนัส: เดินไปคุมพื้นที่ตรงกลางกระดาน
            if 3 <= er <= 4 and 3 <= ec <= 4:
                score += 5

            # 🔴 ระดับ HARD: คิดหน้าคิดหลัง และการหนีตายแบบขั้นสุด
            if difficulty == 'hard':
                # ประเมินว่าตำแหน่งที่ยืนอยู่ปัจจุบันกำลังจะโดนกินไหม (ถ้าหนีได้ให้คะแนนโบนัสหนีตาย)
                is_currently_safe = True
                for rr in range(8):
                    for cc in range(8):
                        ep = board_obj.board[rr][cc]
                        if ep and ep.color == enemy_color and ep.is_valid_move((rr, cc), (sr, sc), board_obj.board):
                            is_currently_safe = False
                            break
                    if not is_currently_safe: break
                
                if not is_currently_safe:
                    score += ChessAI.get_piece_value(our_piece) * 5 # โบนัสหนีตาย ยิ่งตัวแพงยิ่งต้องหนี

                # จำลองการเดินชั่วคราว เพื่อดูว่าเดินไปแล้วจะโดนกินไหม
                board_obj.board[sr][sc] = None
                board_obj.board[er][ec] = our_piece
                
                is_safe = True
                for rr in range(8):
                    for cc in range(8):
                        epiece = board_obj.board[rr][cc]
                        if epiece and epiece.color == enemy_color:
                            if epiece.is_valid_move((rr, cc), (er, ec), board_obj.board):
                                is_safe = False
                                break
                    if not is_safe: break
                
                board_obj.board[er][ec] = target_piece
                board_obj.board[sr][sc] = our_piece
                
                if not is_safe:
                    score -= ChessAI.get_piece_value(our_piece) * 15 # หักคะแนนหนักมาก ห้ามเดินไปแจกฟรี
                else:
                    score += 10 # โบนัสเลือกตาเดินที่ปลอดภัย

            # 🟢 ระดับ EASY (ในกรณีที่ไม่สุ่มในตอนแรก): สุ่มแกว่งคะแนนให้รวนๆ (เพื่อให้บางทีเมินตัวกินฟรี)
            if difficulty == 'easy':
                import random
                score += random.randint(-30, 30)

            # เก็บตาเดินที่คะแนนดีที่สุดไว้
            if score > highest_score:
                highest_score = score
                best_moves = [(start_pos, end_pos)]
            elif score == highest_score:
                best_moves.append((start_pos, end_pos))

        import random
        return random.choice(best_moves) if best_moves else random.choice(all_legal_moves)