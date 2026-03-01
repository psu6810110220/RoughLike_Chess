# screens/match_setup/setup_screen.py
# screens/match_setup/setup_screen.py
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.app import App
from screens.match_setup.setup_section import SetupSection

class MatchSetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = BoxLayout(orientation='vertical', padding=20, spacing=10)
        Window.clearcolor = (0.02, 0.02, 0.05, 1)

        # 1. Header 
        header = BoxLayout(size_hint_y=None, height=60)
        back_btn = Button(text="< Back", size_hint_x=0.2, background_color=(0.3, 0.3, 0.3, 1))
        back_btn.bind(on_release=self.go_back)
        header.add_widget(back_btn)
        header.add_widget(Label(text="Make Match", font_size='28sp', bold=True))
        self.root.add_widget(header)

        # 2. Scrollable Area
        self.scroll = ScrollView()
        self.content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=30, padding=[0, 20])
        self.content.bind(minimum_height=self.content.setter('height'))
        
        # --- Section 1: Game Mode ---
        mode_items = [
            ("[b]PVE Mode[/b]\nPlay against AI", "PVE"),
            ("[b]PVP Mode[/b]\nLocal 2 Players", "PVP")
        ]
        self.mode_section = SetupSection(
            title="⚔ Select Game Mode", 
            options=mode_items, 
            target_attr='selected_mode', 
            size_hint_y=None, 
            height=200
        )
        self.content.add_widget(self.mode_section)

        # --- Section 2: Faction & Board Container ---
        sections_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=450)

        # เผ่าฝ่ายขาว
        self.white_unit_section = SetupSection(
            title="WHITE FACTION", 
            options=['Medieval Knights', 'Ayothaya', 'Demon', 'Heaven'],
            target_attr='selected_unit_white'
        )
        
        # เผ่าฝ่ายดำ
        self.black_unit_section = SetupSection(
            title="BLACK FACTION", 
            options=['Medieval Knights', 'Ayothaya', 'Demon', 'Heaven'],
            target_attr='selected_unit_black'
        )
        
        # กระดาน
        self.board_section = SetupSection(
            title="MAP SELECTION", 
            options=['Classic Board', 'Enchanted Forest', 'Desert Ruins', 'Frozen Tundra', 'Random Board'],
            target_attr='selected_board' 
        )

        sections_layout.add_widget(self.white_unit_section)
        sections_layout.add_widget(self.black_unit_section)
        sections_layout.add_widget(self.board_section)
        
        self.content.add_widget(sections_layout)
        
        # --- Section 3: Start Button ---
        start_btn = Button(text="START BATTLE", size_hint_y=None, height=80, 
                          background_color=(0, 0.8, 0.4, 1), bold=True, font_size='22sp')
        start_btn.bind(on_release=self.start_battle)
        self.content.add_widget(start_btn)

        self.scroll.add_widget(self.content)
        self.root.add_widget(self.scroll)

        self.add_widget(self.root)

    def go_back(self, instance):
        self.manager.current = 'menu'

    def start_battle(self, instance):
        app = App.get_running_app()
        
        # ดึงค่าปัจจุบันที่ถูกเลือกไว้
        final_board = getattr(app, 'selected_board', 'Classic Board')
        final_mode = getattr(app, 'selected_mode', 'PVE')
        
        if final_board == "Random Board":
            playable_boards = ["Classic Board", "Enchanted Forest", "Desert Ruins", "Frozen Tundra"] 
            final_board = random.choice(playable_boards)
            app.selected_board = final_board # อัปเดตกลับไปที่ App เผื่อต้องดึงไปใช้หน้าอื่น
            print(f"System randomized board to: {final_board}") 

        # ตรวจสอบค่าที่จะถูกส่งไปหน้าเกม (คุณสามารถนำค่าเหล่านี้ไปใช้รันโมเดลหมากได้เลย)
        print(f"Starting Match: Mode={final_mode}, Board={final_board}")
        print(f"White Faction: {getattr(app, 'selected_unit_white', 'Medieval Knights')}")
        print(f"Black Faction: {getattr(app, 'selected_unit_black', 'Medieval Knights')}")

        game_screen = self.manager.get_screen('game')
        
        # ส่ง Mode ไปตั้งค่าให้เกมรับรู้ (ถ้าเมธอดใน GameScreen รองรับ)
        if hasattr(game_screen, 'setup_game'):
            game_screen.setup_game(final_mode) 
            
        self.manager.current = 'game'

    def clear_steps_after(self, step_index):
        while len(self.content.children) > step_index:
            self.content.remove_widget(self.content.children[0])

    def show_mode_selection(self):
        items = [
            ("[b]PVE Mode[/b]\nPlay against AI", "PVE"),
            ("[b]PVP Mode[/b]\nLocal 2 Players", "PVP")
        ]
        sec = SetupSection("⚔ Select Game Mode", items, cols=2, group_name="mode", 
                           on_select_callback=self.on_select, height=120)
        self.sections['mode'] = sec
        self.content.add_widget(sec)

    def show_board_selection(self):
        boards = ["Classic Board", "Enchanted Forest", "Desert Ruins", "Frozen Tundra", "Random Board"]
        items = [(b, b) for b in boards] 
        sec = SetupSection("✨ Select Board", items, cols=3, group_name="board", 
                           on_select_callback=self.on_select, height=220)
        self.sections['board'] = sec
        self.content.add_widget(sec)

    def show_unit_selection(self):
        # แก้ไขจาก "Royal Guard" เป็น "Ayothaya"
        units = ["Medieval Knights", "Ayothaya", "Demon", "Heaven"]
        items = [(u, u) for u in units]
        sec = SetupSection("🛡 Select Your Units", items, cols=2, group_name="unit", 
                           on_select_callback=self.on_select, height=250)
        self.sections['unit'] = sec
        self.content.add_widget(sec)

    def show_start_button(self):
        start_btn = Button(text="START BATTLE", size_hint_y=None, height=80, 
                          background_color=(0, 0.8, 0.4, 1), bold=True, font_size='22sp')
        start_btn.bind(on_release=self.start_battle)
        self.content.add_widget(start_btn)

    def show_coming_soon_popup(self, item_name):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f"[b]{item_name}[/b]\nis still in development!\n(Please select Classic for now)", markup=True, halign='center'))
        close_btn = Button(text="OK", size_hint_y=None, height=40, background_color=(0.8, 0.2, 0.2, 1))
        popup = Popup(title='Coming Soon', content=content, size_hint=(0.6, 0.35), auto_dismiss=True)
        close_btn.bind(on_release=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

    def on_select(self, category, value, clicked_btn):
        # ✨ ปลดล็อก Board ให้กดได้ทุกอันแล้ว
        
        # ดักจับ Unit: อนุญาตแค่ Classic Knights
        if category == 'unit' and value not in ["Medieval Knights", "Ayothaya", "Demon", "Heaven"]:
            self.show_coming_soon_popup(value)
            return

        self.sections[category].update_selection(clicked_btn)
        self.selected_data[category] = value

        if category == 'mode':
            self.clear_steps_after(1)
            self.step = 2
            self.show_board_selection()
        elif category == 'board':
            self.clear_steps_after(2)
            self.step = 3
            self.show_unit_selection()
        elif category == 'unit':
            self.clear_steps_after(3)
            self.step = 4
            self.show_start_button()

