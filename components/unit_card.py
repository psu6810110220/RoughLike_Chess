# screens/match_setup/unit_card.py
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line

class CardButton(Button):
    """ปุ่มสไตล์การ์ดที่มีขอบเรืองแสงเมื่อถูกเลือก"""
    def __init__(self, text, **kwargs):
        kwargs.pop('group', None) # ลบ parameter group ทิ้งเพื่อป้องกัน error
        super().__init__(**kwargs)
        self.text = text
        self.is_selected = False
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.markup = True
        self.halign = 'center'
        self.bind(pos=self.draw_card, size=self.draw_card)

    def set_selected(self, selected):
        """อัปเดตสถานะและวาด UI ใหม่"""
        self.is_selected = selected
        self.draw_card()

    def draw_card(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # สีพื้นหลังการ์ด
            Color(0.1, 0.1, 0.15, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[15,])
            
            # ถ้าถูกเลือก ให้วาดขอบเรืองแสงสี Cyan
            if self.is_selected:
                Color(0, 0.8, 1, 1) 
                Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 15), width=2)