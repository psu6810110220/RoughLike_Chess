# screens/gameplay_screen.py
from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.clock import Clock

from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from logic.board import ChessBoard
from logic.ai_logic import ChessAI
from components.chess_square import ChessSquare
from components.sidebar_ui import SidebarUI

try:
    from logic.maps.forest_map import ForestMap
except ImportError:
    ForestMap = None

try:
    from logic.maps.desert_map import DesertMap
except ImportError:
    DesertMap = None

# ✨ ดึง TundraMap เข้ามา
try:
    from logic.maps.tundra_map import TundraMap
except ImportError:
    TundraMap = None

class PromotionPopup(ModalView):
    def __init__(self, color, callback, **kwargs):
        super().__init__(size_hint=(0.6, 0.2), auto_dismiss=False, **kwargs)
        layout = GridLayout(cols=4, padding=10, spacing=10)
        from logic.pieces import Queen, Rook, Bishop, Knight
        ops = [Queen, Rook, Bishop, Knight]
        names = ['queen', 'rook', 'bishop', 'knight']
        for cls, n in zip(ops, names):
            btn = Button(background_normal=f"assets/pieces/classic/{color}/{n}.png")
            btn.bind(on_release=lambda b, c=cls: callback(c))
            layout.add_widget(btn)
        self.add_widget(layout)

class GameplayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root_layout = FloatLayout()
        self.main_layout = BoxLayout(orientation='horizontal')
        self.root_layout.add_widget(self.main_layout)
        self.add_widget(self.root_layout)
        self.status_popup = None
        self.clash_popup = None

    def setup_game(self, mode):
        self.main_layout.clear_widgets()
        self.game_mode = mode
        
        app = App.get_running_app()
        selected_board = getattr(app, 'selected_board', 'Classic Board')
        
        # ✨ เช็คเงื่อนไขให้ครบทุกด่าน
        if selected_board == 'Enchanted Forest' and ForestMap is not None:
            self.game = ForestMap()
        elif selected_board == 'Desert Ruins' and DesertMap is not None:
            self.game = DesertMap()
        elif selected_board == 'Frozen Tundra' and TundraMap is not None:
            self.game = TundraMap()
        else:
            self.game = ChessBoard()
            self.game.bg_image = 'assets/boards/classic.png'
            
        self.selected = None
        
        self.board_area = BoxLayout(orientation='vertical', size_hint_x=0.75)
        self.info_label = Label(text="WHITE'S TURN", size_hint_y=0.1, color=(0.9, 0.8, 0.5, 1), bold=True, font_size='20sp')
        self.board_area.add_widget(self.info_label)
        
        self.container = BoxLayout(orientation='horizontal')
        self.board_area.add_widget(self.container)
        self.main_layout.add_widget(self.board_area)

        self.sidebar = SidebarUI(on_undo_callback=self.on_undo_click, on_quit_callback=self.on_quit)
        self.main_layout.add_widget(self.sidebar)
        self.init_board_ui()

    def on_quit(self):
        self.manager.current = 'setup'

    def init_board_ui(self):
        self.container.clear_widgets()

        if getattr(self, 'game_mode', 'PVP') == 'PVE':
            view_perspective = 'white'
        else:
            view_perspective = self.game.current_turn

        ranks = GridLayout(cols=1, size_hint_x=0.05)
        rank_order = range(8, 0, -1) if view_perspective == 'white' else range(1, 9)
        for i in rank_order:
            ranks.add_widget(Label(text=str(i), color=(0.8, 0.7, 0.4, 1), bold=True))
        self.container.add_widget(ranks)
        
        self.board_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        self.grid = GridLayout(cols=8, rows=8, size_hint=(None, None))
        self.board_anchor.add_widget(self.grid)
        self.container.add_widget(self.board_anchor)
        
        self.board_anchor.bind(size=self._keep_grid_square)

        if hasattr(self.game, 'bg_image') and self.game.bg_image != '':
            with self.grid.canvas.before:
                Color(1, 1, 1, 1)
                self.bg_rect = Rectangle(source=self.game.bg_image, pos=self.grid.pos, size=self.grid.size)
            self.grid.bind(pos=self._update_bg, size=self._update_bg)

        self.squares = {}
        row_order = range(8) if view_perspective == 'white' else range(7, -1, -1)
        col_order = range(8) if view_perspective == 'white' else range(7, -1, -1)
        for r in row_order:
            for c in col_order:
                sq = ChessSquare(row=r, col=c)
                sq.bind(on_release=self.on_square_tap)
                self.grid.add_widget(sq)
                self.squares[(r, c)] = sq
        self.refresh_ui()

    def _keep_grid_square(self, instance, value):
        stretch_ratio = 1.0
        
        h = instance.height
        w = h * stretch_ratio
        
        if w > instance.width:
            w = instance.width
            h = w / stretch_ratio
            
        self.grid.size = (int(w), int(h))

    def _update_bg(self, instance, value):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size

    def refresh_ui(self, legal_moves=[]):
        if self.game.game_result: self.info_label.text = self.game.game_result
        else: self.info_label.text = f"{self.game.current_turn.upper()}'S TURN"
        
        check_pos = self.game.find_king(self.game.current_turn) if self.game.is_in_check(self.game.current_turn) else None
        for (r, c), sq in self.squares.items():
            is_last = (r, c) in self.game.last_move if self.game.last_move else False
            sq.update_square_style(highlight=(self.selected == (r, c)), is_legal=((r,c) in legal_moves), is_check=((r,c) == check_pos), is_last=is_last)
            p = self.game.board[r][c]
            path = f"assets/pieces/classic/{p.color}/{p.__class__.__name__.lower()}.png" if p else None
            sq.set_piece_icon(path)
        self.sidebar.update_history_text(self.game.history.move_text_history)

    def on_undo_click(self):
        if self.game.undo_move():
            self.selected = None
            self.hide_piece_status() # ซ่อน Pop-up ถ้ายกเลิกการเดิน
            self.init_board_ui()

    def on_square_tap(self, instance):
        if self.game.game_result: return
        
        if getattr(self, 'game_mode', 'PVP') == 'PVE' and self.game.current_turn == 'black':
            return

        r, c = instance.row, instance.col
        
        if self.selected is None:
            piece = self.game.board[r][c]
            if piece and piece.color == self.game.current_turn:
                self.selected = (r, c)
                self.refresh_ui(self.game.get_legal_moves((r, c)))
                
                # โชว์ Pop-up ข้อมูลหมากทางด้านขวา เมื่อมีการกดเลือกหมาก
                self.show_piece_status(piece)
        else:
            sr, sc = self.selected
            res = self.game.move_piece(sr, sc, r, c)

            # เช็คสถานะการ CLASH
            if isinstance(res, tuple) and res[0] == "clash":
                _, attacker, defender = res
                self.show_clash_popup(attacker, defender, (sr, sc), (r, c))
                return
            
            if res == "promote":
                self.hide_piece_status() #  ซ่อน Pop-up
                def do_p(cls):
                    self.game.promote_pawn(r, c, cls)
                    pop.dismiss()
                    self.init_board_ui()
                    self.check_ai_turn()
                pop = PromotionPopup(self.game.board[r][c].color, do_p)
                pop.open()
            elif res == True:
                self.selected = None
                self.hide_piece_status() #  ซ่อน Pop-up เมื่อเดินเสร็จ
                self.init_board_ui()
                self.check_ai_turn()
            else:
                self.selected = None
                self.hide_piece_status() #  ซ่อน Pop-up เมื่อกดที่อื่น (ยกเลิกการเลือก)
                self.refresh_ui()

        #  ฟังก์ชันสร้างหน้าต่าง CLASH
    def show_clash_popup(self, attacker, defender, start_pos, end_pos):
        self.hide_piece_status()
        self.cancel_clash()
        
        # ไฮไลท์ช่องบนกระดานให้เห็นว่าใครสู้กับใคร
        self.refresh_ui()
        self.squares[start_pos].update_square_style(highlight=True)
        self.squares[end_pos].update_square_style(is_check=True) # กรอบแดงตรงจุดที่โดนบุก
        self.clash_popup = BoxLayout(orientation='vertical',size_hint=(None, None),size=(260, 320), 
            pos_hint={'right': 0.96, 'center_y': 0.5},
            padding=15,
            spacing=10 )
        
        # พื้นหลัง
        with self.clash_popup.canvas.before:
            Color(0.12, 0.12, 0.15, 0.95) 
            self.clash_popup.bg_rect = Rectangle(pos=self.clash_popup.pos, size=self.clash_popup.size)
        self.clash_popup.bind(pos=self._update_clash_bg, size=self._update_clash_bg)
        
        # ข้อความ Header "CLASH"
        title_lbl = Label(text="CLASH!", bold=True, font_size='28sp', color=(1, 0.2, 0.2, 1), size_hint_y=0.15)
        self.clash_popup.add_widget(title_lbl)
        
        #  พื้นที่แสดงหมาก 2 ตัว 
        combatants_layout = BoxLayout(orientation='horizontal', size_hint_y=0.5)
        
        # ฝ่ายโจมตี (Attacker)
        atk_box = BoxLayout(orientation='vertical')
        atk_img = Image(source=f"assets/pieces/classic/{attacker.color}/{attacker.__class__.__name__.lower()}.png")
        atk_pts = getattr(attacker, 'points', 0)
        atk_flips = getattr(attacker, 'flip_count', 0)
        atk_box.add_widget(atk_img)
        atk_box.add_widget(Label(text=f"Pts: {atk_pts}", font_size='14sp', color=(1, 0.8, 0.2, 1)))
        atk_box.add_widget(Label(text=f"Flips: {atk_flips}", font_size='14sp', color=(0.7, 0.8, 1, 1)))
        
        # ข้อความ VS ตรงกลาง
        vs_lbl = Label(text="VS", bold=True, font_size='24sp', color=(0.8, 0.8, 0.8, 1), size_hint_x=0.4)
        
        # ฝ่ายป้องกัน (Defender)
        def_box = BoxLayout(orientation='vertical')
        def_img = Image(source=f"assets/pieces/classic/{defender.color}/{defender.__class__.__name__.lower()}.png")
        def_pts = getattr(defender, 'points', 0)
        def_flips = getattr(defender, 'flip_count', 0)
        def_box.add_widget(def_img)
        def_box.add_widget(Label(text=f"Pts: {def_pts}", font_size='14sp', color=(1, 0.8, 0.2, 1)))
        def_box.add_widget(Label(text=f"Flips: {def_flips}", font_size='14sp', color=(0.7, 0.8, 1, 1)))

        combatants_layout.add_widget(atk_box)
        combatants_layout.add_widget(vs_lbl)
        combatants_layout.add_widget(def_box)
        
        self.clash_popup.add_widget(combatants_layout)
        
        # พื้นที่ปุ่มกด (แนวตั้ง)
        btn_layout = BoxLayout(orientation='vertical', size_hint_y=0.35, spacing=10, padding=[0, 10, 0, 0])
        
        roll_btn = Button(text="ROLL!", bold=True, font_size='18sp', background_color=(0.8, 0.2, 0.2, 1))
        roll_btn.bind(on_release=lambda x: self.resolve_clash(start_pos, end_pos))
        
        cancel_btn = Button(text="CANCEL", font_size='14sp', background_color=(0.3, 0.3, 0.3, 1))
        cancel_btn.bind(on_release=lambda x: self.cancel_clash(reset_selection=True))
        
        btn_layout.add_widget(roll_btn)
        btn_layout.add_widget(cancel_btn)
        
        self.clash_popup.add_widget(btn_layout)

        self.root_layout.add_widget(self.clash_popup)
        
        # อนิเมชันให้สไลด์เข้ามาจากขวา
        self.clash_popup.x += 30
        self.clash_popup.opacity = 0
        anim = Animation(x=self.clash_popup.x - 30, opacity=1, duration=0.2, t='out_quad')
        anim.start(self.clash_popup)

        #  ฟังก์ชันอัปเดตพื้นหลังของหน้าต่าง Clash
    def _update_clash_bg(self, instance, value):
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size

    #  ฟังก์ชันยกเลิกการต่อสู้ ปิดป๊อปอัป
    def cancel_clash(self, reset_selection=False):
        if self.clash_popup:
            self.root_layout.remove_widget(self.clash_popup)
            self.clash_popup = None
        
        if reset_selection:
            self.selected = None
            self.refresh_ui()

    #  ฟังก์ชันยืนยันการโจมตี
    def resolve_clash(self, start_pos, end_pos):
        self.cancel_clash()
            
        sr, sc = start_pos
        er, ec = end_pos
        
        # สั่ง move แบบ resolve_clash=True คือให้มันกินหมากไปเลย
        res = self.game.move_piece(sr, sc, er, ec, resolve_clash=True)
        
        if res == "promote":
            def do_p(cls):
                self.game.promote_pawn(er, ec, cls)
                pop.dismiss()
                self.init_board_ui()
                self.check_ai_turn()
            pop = PromotionPopup(self.game.board[er][ec].color, do_p)
            pop.open()
        elif res == True:
            self.selected = None
            self.init_board_ui()
            self.check_ai_turn()

    #  ฟังก์ชันแสดง Card/Pop-up โชว์ชื่อและแต้มของหมาก
    def show_piece_status(self, piece):
        self.hide_piece_status()
        # สร้าง Layout ของ Card Pop-up
        self.status_popup = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(220, 100),
            pos_hint={'right': 0.95, 'center_y': 0.5},
            padding=10,
            spacing=10
        )
        
        # วาดพื้นหลัง Card
        with self.status_popup.canvas.before:
            Color(0.15, 0.15, 0.15, 0.95) 
            self.status_popup.bg_rect = Rectangle(pos=self.status_popup.pos, size=self.status_popup.size)
        self.status_popup.bind(pos=self._update_popup_bg, size=self._update_popup_bg)
        img_path = f"assets/pieces/classic/{piece.color}/{piece.__class__.__name__.lower()}.png"
        img = Image(source=img_path, size_hint_x=0.4)
        self.status_popup.add_widget(img)
        text_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        
        # ชื่อหมาก
        name_lbl = Label(text=piece.__class__.__name__.upper(), bold=True, font_size='20sp', halign='left')
        name_lbl.bind(size=name_lbl.setter('text_size'))
        text_layout.add_widget(name_lbl)
        
        # แต้มหมาก
        pts_lbl = Label(text=f"{piece.points} Points", font_size='16sp', color=(1, 0.8, 0.2, 1), halign='left')
        pts_lbl.bind(size=pts_lbl.setter('text_size')) 
        text_layout.add_widget(pts_lbl)

        # จำนวนครั้งการทอย (Flip count)
        # ใช้ getattr เพื่อดึงค่า flip_count ถ้าไม่มีจะตั้งเป็น 0 (กันตัวแปรบั๊กนะจ๊ะ)
        flip_val = getattr(piece, 'flip_count', 0)
        flip_lbl = Label(text=f"Flips: {flip_val}", font_size='14sp', color=(0.7, 0.8, 1, 1), halign='left')
        flip_lbl.bind(size=flip_lbl.setter('text_size'))
        text_layout.add_widget(flip_lbl)
        
        self.status_popup.add_widget(text_layout)
        self.root_layout.add_widget(self.status_popup)
        
        # ทำแอนิเมชันให้การ์ดสไลด์เข้ามานิดหน่อยเพื่อความสมูท
        self.status_popup.x += 20
        self.status_popup.opacity = 0
        anim = Animation(x=self.status_popup.x - 20, opacity=1, duration=0.15)
        anim.start(self.status_popup)

    # ฟังก์ชันอัปเดตพื้นหลัง Pop-up
    def _update_popup_bg(self, instance, value):
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size

    # ฟังก์ชันซ่อนและทำลาย Pop-up
    def hide_piece_status(self):
        if self.status_popup:
            self.root_layout.remove_widget(self.status_popup)
            self.status_popup = None

    def check_ai_turn(self):
        if getattr(self, 'game_mode', 'PVP') == 'PVE' and self.game.current_turn == 'black' and not self.game.game_result:
            Clock.schedule_once(self.trigger_ai_move, 0.8)

    def trigger_ai_move(self, dt):
        move = ChessAI.get_best_move(self.game, ai_color='black')
        if move:
            (sr, sc), (er, ec) = move
            res = self.game.move_piece(sr, sc, er, ec)
            if isinstance(res, tuple) and res[0] == "clash":
                _, attacker, defender = res
                self.show_clash_popup(attacker, defender, (sr, sc), (er, ec))
                return
            
            if res == "promote":
                from logic.pieces import Queen
                self.game.promote_pawn(er, ec, Queen)
            
            self.init_board_ui()