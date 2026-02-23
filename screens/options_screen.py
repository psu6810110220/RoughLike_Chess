# screens/options_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App

class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # หัวข้อหน้า Options
        title = Label(text="[b][color=ff4400]OPTIONS[/color][/b]", markup=True, font_size='48sp', size_hint_y=0.2)
        layout.add_widget(title)
        
        # คำอธิบาย
        diff_label = Label(text="AI Difficulty", font_size='24sp', size_hint_y=0.1)
        layout.add_widget(diff_label)
        
        # กล่องใส่ปุ่มระดับความยาก 3 ปุ่ม
        self.diff_box = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.2)
        
        self.btn_easy = Button(text="Easy", font_size='20sp')
        self.btn_easy.bind(on_release=lambda x: self.set_difficulty('easy'))
        
        self.btn_normal = Button(text="Normal", font_size='20sp')
        self.btn_normal.bind(on_release=lambda x: self.set_difficulty('normal'))
        
        self.btn_hard = Button(text="Hard", font_size='20sp')
        self.btn_hard.bind(on_release=lambda x: self.set_difficulty('hard'))
        
        self.diff_box.add_widget(self.btn_easy)
        self.diff_box.add_widget(self.btn_normal)
        self.diff_box.add_widget(self.btn_hard)
        layout.add_widget(self.diff_box)
        
        # ช่องว่างผลักปุ่ม Back ให้อยู่ล่างสุด
        layout.add_widget(Label(size_hint_y=0.3))
        
        # ปุ่มย้อนกลับ
        btn_back = Button(text="Back to Menu", font_size='20sp', size_hint_y=0.2, background_color=(0.5, 0.1, 0.1, 1))
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
        
    def on_pre_enter(self, *args):
        # ฟังก์ชันนี้จะทำงานก่อนหน้านี้เปิดขึ้นมา เพื่ออัปเดตสีปุ่มให้ตรงกับค่าปัจจุบัน
        self.update_button_colors()

    def set_difficulty(self, level):
        # บันทึกค่าระดับความยากลงในตัวเกมหลัก
        app = App.get_running_app()
        app.ai_difficulty = level  
        self.update_button_colors()
        
    def update_button_colors(self):
        app = App.get_running_app()
        # ถ้ายังไม่มีค่า ให้ตั้งเริ่มต้นเป็น 'normal'
        current = getattr(app, 'ai_difficulty', 'normal')
        
        # สีส้มแดงสำหรับปุ่มที่ถูกเลือก และสีเทาเข้มสำหรับปุ่มที่ไม่ได้เลือก
        active_color = (0.8, 0.2, 0.0, 1)
        inactive_color = (0.2, 0.2, 0.2, 1)
        
        self.btn_easy.background_color = active_color if current == 'easy' else inactive_color
        self.btn_normal.background_color = active_color if current == 'normal' else inactive_color
        self.btn_hard.background_color = active_color if current == 'hard' else inactive_color

    def go_back(self, instance):
        self.manager.current = 'menu'