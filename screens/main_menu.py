# screens/main_menu.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.app import App # นำเข้า App เพื่อใช้สั่งปิดแอป

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (0.02, 0.02, 0.05, 1) # พื้นหลังมืดสนิท
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        
        # Title & Subtitle
        title_box = BoxLayout(orientation='vertical', size_hint_y=0.4)
        title_box.add_widget(Label(
            text="[b][color=ff4400]⚔ ROGUELIKE CHESS ⚔[/color][/b]",
            markup=True, font_size='64sp'
        ))
        title_box.add_widget(Label(
            text="Enter the Dark Battlefield • Face Your Destiny",
            font_size='18sp', color=(0.7, 0.7, 0.8, 1)
        ))
        layout.add_widget(title_box)
        
        # Buttons
        btn_box = BoxLayout(orientation='vertical', spacing=15, size_hint=(0.4, 0.4), pos_hint={'center_x': 0.5})
        
        # 1. ปุ่ม PLAY
        play_btn = Button(text="PLAY", background_color=(1, 0.3, 0, 1), bold=True, font_size='24sp')
        play_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'setup'))
        
        # 2. ปุ่ม Options (เพิ่มจุดเชื่อมต่อตรงนี้ครับ ✨)
        opt_btn = Button(text="Options", background_color=(0.2, 0.2, 0.3, 1))
        opt_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'options'))
        
        # 3. ปุ่ม Exit (เพิ่มฟังก์ชันปิดแอป ✨)
        exit_btn = Button(text="Exit", background_color=(0.5, 0.1, 0.1, 1))
        exit_btn.bind(on_release=lambda x: App.get_running_app().stop())
        
        btn_box.add_widget(play_btn)
        btn_box.add_widget(opt_btn)
        btn_box.add_widget(exit_btn)
        
        layout.add_widget(btn_box)
        layout.add_widget(Label(text="⚡ PREPARE FOR BATTLE ⚡", size_hint_y=0.1, color=(1, 0.5, 0, 1)))
        
        self.add_widget(layout)