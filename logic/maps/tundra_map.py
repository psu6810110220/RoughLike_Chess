import random
from logic.board import ChessBoard
from logic.pieces import King

class TundraMap(ChessBoard):
    def __init__(self):
        super().__init__()
        self.bg_image = 'assets/boards/tundra.png'

    def apply_map_effects(self):
        # เช็คว่าบนกระดานมีหมากติดแช่แข็งอยู่แล้วหรือไม่ เพื่อไม่ให้แช่แข็งซ้อนทับกัน
        is_already_frozen = any(getattr(p, 'freeze_timer', 0) > 0 for row in self.board for p in row if p)
        
        # โอกาส 15% ที่จะเกิด Event
        if not is_already_frozen and random.random() < 0.15:
            for r in range(8):
                for c in range(8):
                    p = self.board[r][c]
                    # ✨ แช่แข็งหมากทุกตัวบนกระดาน (ยกเว้น King และสิ่งกีดขวาง)
                    if p and getattr(p, 'color', '') != 'neutral' and not isinstance(p, King):
                        p.freeze_timer = 3  # ยัดสถานะแช่แข็ง 3 เทิร์นใส่ตัวหมาก