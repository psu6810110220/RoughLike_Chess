from logic.board import ChessBoard # ดึงกฎหมากรุกคลาสสิกมาทั้งหมด

class ForestMap(ChessBoard):
    def __init__(self):
        super().__init__()
        # กำหนดรูปภาพประจำด่านนี้ไว้ที่นี่เลย UI จะได้ดึงไปใช้ง่ายๆ
        self.bg_image = 'assets/boards/forest.png' 

    def apply_map_effects(self):
        # ✨ ใส่โค้ดพิเศษเฉพาะด่านป่าตรงนี้
        # เช่น สุ่มให้หมากสีเขียวได้เกราะป้องกัน
        print("เอฟเฟกต์ป่าอาถรรพ์ทำงาน!")