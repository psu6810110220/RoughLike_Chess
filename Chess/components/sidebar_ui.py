# ไฟล์: components/sidebar_ui.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class SidebarUI(BoxLayout):
    def __init__(self, on_undo_callback, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.size_hint_x = 0.25 
        self.padding = 10
        self.spacing = 10

        # หัวข้อ
        self.add_widget(Label(text="Move History", size_hint_y=0.1, color=(1, 0.84, 0, 1), bold=True))

        # กล่อง ScrollView
        self.history_scroll = ScrollView(size_hint_y=0.8)
        
        # ✨ เปิดใช้งาน markup=True เพื่อให้ใส่สีตัวอักษรได้
        self.history_label = Label(text="", size_hint_y=None, markup=True, halign='left', valign='top')
        
        # ผูกความสูงให้ขยายตามตัวอักษร
        self.history_label.bind(
            width=lambda *x: self.history_label.setter('text_size')(self.history_label, (self.history_label.width, None)),
            texture_size=lambda *x: self.history_label.setter('height')(self.history_label, self.history_label.texture_size[1])
        )
        
        self.history_scroll.add_widget(self.history_label)
        self.add_widget(self.history_scroll)

        # ปุ่ม Undo
        self.undo_btn = Button(text="Undo Move", size_hint_y=0.1, background_color=(0.9, 0.4, 0.4, 1), bold=True)
        self.undo_btn.bind(on_release=lambda instance: on_undo_callback())
        self.add_widget(self.undo_btn)

    def update_history_text(self, moves_list):
        """✨ จัดรูปแบบใหม่ มีหัวตารางและแยกสีชัดเจน"""
        # สร้างหัวตาราง (Turn | White | Black)
        text = "[b][color=aaccff]Turn[/color]    [color=ffffff]White[/color]         [color=aaaaaa]Black[/color][/b]\n"
        text += "[color=555555]" + "-" * 35 + "[/color]\n"
        
        for i in range(0, len(moves_list), 2):
            turn_num = (i // 2) + 1
            white_move = moves_list[i]
            black_move = moves_list[i+1] if i+1 < len(moves_list) else ""
            
            # จัดช่องว่าง (Padding) ของสีขาวให้เท่ากันเสมอ (เว้นไว้ 12 เคาะ)
            white_padded = f"{white_move:<12}" 
            
            # ประกอบร่างข้อความพร้อมใส่สี
            text += f"[b]{turn_num}.[/b]       [color=ffffff]{white_padded}[/color] [color=aaaaaa]{black_move}[/color]\n"
            
        self.history_label.text = text