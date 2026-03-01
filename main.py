# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from screens.main_menu import MainMenuScreen
from screens.match_setup.setup_screen import MatchSetupScreen
from screens.gameplay_screen import GameplayScreen
from screens.options_screen import OptionsScreen

class RogueChessApp(App):
    ai_difficulty = 'normal'  # ตั้งค่าความยากเริ่มต้นของ AI
    
    selected_unit_white = StringProperty('Medieval Knights') 
    selected_unit_black = StringProperty('Demon')
    def build(self):
        # สร้าง ScreenManager พร้อมเอฟเฟกต์เฟดตอนเปลี่ยนหน้า
        sm = ScreenManager(transition=FadeTransition())
        
        # เพิ่มหน้าจอต่างๆ เข้าไปในระบบ
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(MatchSetupScreen(name='setup'))
        sm.add_widget(GameplayScreen(name='game'))
        sm.add_widget(OptionsScreen(name='options')) # เพิ่มหน้า Options เข้าระบบ
        
        return sm

if __name__ == "__main__":
    RogueChessApp().run()