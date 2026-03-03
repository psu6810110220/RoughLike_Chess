# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from screens.main_menu import MainMenuScreen
from screens.match_setup.setup_screen import MatchSetupScreen
from screens.gameplay_screen import GameplayScreen
from screens.options_screen import OptionsScreen
from screens.tutorial_screen import TutorialScreen  # ✨ เพิ่มการ import TutorialScreen
from kivy.properties import StringProperty

class RogueChessApp(App):
    ai_difficulty = 'normal'  # ตั้งค่าความยากเริ่มต้นของ AI

    # ✨ ตัวแปร StringProperty สำหรับเก็บค่าการตั้งค่าต่างๆ
    selected_board = StringProperty('Classic Board') 
    selected_unit_white = StringProperty('Medieval Knights') 
    selected_unit_black = StringProperty('Demon')
    
    def build(self):
        # สร้าง ScreenManager พร้อมเอฟเฟกต์เฟดตอนเปลี่ยนหน้า
        sm = ScreenManager(transition=FadeTransition())
        
        # เพิ่มหน้าจอต่างๆ เข้าไปในระบบ
        sm.add_widget(MainMenuScreen(name='main_menu')) 
        sm.add_widget(MatchSetupScreen(name='setup'))
        
        # 🚨 FIX: หน้า Gameplay หลัก
        sm.add_widget(GameplayScreen(name='gameplay')) 
        
        # ✨ เพิ่มหน้า Tutorial เข้าไปในระบบ (Step 2)
        sm.add_widget(TutorialScreen(name='tutorial'))
        
        sm.add_widget(OptionsScreen(name='options')) # หน้า Options
        
        return sm

if __name__ == "__main__":
    RogueChessApp().run()