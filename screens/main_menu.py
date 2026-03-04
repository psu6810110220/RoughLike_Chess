# screens/main_menu.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Rectangle, Color 
from kivy.animation import Animation 

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # วาดภาพพื้นหลัง
        with self.canvas.before:
            Color(1, 1, 1, 1) 
            # ✨ แก้ไข Path และนามสกุลไฟล์ให้ตรงกับในโฟลเดอร์ของคุณเป๊ะๆ
            self.bg_image = Rectangle(source='assets/ui/backgrounds/menu_bg.png', pos=self.pos, size=self.size)
            Color(0.05, 0.05, 0.08, 0.6) 
            self.bg_overlay = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        
        # Title & Subtitle
        title_box = BoxLayout(orientation='vertical', size_hint_y=0.4)
        title_box.add_widget(Label(
            text="[b][color=ff4400]- ROGUELIKE CHESS -[/color][/b]",
            markup=True, font_size='64sp'
        ))
        title_box.add_widget(Label(
            text="Enter the Dark Battlefield • Face Your Destiny",
            font_size='18sp', color=(0.8, 0.8, 0.9, 1) 
        ))
        layout.add_widget(title_box)
        
        # Buttons
        btn_box = BoxLayout(orientation='vertical', spacing=15, size_hint=(0.4, 0.5), pos_hint={'center_x': 0.5})
        
        play_btn = Button(text="PLAY", background_color=(1, 0.3, 0, 0.9), bold=True, font_size='24sp')
        play_btn.bind(on_press=self.play_btn_sound, on_release=self.go_play)
        
        tutorial_btn = Button(text="TUTORIAL", background_color=(0.1, 0.6, 0.8, 0.9), bold=True, font_size='24sp')
        tutorial_btn.bind(on_press=self.play_btn_sound, on_release=self.go_tutorial)
        
        opt_btn = Button(text="Options", background_color=(0.2, 0.2, 0.3, 0.9))
        opt_btn.bind(on_press=self.play_btn_sound, on_release=self.go_options) 
        
        exit_btn = Button(text="Exit", background_color=(0.5, 0.1, 0.1, 0.9))
        exit_btn.bind(on_press=self.play_btn_sound, on_release=self.do_exit)
        
        btn_box.add_widget(play_btn)
        btn_box.add_widget(tutorial_btn)
        btn_box.add_widget(opt_btn)
        btn_box.add_widget(exit_btn)
        
        layout.add_widget(btn_box)
        
        self.prep_label = Label(text=">> PREPARE FOR BATTLE <<", size_hint_y=0.1, color=(1, 0.5, 0, 1))
        layout.add_widget(self.prep_label)
        
        self.add_widget(layout)

    def update_bg(self, *args):
        self.bg_image.pos = self.pos
        self.bg_image.size = self.size
        self.bg_overlay.pos = self.pos
        self.bg_overlay.size = self.size

    def on_enter(self, *args):
        anim = Animation(opacity=0.2, duration=1.0) + Animation(opacity=1, duration=1.0)
        anim.repeat = True 
        anim.start(self.prep_label) 

    def on_leave(self, *args):
        Animation.cancel_all(self.prep_label)

    def play_btn_sound(self, instance=None):
        app = App.get_running_app()
        if hasattr(app, 'play_click_sound'):
            app.play_click_sound()

    def go_play(self, instance):
        self.manager.current = 'setup'

    def go_tutorial(self, instance):
        self.manager.current = 'tutorial'

    def go_options(self, instance):
        self.manager.current = 'options'

    def do_exit(self, instance):
        App.get_running_app().stop()