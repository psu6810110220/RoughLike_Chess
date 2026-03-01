from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from screens.match_setup.unit_card import UnitCard
from kivy.graphics import Color, Rectangle

class SetupSection(BoxLayout):
    # ✨ แก้ไข __init__ ให้รับ target_attr เพิ่มเข้ามา
    def __init__(self, title, options, target_attr='selected_unit', **kwargs):
        super().__init__(orientation='vertical', spacing=10, **kwargs)
        self.target_attr = target_attr # บันทึกว่า section นี้ปรับค่าตัวแปรไหน
        
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.add_widget(Label(text=title, font_size='20sp', bold=True, size_hint_y=0.15, color=(0.8, 0.7, 0.3, 1)))
        
        self.cards = []
        for opt in options:
            card = UnitCard(text=opt)
            card.bind(on_release=lambda c, val=opt: self.select_option(c, val))
            self.add_widget(card)
            self.cards.append(card)
            
        # ✨ ดึงค่าเริ่มต้นตาม target_attr (แยกระหว่างขาว/ดำ)
        app = App.get_running_app()
        default_val = getattr(app, self.target_attr, options[0])
        for card in self.cards:
            if card.text == default_val:
                card.set_selected(True)
            else:
                card.set_selected(False)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def select_option(self, selectedCard, value):
        for card in self.cards:
            card.set_selected(card == selectedCard)
            
        # ✨ บันทึกค่าลงตัวแปรใน App ตาม target_attr ที่ตั้งไว้
        app = App.get_running_app()
        setattr(app, self.target_attr, value)