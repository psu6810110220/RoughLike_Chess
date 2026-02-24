# components/chess_square.py
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Line

class ChessSquare(Button):
    def __init__(self, row, col, **kwargs):
        super().__init__(**kwargs)
        self.row, self.col = row, col
        
        # ปิดการแสดงสีพื้นหลังแบบปุ่มปกติของ Kivy ทิ้งไป
        self.background_normal = '' 
        self.background_down = ''
        
        # เตรียมตัวแสดงรูปหมาก
        self.piece_img = Image(allow_stretch=True, keep_ratio=True, opacity=0)
        self.add_widget(self.piece_img)
        
        self.is_last_move = False
        self.is_legal = False
        
        # ตั้งค่าสีเริ่มต้น (จะกลายเป็นช่องใส)
        self.update_square_style()
        
        self.bind(pos=self.sync_layout, size=self.sync_layout)

    def sync_layout(self, *args):
        """จัดตำแหน่งรูปหมากและวาดเส้นขอบนีออน (Neon UI)"""
        self.piece_img.size = (self.width * 0.85, self.height * 0.85)
        self.piece_img.center = self.center
        
        self.canvas.after.clear()
        with self.canvas.after:
            if self.is_legal:
                Color(0.1, 1, 0.1, 1) 
                Line(rectangle=(self.x + 1, self.y + 1, self.width - 2, self.height - 2), width=3)
            elif self.is_last_move:
                Color(1, 0.5, 0, 1) 
                Line(rectangle=(self.x, self.y, self.width, self.height), width=2.5)

    def update_square_style(self, highlight=False, is_legal=False, is_check=False, is_last=False):
        """อัปเดตสีพื้นหลังและสถานะของช่อง"""
        self.is_last_move = is_last
        self.is_legal = is_legal
        
        # ✨ จุดสำคัญ: เปลี่ยนสีพื้นหลังปกติให้เป็น "สีใส" (Alpha = 0)
        if is_check: 
            self.background_color = (1, 0.2, 0.2, 0.8) # ราชาโดนรุก (แดงโปร่งแสง)
        elif highlight: 
            self.background_color = (1, 1, 0, 0.6) # เลือกหมาก (เหลืองโปร่งแสง)
        else:
            # ไม่ได้เลือกอะไรเลย ให้โปร่งใส 100% เพื่อโชว์รูปภาพพื้นหลังด่าน
            self.background_color = (0, 0, 0, 0) 
            
        self.sync_layout()

    def set_piece_icon(self, path):
        """แสดงรูปภาพหมากตาม Path ที่ส่งมา"""
        if path:
            self.piece_img.source = path
            self.piece_img.opacity = 1
        else: 
            self.piece_img.opacity = 0