# screens/tutorial_screen.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
from screens.gameplay_screen import GameplayScreen
from logic.pieces import Pawn, King

class TutorialScreen(GameplayScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs); self.tutorial_step = 0; self.instr_box = None

    def on_enter(self):
        # ✨ Advanced Fix: เรียกการวาดโครงสร้าง Layout จาก GameplayScreen ก่อน
        super().setup_game(mode='TUTORIAL')
        # หน่วงเวลา 0.2 วินาทีเพื่อให้ Kivy คำนวณพิกัดบอร์ดจริงเสร็จก่อนวางหมาก
        Clock.schedule_once(self.inject_scenario, 0.2)

    def inject_scenario(self, dt):
        self.tutorial_step = 1; self.game.board = [[None for _ in range(8)] for _ in range(8)]
        # วางหมากขาว
        white_pawn = Pawn('white', 'medieval'); white_pawn.setup_stats('pawn', 'medieval')
        self.game.board[6][4] = white_pawn
        white_king = King('white', 'medieval'); white_king.setup_stats('king', 'medieval')
        self.game.board[7][4] = white_king
        # วางหมากดำ (ศัตรู)
        target_pawn = Pawn('black', 'demon'); target_pawn.setup_stats('pawn', 'demon')
        self.game.board[5][4] = target_pawn
        
        # บังคับรีเฟรช Grid และพิกัดบอร์ดให้ตรงตามหน้าจอจริง
        if hasattr(self, 'board_anchor'): self._keep_grid_square(self.board_anchor, self.board_anchor.size)
        self.refresh_ui(); self.add_tutorial_overlay(); self.update_instruction()

    def add_tutorial_overlay(self):
        if self.instr_box: self.root_layout.remove_widget(self.instr_box)
        self.instr_box = BoxLayout(orientation='vertical', size_hint=(0.7, 0.12), pos_hint={'center_x': 0.5, 'top': 0.98}, padding=dp(10))
        with self.instr_box.canvas.before:
            Color(0.05, 0.05, 0.08, 0.9); self.bg_rect = Rectangle(pos=self.instr_box.pos, size=self.instr_box.size)
            Color(1, 0.4, 0, 1); self.border = Line(rectangle=(self.instr_box.x, self.instr_box.y, self.instr_box.width, self.instr_box.height), width=dp(1.5))
        self.instr_box.bind(pos=self._update_ui, size=self._update_ui)
        self.lbl = Label(text="", markup=True, font_size='18sp', halign='center')
        self.lbl.bind(size=self.lbl.setter('text_size')); self.instr_box.add_widget(self.lbl); self.root_layout.add_widget(self.instr_box)
    def _update_ui(self, instance, value):
        self.bg_rect.pos, self.bg_rect.size = instance.pos, instance.size
        self.border.rectangle = (instance.x, instance.y, instance.width, instance.height)

    def update_instruction(self):
        steps = {
            1: "[color=ffcc00][b]STEP 1: MOVEMENT[/b][/color]\\nSelect your [b]White Pawn[/b] and move it forward to attack.",
            2: "[color=ffcc00][b]STEP 2: CRASH COMBAT[/b][/color]\\nThe [b]CRASH[/b] has started! Roll the dice to defeat the demon.",
            3: "[color=ffcc00][b]STEP 3: UNIT PASSIVE[/b][/color]\\nCheck the [b]Sidebar[/b] to see your unit's [b]Passive Skill[/b].",
            4: "[color=ffcc00][b]STEP 4: FINISH[/b][/color]\\nBasic training complete! Press [b]QUIT MATCH[/b] to go back."
        }
        if hasattr(self, 'lbl'): self.lbl.text = steps.get(self.tutorial_step, "")

    def on_square_tap(self, instance):
        r, c = instance.row, instance.col
        if self.tutorial_step == 1:
            if self.selected is None and (r, c) == (6, 4): super().on_square_tap(instance)
            elif self.selected is not None and (r, c) == (5, 4): super().on_square_tap(instance)
            else: self.selected = None; self.refresh_ui()
            return
        super().on_square_tap(instance)

    def show_crash_overlay(self, attacker, defender, start, end):
        if self.tutorial_step == 1: self.tutorial_step = 2; self.update_instruction()
        super().show_crash_overlay(attacker, defender, start, end)

    def execute_board_move(self, start, end, status):
        super().execute_board_move(start, end, status)
        if self.tutorial_step == 2 and status in ["won", "died"]:
            self.tutorial_step = 3; self.update_instruction(); p = self.game.board[end[0]][end[1]]
            if p: self.show_piece_status(p)
            Clock.schedule_once(lambda dt: self.set_step(4), 5)
    def set_step(self, s): self.tutorial_step = s; self.update_instruction()
    def on_quit(self):
        if self.instr_box: self.root_layout.remove_widget(self.instr_box); self.instr_box = None
        super().on_quit()