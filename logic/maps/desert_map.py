# logic/maps/desert_map.py
from logic.board import ChessBoard

class DesertMap(ChessBoard):
    def __init__(self):
        super().__init__()
        # ✨ ดึงรูปภาพทะเลทรายมาเป็นพื้นหลัง
        self.bg_image = 'assets/boards/desert.png'
        
        # (เดี๋ยวเราค่อยมาเพิ่มกติกาพิเศษของด่านทะเลทรายตรงนี้ทีหลัง)