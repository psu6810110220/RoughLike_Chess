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
        self.piece_img = Image(fit_mode='contain', opacity=0)
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
        
        # ✨ เปลี่ยนสีพื้นหลังปกติให้เป็น "สีใส" (Alpha = 0)
        if is_check: 
            self.background_color = (1, 0.2, 0.2, 0.8) # ราชาโดนรุก (แดงโปร่งแสง)
        elif highlight: 
            self.background_color = (1, 1, 0, 0.6) # เลือกหมาก (เหลืองโปร่งแสง)
        else:
            # ไม่ได้เลือกอะไรเลย ให้โปร่งใส 100% เพื่อโชว์รูปภาพพื้นหลังด่าน
            self.background_color = (0, 0, 0, 0) 
            
        self.sync_layout()

    # ✨ ฟังก์ชันนี้คือจุดที่มีปัญหา แก้ไขให้รับค่า is_frozen แล้ว
    def set_piece_icon(self, path, is_frozen=False):
        """แสดงรูปภาพหมากตาม Path ที่ส่งมา และปรับเป็นสีฟ้าถ้าโดนแช่แข็ง"""
        if path:
            self.piece_img.source = path
            self.piece_img.opacity = 1
            
            # ✨ ถ้าติดแช่แข็งให้ปรับสีตัวหมากให้เข้มขึ้น และใส่สีพื้นหลังช่อง
            if is_frozen:
                # เปลี่ยนตัวหมากให้เป็นสีน้ำเงินเข้ม/ฟ้าเข้ม 
                self.piece_img.color = (0.2, 0.6, 1, 1)  
                
                # ซ้อนสีพื้นหลังช่องให้เป็นสีฟ้าโปร่งแสง เพื่อให้สังเกตง่ายขึ้น
                if self.background_color == [0, 0, 0, 0]: # ถ้าช่องปกติ (ไม่ได้ถูกเลือกหรือโดนรุก)
                    self.background_color = (0, 0.5, 1, 0.4) 
            else:
                self.piece_img.color = (1, 1, 1, 1) # หมากสีปกติ
                # คืนค่าพื้นหลังช่องกลับเป็นโปร่งใส (ถ้าไม่ได้ติด highlight หรือ check)
                if self.background_color == [0, 0.5, 1, 0.4]: 
                    self.background_color = (0, 0, 0, 0)
        else: 
            self.piece_img.opacity = 0
            self.piece_img.color = (1, 1, 1, 1)
            # รีเซ็ตสีพื้นหลังกรณีหมากตาย/หายไปจากช่อง
            if self.background_color == [0, 0.5, 1, 0.4]: 
                self.background_color = (0, 0, 0, 0)