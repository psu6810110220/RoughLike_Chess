# components/unit_card.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.animation import Animation

class UnitCard(BoxLayout):
    def __init__(self, piece, img_path, **kwargs):
        super().__init__(orientation='horizontal', size_hint=(None, None), size=(420, 300),
                         pos_hint={'right': 0.95, 'center_y': 0.5}, padding=10, spacing=10, **kwargs)
        
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 0.98) 
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        img = Image(source=img_path, size_hint_x=0.4)
        self.add_widget(img)
        text_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        
        name_lbl = Label(text=piece.__class__.__name__.upper(), bold=True, font_size='22sp', color=(1, 1, 1, 1), halign='left')
        text_layout.add_widget(name_lbl)
        
        p_base = getattr(piece, 'base_points', 5)
        pts_lbl = Label(text=f"{p_base} Points", font_size='16sp', color=(1, 0.8, 0.2, 1), halign='left')
        pts_lbl.bind(size=pts_lbl.setter('text_size')) 
        text_layout.add_widget(pts_lbl)

        p_coins = getattr(piece, 'coins', 3)
        coins_lbl = Label(text=f"Coins: {p_coins}", font_size='14sp', color=(0.7, 0.8, 1, 1), halign='left')
        coins_lbl.bind(size=coins_lbl.setter('text_size'))
        text_layout.add_widget(coins_lbl)
        
        p_item = getattr(piece, 'item', None)
        item_container = BoxLayout(orientation='horizontal', size_hint_y=0.4, spacing=10)
        
        if p_item:
            item_img = Image(source=p_item.image_path, size_hint=(None, None), size=(48, 48), keep_ratio=True, allow_stretch=True)
            item_lbl = Label(text=f"Eqp: {p_item.name}", font_size='14sp', color=(0.4, 1, 0.4, 1), halign='left', valign='middle')
            item_lbl.bind(size=item_lbl.setter('text_size'))
            item_container.add_widget(item_img)
            item_container.add_widget(item_lbl)
        else:
            item_lbl = Label(text="Eqp: No Item", font_size='14sp', color=(0.5, 0.5, 0.5, 1), halign='left', valign='middle')
            item_lbl.bind(size=item_lbl.setter('text_size'))
            item_container.add_widget(item_lbl)

        text_layout.add_widget(item_container)
        self.add_widget(text_layout)

        # Animation ให้สไลด์เข้ามา
        self.x += 20
        self.opacity = 0
        anim = Animation(x=self.x - 20, opacity=1, duration=0.15)
        anim.start(self)

    def _update_bg(self, instance, value):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size