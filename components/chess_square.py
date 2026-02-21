# components/chess_square.py
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Line

class ChessSquare(Button):
    def __init__(self, row, col, **kwargs):
        super().__init__(**kwargs)
        self.row, self.col = row, col
        self.background_normal = '' 
        self.background_down = ''
        
        # เตรียมตัวแสดงรูปหมาก
        self.piece_img = Image(allow_stretch=True, keep_ratio=True, opacity=0)
        self.add_widget(self.piece_img)
        
        self.is_last_move = False
        self.is_legal = False
        
        # ตั้งค่าสีเริ่มต้นของช่อง
        self.update_square_style()
        
        # ผูกฟังก์ชันการจัดวางรูปและวาดกราฟิกนีออน
        self.bind(pos=self.sync_layout, size=self.sync_layout)

    def sync_layout(self, *args):
        """จัดตำแหน่งรูปหมากและวาดเส้นขอบนีออน (Neon UI)"""
        # ปรับขนาดรูปหมากให้พอดี (85% ของช่อง)
        self.piece_img.size = (self.width * 0.85, self.height * 0.85)
        self.piece_img.center = self.center
        
        # วาดเส้นขอบ (Neon Effect)
        self.canvas.after.clear()
        with self.canvas.after:
            if self.is_legal:
                # สีเขียวนีออน สำหรับช่องที่เดินได้
                Color(0.1, 1, 0.1, 1) 
                Line(rectangle=(self.x + 1, self.y + 1, self.width - 2, self.height - 2), width=3)
            elif self.is_last_move:
                # สีส้มสด สำหรับตาเดินล่าสุด
                Color(1, 0.5, 0, 1) 
                Line(rectangle=(self.x, self.y, self.width, self.height), width=2.5)

    def update_square_style(self, highlight=False, is_legal=False, is_check=False, is_last=False):
        """อัปเดตสีพื้นหลังและสถานะของช่อง"""
        self.is_last_move = is_last
        self.is_legal = is_legal
        
        # 1. กำหนดสีขาว-ฟ้า พื้นฐาน (Standard Board)
        if (self.row + self.col) % 2 == 0: 
            self.background_color = (0.94, 0.94, 0.91, 1) # ขาวนวล
        else: 
            self.background_color = (0.46, 0.59, 0.74, 1) # ฟ้า Tournament
            
        # 2. ใส่สีสถานะพิเศษ
        if is_check: 
            self.background_color = (1, 0.2, 0.2, 0.8) # ราชาโดนรุก (แดง)
        elif highlight: 
            self.background_color = (1, 1, 0, 0.6) # เลือกหมาก (เหลือง)
            
        # สั่งวาดกราฟิกใหม่
        self.sync_layout()

    def set_piece_icon(self, path):
        """แสดงรูปภาพหมากตาม Path ที่ส่งมา"""
        if path:
            self.piece_img.source = path
            self.piece_img.opacity = 1
        else: 
            self.piece_img.opacity = 0