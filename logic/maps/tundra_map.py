# logic/maps/tundra_map.py
import random
from logic.board import ChessBoard

class TundraMap(ChessBoard):
    def __init__(self):
        super().__init__()
        self.bg_image = 'assets/boards/tundra.png'

    def apply_map_effects(self):
        # โอกาส 15% และต้องไม่โดนแช่แข็งซ้อนทับกันอยู่
        if self.freeze_timer <= 0 and random.random() < 0.15:
            # แช่แข็ง 3 เทิร์น
            self.freeze_timer = 3