from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.graphics import Color, Rectangle

from components.unit_card import CardButton

class SetupSection(BoxLayout):
    def __init__(self, title, options, target_attr='selected_unit', **kwargs):
        kwargs.pop('cols', None)
        kwargs.pop('group_name', None)
        
        super().__init__(orientation='vertical', spacing=10, **kwargs)
        self.target_attr = target_attr 
        
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.add_widget(Label(text=title, font_size='20sp', bold=True, size_hint_y=0.15, color=(0.8, 0.7, 0.3, 1)))
        
        self.cards = []
        for opt in options:
            # ✨ เช็คว่าข้อมูลตัวเลือกเป็น Dictionary หรือ String ปกติ
            if isinstance(opt, dict):
                text_to_show = str(opt.get('text', opt))
                val_to_save = opt.get('value', opt)
            elif isinstance(opt, tuple) or isinstance(opt, list):
                text_to_show = str(opt[0])
                val_to_save = opt[1] if len(opt) > 1 else opt[0]
            else:
                text_to_show = str(opt)
                val_to_save = opt
                
            card = UnitCard(text=text_to_show)
            card.bind(on_release=lambda c, v=val_to_save: self.select_option(c, v))
            self.add_widget(card)
            self.cards.append(card)
            
        app = App.get_running_app()
        default_val = getattr(app, self.target_attr, val_to_save) # ใช้ค่าสุดท้ายเป็นค่าตั้งต้นชั่วคราว
        
        for card in self.cards:
            # เทียบชื่อปุ่มกับค่า default
            if card.text == str(default_val):
                card.set_selected(True)
            else:
                card.set_selected(False)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def select_option(self, selectedCard, value):
        for card in self.cards:
            card.set_selected(card == selectedCard)
            
        app = App.get_running_app()
        setattr(app, self.target_attr, value)