# components/item_tooltip.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.metrics import dp

class ItemTooltip(BoxLayout):
    def __init__(self, item, **kwargs):
        # ✨ 1. ดันขึ้นบนด้วย 'top': 0.85 และให้ชิดขวาสุดเป๊ะๆ ด้วย 'right': 1.0
        # ✨ 2. ปรับความกว้างเป็น 350 ให้พอดีกับกรอบ Sidebar
        super().__init__(orientation='horizontal', size_hint=(None, None), size=(dp(350), dp(130)),
                         pos_hint={'right': 1.0, 'top': 0.85}, padding=dp(15), spacing=dp(10), **kwargs)
        
        with self.canvas.before:
            # ปรับให้สีทึบ 100% เพื่อจะได้บังเส้นขอบหรือสิ่งของด้านหลังได้มิดชิด
            Color(0.08, 0.08, 0.12, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # ปรับขนาดรูปให้พอดีกับความสูงที่หดลง
        large_img = Image(
            source=item.image_path,
            size_hint=(None, 1),
            width=dp(70), 
            keep_ratio=True,
            allow_stretch=True
        )
        self.add_widget(large_img)
        
        text_layout = BoxLayout(orientation='vertical', spacing=dp(2))
        
        name_lbl = Label(
            text=f"[color=ffff00]{item.name}[/color]", 
            markup=True, bold=True, 
            font_size='20sp', 
            size_hint_y=0.4, 
            halign='left',
            valign='middle'
        )
        name_lbl.bind(size=name_lbl.setter('text_size'))
        
        desc_lbl = Label(
            text=item.description, 
            font_size='14sp', 
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