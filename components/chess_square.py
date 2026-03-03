# components/chess_square.py
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Ellipse
from kivy.metrics import dp # ✨ เพิ่มสำหรับจัดการความหนาพิกเซลให้คงที่

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
        
        # เตรียมตัวแสดง passive แฝง
        self.passive_indicator = Label(
            font_size='12sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(22, 22),
            opacity=0
        )
        self.add_widget(self.passive_indicator)
        
        self.is_last_move = False
        self.is_legal = False
        self.highlight = False # ✨ เพิ่มตัวแปรเก็บสถานะการเลือก
        
        # ตั้งค่าสีเริ่มต้น (จะกลายเป็นช่องใส)
        self.update_square_style()
        
        self.bind(pos=self.sync_layout, size=self.sync_layout)

    def sync_layout(self, *args):
        """จัดตำแหน่งรูปหมากและวาดเส้นขอบ (Neon UI) แบบ Inset เพื่อความแม่นยำ"""
        self.piece_img.size = (self.width * 0.85, self.height * 0.85)
        self.piece_img.center = self.center
        
        if hasattr(self, 'passive_indicator'):
            self.passive_indicator.pos = (self.x + self.width - 26, self.y + self.height - 26)
            self.passive_indicator.canvas.before.clear()
            with self.passive_indicator.canvas.before:
                Color(0, 0, 0, 0.5)
                Ellipse(pos=(self.passive_indicator.x - 1, self.passive_indicator.y - 1), 
                       size=(self.passive_indicator.width + 2, self.passive_indicator.height + 2))
        
        # ✨ ล้าง canvas และวาดใหม่แบบ Inset (ขยับเข้ามาข้างใน 1-2 พิกเซล)
        self.canvas.after.clear()
        with self.canvas.after:
            # 1. เส้นขอบสีส้ม (หมากที่ถูกเลือก) - วาดเป็นกรอบสีส้ม
            if self.highlight:
                Color(1, 0.5, 0, 1) # Orange
                # วาดขยับเข้ามาด้านใน 2 พิกเซล เพื่อไม่ให้ทับกับช่องข้างๆ
                Line(rectangle=(self.x + dp(2), self.y + dp(2), self.width - dp(4), self.height - dp(4)), width=dp(2.5))
            
            # 2. เส้นขอบสีเขียวนีออน (ช่องที่เดินได้)
            elif self.is_legal:
                Color(0.1, 1, 0.1, 1) # Green Neon
                Line(rectangle=(self.x + dp(2), self.y + dp(2), self.width - dp(4), self.height - dp(4)), width=dp(2))
            
            # 3. เส้นขอบแจ้งตำแหน่งที่เดินล่าสุด
            elif self.is_last_move:
                Color(1, 1, 0, 0.6) # Yellow
                Line(rectangle=(self.x + dp(1), self.y + dp(1), self.width - dp(2), self.height - dp(2)), width=dp(1.5))

    def update_square_style(self, highlight=False, is_legal=False, is_check=False, is_last=False):
        """อัปเดตสีพื้นหลังและสถานะของช่อง"""
        self.is_last_move = is_last
        self.is_legal = is_legal
        self.highlight = highlight # ✨ เก็บค่าไว้ใช้ใน sync_layout
        
        if is_check: 
            self.background_color = (1, 0.2, 0.2, 0.8) # ราชาโดนรุก (แดง)
        elif highlight: 
            self.background_color = (1, 1, 0, 0.3) # เลือกหมาก (เหลืองจางๆ)
        else:
            self.background_color = (0, 0, 0, 0) # โปร่งใส
            
        self.sync_layout()

    def set_piece_icon(self, path, is_frozen=False, piece=None):
        """แสดงรูปภาพหมากและจัดการสีกรณีโดนแช่แข็ง"""
        if path:
            self.piece_img.source = path
            self.piece_img.opacity = 1
            self.show_hidden_passive(piece)
            
            if is_frozen:
                self.piece_img.color = (0.2, 0.6, 1, 1)  # หมากสีฟ้า
                if self.background_color == [0, 0, 0, 0]:
                    self.background_color = (0, 0.5, 1, 0.4) # พื้นหลังฟ้าโปร่งแสง
            else:
                self.piece_img.color = (1, 1, 1, 1)
                if self.background_color == [0, 0.5, 1, 0.4]: 
                    self.background_color = (0, 0, 0, 0)
        else: 
            self.piece_img.opacity = 0
            self.piece_img.color = (1, 1, 1, 1)
            if hasattr(self, 'passive_indicator'):
                self.passive_indicator.opacity = 0
            if self.background_color == [0, 0.5, 1, 0.4]: 
                self.background_color = (0, 0, 0, 0)
    
    def show_hidden_passive(self, piece):
        """แสดง passive แฝงของหมาก"""
        if not piece or not hasattr(piece, 'hidden_passive'):
            if hasattr(self, 'passive_indicator'):
                self.passive_indicator.opacity = 0
            return
            
        passive_info = piece.hidden_passive.get_passive_info()
        if passive_info['type'] is None:
            self.passive_indicator.opacity = 0
            return
        
        if passive_info['type'].startswith('buff'):
            self.passive_indicator.color = (0.1, 0.9, 0.1, 1)
            self.passive_indicator.text = '+C' if passive_info['type'] == 'buff1' else '+P'
        else:
            self.passive_indicator.color = (1, 0.1, 0.1, 1)
            self.passive_indicator.text = '-C' if passive_info['type'] == 'debuff1' else '-P'
        
        self.passive_indicator.opacity = 1