# screens/match_setup/setup_section.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from screens.match_setup.unit_card import CardButton # นำเข้าปุ่มการ์ดจากไฟล์ที่ 1

class SetupSection(BoxLayout):
    """Component สำหรับสร้างหัวข้อและกลุ่มปุ่มตัวเลือกแบบอัตโนมัติ"""
    def __init__(self, title, items, cols, group_name, on_select_callback, height=200, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, spacing=10, **kwargs)
        self.bind(minimum_height=self.setter('height'))
        
        # สร้างหัวข้อ Section
        self.add_widget(Label(text=title, size_hint_y=None, height=40, bold=True, halign='left'))
        
        # สร้างตารางใส่ปุ่มการ์ด
        self.grid = GridLayout(cols=cols, spacing=15, size_hint_y=None, height=height)
        self.buttons = []
        
        # สร้างปุ่มตามรายชื่อที่ส่งเข้ามา (รับเป็น Tuple: (ข้อความบนปุ่ม, ค่าที่จะส่งกลับ))
        for display_text, item_value in items:
            btn = CardButton(text=display_text, group=group_name)
            btn.bind(on_release=lambda x, val=item_value, b=btn: on_select_callback(group_name, val, b))
            self.grid.add_widget(btn)
            self.buttons.append(btn)
            
        self.add_widget(self.grid)

    def update_selection(self, selected_btn):
        """ล้างขอบเรืองแสงปุ่มอื่นในกลุ่ม แล้วเปิดให้แค่ปุ่มที่ถูกกด"""
        for b in self.buttons:
            b.is_selected = False
            b.draw_card()
        selected_btn.is_selected = True
        selected_btn.draw_card()