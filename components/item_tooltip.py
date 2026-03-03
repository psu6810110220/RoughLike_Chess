# components/item_tooltip.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color

class ItemTooltip(BoxLayout):
    def __init__(self, item, **kwargs):
        super().__init__(orientation='horizontal', size_hint=(None, None), size=(800, 300),
                         pos_hint={'right': 0.98, 'center_y': 0.5}, padding=20, spacing=20, **kwargs)
        
        with self.canvas.before:
            Color(0.05, 0.05, 0.1, 0.98)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # รูปภาพขนาดใหญ่ด้านซ้าย
        large_img = Image(
            source=item.image_path,
            size_hint=(None, 1),
            width=200,
            keep_ratio=True,
            allow_stretch=True
        )
        self.add_widget(large_img)
        
        # กรอบข้อความด้านขวา
        text_layout = BoxLayout(orientation='vertical', spacing=10)
        
        name_lbl = Label(
            text=f"[color=ffff00]{item.name}[/color]", 
            markup=True, bold=True, 
            font_size='48sp', 
            size_hint_y=0.4, 
            halign='left'
        )
        name_lbl.bind(size=name_lbl.setter('text_size'))
        
        desc_lbl = Label(
            text=item.description, 
            font_size='36sp', 
            color=(0.9, 0.9, 0.9, 1),
            halign="left", 
            valign="top"
        )
        desc_lbl.bind(size=desc_lbl.setter('text_size'))
        
        text_layout.add_widget(name_lbl)
        text_layout.add_widget(desc_lbl)
        self.add_widget(text_layout)

    def _update_bg(self, instance, value):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size