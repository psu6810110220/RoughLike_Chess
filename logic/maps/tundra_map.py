# logic/maps/tundra_map.py
from logic.board import ChessBoard

class TundraMap(ChessBoard):
    def __init__(self):
        super().__init__()
        # ✨ ดึงรูปภาพทุ่งน้ำแข็งมาเป็นพื้นหลัง
        self.bg_image = 'assets/boards/tundra.png'
        
        # (กติกาพิเศษของด่านน้ำแข็ง เช่น พื้นลื่น จะเอามาใส่ตรงนี้ทีหลัง)ห