# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from screens.main_menu import MainMenuScreen
from screens.match_setup.setup_screen import MatchSetupScreen
from screens.gameplay_screen import GameplayScreen

class RogueChessApp(App):
    def build(self):
        # สร้าง ScreenManager พร้อมเอฟเฟกต์เฟดตอนเปลี่ยนหน้า
        sm = ScreenManager(transition=FadeTransition())
        
        # เพิ่มหน้าจอต่างๆ เข้าไปในระบบ
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(MatchSetupScreen(name='setup'))
        sm.add_widget(GameplayScreen(name='game'))
        
        return sm

if __name__ == "__main__":
    RogueChessApp().run()