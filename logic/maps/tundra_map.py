# logic/maps/tundra_map.py
import random
from logic.board import ChessBoard
from logic.pieces import King

class TundraMap(ChessBoard):
    def __init__(self):
        super().__init__()
        self.bg_image = 'assets/boards/tundra.png'
        self.tundra_turn_count = 0  # ตัวนับเทิร์นของด่าน Tundra

    def apply_map_effects(self):
        # นับเทิร์นเมื่อสลับมาเป็นตาของสีขาว (ความหมายคือ เพิ่งจบเทิร์นของสีดำ = จบ 1 รอบ/เทิร์นเต็ม)
        if self.current_turn == 'white':
            self.tundra_turn_count += 1
            
            # Event จะทำงาน "ทุกๆ 3 เทิร์น"
            if self.tundra_turn_count % 3 == 0:
                white_pieces = []
                black_pieces = []
                
                # รวบรวมหมากที่สามารถแช่แข็งได้ (ไม่ใช่ King, ไม่ใช่สิ่งกีดขวาง, และยังไม่โดนแช่แข็งซ้ำ)
                for r in range(8):
                    for c in range(8):
                        p = self.board[r][c]
                        if p and getattr(p, 'color', '') != 'neutral' and not isinstance(p, King):
                            if getattr(p, 'freeze_timer', 0) <= 0:
                                if p.color == 'white':
                                    white_pieces.append(p)
                                elif p.color == 'black':
                                    black_pieces.append(p)
                                    
                # สุ่ม 2 ตัวจากทีมสีขาวให้ติดแช่แข็ง
                if white_pieces:
                    num_to_freeze = min(2, len(white_pieces))
                    for p in random.sample(white_pieces, num_to_freeze):
                        p.freeze_timer = 6  # ใส่ค่า 6 (เพราะลดทีละ 1 ทุกครั้งที่ใครคนใดคนหนึ่งเดิน 6 ครั้ง = 3 เทิร์นเต็ม)
                        
                # สุ่ม 2 ตัวจากทีมสีดำให้ติดแช่แข็ง
                if black_pieces:
                    num_to_freeze = min(2, len(black_pieces))
                    for p in random.sample(black_pieces, num_to_freeze):
                        p.freeze_timer = 6