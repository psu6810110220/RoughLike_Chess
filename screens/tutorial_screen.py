# screens/tutorial_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window

from screens.gameplay_screen import GameplayScreen
from logic.pieces import Pawn, King

class TutorialScreen(GameplayScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tutorial_step = 0
        self.instruction_label = None
        self.overlay = None

    def on_enter(self):
        """เริ่มตั้งค่า Tutorial เมื่อเข้าสู่หน้านี้"""
        self.setup_tutorial()

    def setup_tutorial(self):
        # 1. ใช้ระบบพื้นฐานจาก GameplayScreen ในโหมด TUTORIAL
        self.setup_game(mode='TUTORIAL')
        self.tutorial_step = 1
        
        # 2. จัดวางหมากสำหรับฝึกสอน (Scenario)
        self.game.board = [[None for _ in range(8)] for _ in range(8)]
        
        # วางหมากฝั่งผู้เล่น (White)
        self.game.board[6][4] = Pawn('white', 'medieval') 
        self.game.board[7][4] = King('white', 'medieval')
        
        # วางหมากศัตรู (Black) เพื่อสอน Crash
        target_pawn = Pawn('black', 'demon')
        target_pawn.setup_stats('pawn', 'demon')
        self.game.board[5][4] = target_pawn
        
        self.refresh_ui()
        self.add_tutorial_overlay()
        self.update_instruction()

    def add_tutorial_overlay(self):
        """สร้าง Instruction Box ให้สวยงามพร้อมเส้นขอบ"""
        if self.overlay: return
        self.overlay = FloatLayout(size_hint=(1, 1))
        
        # พื้นหลังและเส้นขอบของกล่องคำแนะนำ
        with self.overlay.canvas.before:
            # 1. พื้นหลังดำโปร่งแสง
            Color(0.05, 0.05, 0.08, 0.85)
            self.bg_rect = Rectangle(
                pos=(dp(20), Window.height - dp(130)), 
                size=(Window.width - dp(40), dp(110))
            )
            # 2. เส้นขอบสีส้ม (Theme ของเกม)
            Color(1, 0.4, 0, 1)
            self.border = Line(
                rectangle=(dp(20), Window.height - dp(130), Window.width - dp(40), dp(110)),
                width=dp(1.5)
            )
        
        self.instruction_label = Label(
            text="", markup=True, font_size='18sp',
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'top': 0.97},
            size_hint=(0.8, 0.1), halign='center', valign='middle'
        )
        self.instruction_label.bind(size=self.instruction_label.setter('text_size'))
        
        self.overlay.add_widget(self.instruction_label)
        self.root_layout.add_widget(self.overlay)

    def update_instruction(self):
        """ข้อความคำแนะนำภาษาอังกฤษตามลำดับการสอน"""
        steps = {
            1: "[color=ffcc00][b]STEP 1: MOVEMENT[/b][/color]\nSelect your [b]White Pawn[/b] and move it forward to attack.",
            2: "[color=ffcc00][b]STEP 2: CRASH COMBAT[/b][/color]\nThe [b]CRASH[/b] has started! Roll the dice to defeat the demon.",
            3: "[color=ffcc00][b]STEP 3: UNIT PASSIVE[/b][/color]\nNotice the [b]Sidebar[/b]. It shows your unit's [b]Passive Skill[/b].",
            4: "[color=ffcc00][b]STEP 4: FINISH[/b][/color]\nYou've learned the basics. Press [b]QUIT MATCH[/b] to return to menu."
        }
        self.instruction_label.text = steps.get(self.tutorial_step, "")

    def on_square_tap(self, instance):
        """ล็อคการเดินใน Step 1 ให้ทำตามคำแนะนำเท่านั้น"""
        r, c = instance.row, instance.col
        if self.tutorial_step == 1:
            if self.selected is None:
                # บังคับให้เลือกเฉพาะ Pawn ที่ช่อง (6,4)
                if (r, c) == (6, 4):
                    super().on_square_tap(instance)
            else:
                # บังคับให้เดินไปโจมตีที่ช่อง (5,4) เท่านั้น
                if (r, c) == (5, 4):
                    super().on_square_tap(instance)
                else:
                    # ถ้าคลิกผิดที่ ให้ยกเลิกการเลือก
                    self.selected = None
                    self.refresh_ui()
            return
        super().on_square_tap(instance)

    def show_crash_overlay(self, attacker, defender, start_pos, end_pos):
        """เมื่อเกิดการ Crash ให้เปลี่ยนไป Step 2"""
        if self.tutorial_step == 1:
            self.tutorial_step = 2
            self.update_instruction()
        super().show_crash_overlay(attacker, defender, start_pos, end_pos)

    def execute_board_move(self, start_pos, end_pos, crash_status):
        """เมื่อการต่อสู้จบลง ให้ไป Step 3 เพื่อดูข้อมูล Passive"""
        super().execute_board_move(start_pos, end_pos, crash_status)
        if self.tutorial_step == 2 and crash_status in ["won", "died"]:
            self.tutorial_step = 3
            self.update_instruction()
            
            # แสดงสถานะของหมากตัวที่ชนะเพื่อให้ผู้เล่นอ่าน Passive Skill
            piece = self.game.board[end_pos[0]][end_pos[1]]
            if piece: 
                self.show_piece_status(piece)
                
            # รอ 5 วินาทีเพื่อให้ผู้เล่นได้อ่าน ก่อนจะจบบทเรียน
            Clock.schedule_once(lambda dt: self.set_step(4), 5)

    def set_step(self, step):
        self.tutorial_step = step
        self.update_instruction()

    def on_quit(self):
        """ล้างหน้าจอ Instruction Box ก่อนออกจากหน้า Tutorial"""
        if self.overlay:
            self.root_layout.remove_widget(self.overlay)
            self.overlay = None
        super().on_quit()