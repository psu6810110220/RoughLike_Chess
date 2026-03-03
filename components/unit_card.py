# components/unit_card.py
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color

class UnitCard(ButtonBehavior, BoxLayout):
    def __init__(self, piece=None, img_path=None, **kwargs):
        text_to_show = kwargs.pop('text', '') 
        kwargs.setdefault('size_hint', (1, 1))
        super().__init__(orientation='vertical', padding=15, spacing=5, **kwargs)
        
        with self.canvas.before:
            self.bg_color = Color(0.1, 0.1, 0.12, 1) 
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        if piece is None:
            lbl = Label(text=text_to_show, color=(1, 1, 1, 1), font_size='20sp', markup=True, halign='center')
            lbl.bind(size=lbl.setter('text_size'))
            self.add_widget(lbl)
            return 
            
        # UI สำหรับโหมด Gameplay
        self.add_widget(Label(text=piece.__class__.__name__.upper(), bold=True, font_size='22sp', color=(1,1,1,1), size_hint_y=0.15))
        
        mid = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.3)
        mid.add_widget(Image(source=img_path, size_hint_x=0.4))
        mid.add_widget(Label(text=f"{getattr(piece, 'base_points', 5)} Pts", font_size='20sp', color=(1, 0.8, 0.2, 1)))
        self.add_widget(mid)
        
        stats_row = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        stats_row.add_widget(Label(text=f"Coins: {getattr(piece, 'coins', 3)}", font_size='14sp', color=(0.7, 0.8, 1, 1)))
        p_item = getattr(piece, 'item', None)
        stats_row.add_widget(Label(text=f"Eqp: {p_item.name if p_item else 'None'}", font_size='13sp', color=(0.5, 0.5, 0.5, 1)))
        self.add_widget(stats_row)

        # ✨ ส่วนแสดงผล Passive Description (English)
        desc = getattr(piece, 'passive_desc', 'No special ability')
        passive_lbl = Label(text=f"[i]{desc}[/i]", font_size='13sp', color=(0.8, 0.9, 1, 1), size_hint_y=0.4, markup=True, halign='center', valign='top')
        passive_lbl.bind(size=passive_lbl.setter('text_size'))
        self.add_widget(passive_lbl)

    def _update_bg(self, instance, value):
        self.bg_rect.pos, self.bg_rect.size = instance.pos, instance.size

    def set_selected(self, is_selected):
        self.bg_color.rgba = (0.2, 0.45, 0.2, 1) if is_selected else (0.1, 0.1, 0.12, 1)