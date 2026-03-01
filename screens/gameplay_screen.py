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
    # ✨ ลบ parameter theme ออก เพราะเราจะให้ Popup ดึงค่าเองตามสี (color)
    def __init__(self, color, callback, **kwargs):
        super().__init__(size_hint=(0.6, 0.2), auto_dismiss=False, **kwargs)
        layout = GridLayout(cols=4, padding=10, spacing=10)
        from logic.pieces import Queen, Rook, Bishop, Knight
        ops = [Queen, Rook, Bishop, Knight]
        names = ['queen', 'rook', 'bishop', 'knight']
        
        # ✨ ดึง Theme ตามสีที่ได้โปรโมท
        app = App.get_running_app()
        if color == 'white':
            theme = getattr(app, 'selected_unit_white', 'Medieval Knights')
        else:
            theme = getattr(app, 'selected_unit_black', 'Demon')
        
        for cls, n in zip(ops, names):
            if theme == "Ayothaya":
                mapping = {'queen': 'chess ayothaya2.png', 'rook': 'chess ayothaya3.png', 'bishop': 'chess ayothaya5.png', 'knight': 'chess ayothaya4.png'}
                path = f"assets/pieces/ayothaya/{color}/{mapping[n]}"
            elif theme == "Demon":
                mapping = {'queen': 'chess demon2.png', 'rook': 'chess demon3.png', 'bishop': 'chess demon5.png', 'knight': 'chess demon4.png'}
                path = f"assets/pieces/demon/{color}/{mapping[n]}"
            elif theme == "Heaven":
                mapping = {'queen': 'chess heaven2.png', 'rook': 'chess heaven3.png', 'bishop': 'chess heaven5.png', 'knight': 'chess heaven4.png'}
                path = f"assets/pieces/heaven/{color}/{mapping[n]}"
            else:
                mapping = {'queen': 'chess medieval2.png', 'rook': 'chess medieval3.png', 'bishop': 'chess medieval5.png', 'knight': 'chess medieval4.png'}
                path = f"assets/pieces/medieval/{color}/{mapping[n]}"

            btn = Button(background_normal=path)
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
        self.crash_popup = None # ✨ เปลี่ยนตัวแปรจาก clash เป็น crash

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

    def get_piece_image_path(self, piece):
        """✨ ฟังก์ชันสำหรับดึง Path รูปภาพหมากตามเผ่า (Theme) แบบแยกสี White/Black"""
        app = App.get_running_app()
        p_color = piece.color
        p_name = piece.__class__.__name__.lower()
        
        # ✨ เช็คสีของหมาก เพื่อดึง Theme ให้ตรงกับฝ่ายนั้น
        if p_color == 'white':
            theme = getattr(app, 'selected_unit_white', 'Medieval Knights')
        else:
            theme = getattr(app, 'selected_unit_black', 'Demon')
        
        if theme == "Ayothaya":
            mapping = {
                'king': 'chess ayothaya1.png', 'queen': 'chess ayothaya2.png',
                'rook': 'chess ayothaya3.png', 'knight': 'chess ayothaya4.png',
                'bishop': 'chess ayothaya5.png', 'pawn': 'chess ayothaya6.png'
            }
            filename = mapping.get(p_name, 'chess ayothaya6.png')
            return f"assets/pieces/ayothaya/{p_color}/{filename}"
        elif theme == "Demon":
            mapping = {
                'king': 'chess demon1.png', 'queen': 'chess demon2.png',
                'rook': 'chess demon3.png', 'knight': 'chess demon4.png',
                'bishop': 'chess demon5.png', 'pawn': 'chess demon6.png'
            }
            filename = mapping.get(p_name, 'chess demon6.png')
            return f"assets/pieces/demon/{p_color}/{filename}"
        elif theme == "Heaven":
            mapping = {
                'king': 'chess heaven1.png', 'queen': 'chess heaven2.png',
                'rook': 'chess heaven3.png', 'knight': 'chess heaven4.png',
                'bishop': 'chess heaven5.png', 'pawn': 'chess heaven6.png'
            }
            filename = mapping.get(p_name, 'chess heaven6.png')
            return f"assets/pieces/heaven/{p_color}/{filename}"
        else:
            mapping = {
                'king': 'chess medieval1.png', 'queen': 'chess medieval2.png',
                'rook': 'chess medieval3.png', 'knight': 'chess medieval4.png',
                'bishop': 'chess medieval5.png', 'pawn': 'chess medieval6.png'
            }
            filename = mapping.get(p_name, 'chess medieval6.png')
            return f"assets/pieces/medieval/{p_color}/{filename}"

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
            
            # ✨ แก้ไขบรรทัดดึง path รูปภาพโดยเรียกใช้ฟังก์ชันใหม่
            path = self.get_piece_image_path(p) if p else None
            
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

            # ✨ เช็คสถานะการ CRASH
            if isinstance(res, tuple) and res[0] == "crash":
                _, attacker, defender = res
                self.show_crash_popup(attacker, defender, (sr, sc), (r, c))
                return
            
            if res == "promote":
                self.hide_piece_status() #  ซ่อน Pop-up
                def do_p(cls):
                    self.game.promote_pawn(r, c, cls)
                    pop.dismiss()
                    self.init_board_ui()
                    self.check_ai_turn()
                # ✨ ลบการดึง theme เพราะ PromotionPopup เช็คจากสีเองได้แล้ว
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

# ✨ ฟังก์ชันสร้างหน้าต่าง CRASH (อัปเดตหน้าตาใหม่)
    def show_crash_popup(self, attacker, defender, start_pos, end_pos):
        self.hide_piece_status()
        self.cancel_crash()
        # ✨ เพิ่มบรรทัดนี้: รีเซ็ตจำนวนครั้งการติด Stagger เมื่อเริ่ม Crash ครั้งแรก
        self.crash_stagger_count = 0
        
        # ไฮไลท์ช่องบนกระดาน
        self.refresh_ui()
        self.squares[start_pos].update_square_style(highlight=True)
        self.squares[end_pos].update_square_style(is_check=True)
        
        # ขยายขนาด Popup เล็กน้อยเพื่อรองรับพื้นที่เหรียญ
        self.crash_popup = BoxLayout(orientation='vertical', size_hint=(None, None), size=(340, 400), 
            pos_hint={'right': 0.96, 'center_y': 0.5},
            padding=15,
            spacing=10)
        
        with self.crash_popup.canvas.before:
            Color(0.12, 0.12, 0.15, 0.95) 
            self.crash_popup.bg_rect = Rectangle(pos=self.crash_popup.pos, size=self.crash_popup.size)
        self.crash_popup.bind(pos=self._update_crash_bg, size=self._update_crash_bg)
        
        title_lbl = Label(text="CRASH!", bold=True, font_size='28sp', color=(1, 0.2, 0.2, 1), size_hint_y=0.15)
        self.crash_popup.add_widget(title_lbl)
        
        combatants_layout = BoxLayout(orientation='horizontal', size_hint_y=0.55)
        
        # === ฝ่ายโจมตี (Attacker) ===
        atk_box = BoxLayout(orientation='vertical', spacing=5)
        atk_img = Image(source=self.get_piece_image_path(attacker), size_hint_y=0.4)
        atk_pts = getattr(attacker, 'base_points', 5)
        atk_coins = getattr(attacker, 'coins', 3)
        atk_box.add_widget(atk_img)
        
        # ข้อมูล point (ห้ามแก้ไข)
        atk_box.add_widget(Label(text=f"point : {atk_pts}", font_size='14sp', color=(1, 0.8, 0.2, 1), size_hint_y=0.15))
        
        # ข้อมูล coin (แสดงทีละเหรียญ)
        atk_coin_row = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        atk_coin_row.add_widget(Label(text="coin : ", font_size='14sp', size_hint_x=0.4))
        self.atk_coin_labels = []
        for _ in range(atk_coins):
            lbl = Label(text="0", font_size='16sp', bold=True, color=(0.5, 0.5, 0.5, 1))
            atk_coin_row.add_widget(lbl)
            self.atk_coin_labels.append(lbl)
        atk_box.add_widget(atk_coin_row)
        
        # ข้อมูล crash รวม
        self.atk_total_lbl = Label(text=f"crash : {atk_pts}", font_size='16sp', color=(1, 0.4, 0.4, 1), bold=True, size_hint_y=0.2)
        atk_box.add_widget(self.atk_total_lbl)
        
        self.vs_lbl = Label(text="VS", bold=True, font_size='24sp', color=(0.8, 0.8, 0.8, 1), size_hint_x=0.4, halign="center")
        
        # === ฝ่ายป้องกัน (Defender) ===
        def_box = BoxLayout(orientation='vertical', spacing=5)
        def_img = Image(source=self.get_piece_image_path(defender), size_hint_y=0.4)
        def_pts = getattr(defender, 'base_points', 5)
        def_coins = getattr(defender, 'coins', 3)
        def_box.add_widget(def_img)
        
        # ข้อมูล point (ห้ามแก้ไข)
        def_box.add_widget(Label(text=f"point : {def_pts}", font_size='14sp', color=(1, 0.8, 0.2, 1), size_hint_y=0.15))
        
        # ข้อมูล coin (แสดงทีละเหรียญ)
        def_coin_row = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        def_coin_row.add_widget(Label(text="coin : ", font_size='14sp', size_hint_x=0.4))
        self.def_coin_labels = []
        for _ in range(def_coins):
            lbl = Label(text="0", font_size='16sp', bold=True, color=(0.5, 0.5, 0.5, 1))
            def_coin_row.add_widget(lbl)
            self.def_coin_labels.append(lbl)
        def_box.add_widget(def_coin_row)
        
        # ข้อมูล crash รวม
        self.def_total_lbl = Label(text=f"crash : {def_pts}", font_size='16sp', color=(0.4, 0.4, 1, 1), bold=True, size_hint_y=0.2)
        def_box.add_widget(self.def_total_lbl)
        
        combatants_layout.add_widget(atk_box)
        combatants_layout.add_widget(self.vs_lbl)
        combatants_layout.add_widget(def_box)
        
        self.crash_popup.add_widget(combatants_layout)
        
        btn_layout = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=10, padding=[0, 10, 0, 0])
        
        # ปุ่มกดเริ่มทอยเหรียญ (เปลี่ยนจาก resolve_crash_ui เป็น start_crash_animation)
        self.crash_btn = Button(text="CRASH!", bold=True, font_size='18sp', background_color=(0.8, 0.2, 0.2, 1))
        self.crash_btn.bind(on_release=lambda x: self.start_crash_animation(start_pos, end_pos))
        
        self.cancel_btn = Button(text="CANCEL", font_size='14sp', background_color=(0.3, 0.3, 0.3, 1))
        self.cancel_btn.bind(on_release=lambda x: self.cancel_crash(reset_selection=True))
        
        btn_layout.add_widget(self.crash_btn)
        btn_layout.add_widget(self.cancel_btn)
        
        self.crash_popup.add_widget(btn_layout)
        self.root_layout.add_widget(self.crash_popup)
        
        self.crash_popup.x += 30
        self.crash_popup.opacity = 0
        anim = Animation(x=self.crash_popup.x - 30, opacity=1, duration=0.2, t='out_quad')
        anim.start(self.crash_popup)

    # ✨ ฟังก์ชันอัปเดตพื้นหลังของหน้าต่าง Crash
    def _update_crash_bg(self, instance, value):
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size

    # ✨ ฟังก์ชันยกเลิกการต่อสู้ ปิดป๊อปอัป
    def cancel_crash(self, reset_selection=False):
        if hasattr(self, 'spin_event') and self.spin_event:
            self.spin_event.cancel()
        if self.crash_popup:
            self.root_layout.remove_widget(self.crash_popup)
            self.crash_popup = None
        
        if reset_selection:
            self.selected = None
            self.refresh_ui()

    # ✨ ชุดฟังก์ชันใหม่สำหรับจัดการ Animation หมุนตัวเลข
    def start_crash_animation(self, start_pos, end_pos):
        self.crash_btn.disabled = True
        self.cancel_btn.disabled = True

        sr, sc = start_pos
        er, ec = end_pos
        attacker = self.game.board[sr][sc]
        defender = self.game.board[er][ec]

        a_base = getattr(attacker, 'base_points', 5)
        a_coins = getattr(attacker, 'coins', 3)
        d_base = getattr(defender, 'base_points', 5)
        d_coins = getattr(defender, 'coins', 3)

        # สุ่มผลลัพธ์ล่วงหน้าเพื่อให้แอนิเมชันวิ่งไปหาคำตอบที่ถูกต้อง
        from logic.crash_logic import calculate_total_points
        
        # ✨ ดึงค่า Theme/Faction ของทั้งสองฝ่าย
        app = App.get_running_app()
        def get_faction_name(color):
            theme = getattr(app, f'selected_unit_{color}', 'Medieval Knights')
            if theme == "Ayothaya": return "ayothaya"
            elif theme == "Demon": return "demon"
            elif theme == "Heaven": return "heaven"
            return "medieval"
            
        a_faction = get_faction_name(attacker.color)
        d_faction = get_faction_name(defender.color)

        # ✨ ส่ง a_faction และ d_faction เข้าไปด้วย
        self.a_final_total, self.a_results = calculate_total_points(a_base, a_coins, a_faction)
        self.d_final_total, self.d_results = calculate_total_points(d_base, d_coins, d_faction)

        # ✨ รีเซ็ตข้อความ UI เหรียญให้เป็นค่าเริ่มต้น เพื่อรองรับการทอยซ้ำหลายๆ รอบ
        self.atk_total_lbl.text = f"crash : {a_base}"
        self.def_total_lbl.text = f"crash : {d_base}"
        for lbl in self.atk_coin_labels:
            lbl.text = "0"
            lbl.color = (0.5, 0.5, 0.5, 1)
        for lbl in self.def_coin_labels:
            lbl.text = "0"
            lbl.color = (0.5, 0.5, 0.5, 1)

        # แปลงข้อความเป็นค่าตัวเลข เพื่อนำไปโชว์ในช่อง coin
        def get_pt(res_str, faction):
            if "เขียว" in res_str: return 100
            if "ฟ้า" in res_str: return 10
            if "ม่วง" in res_str: return 6
            if "ส้ม" in res_str: return 4
            if "น้ำเงิน" in res_str: return 3
            if "แดง" in res_str: return 2
            if "เหลือง" in res_str: return 1
            if "ก้อย" in res_str and faction == "demon": return -3
            return 0

        self.a_pts_array = [get_pt(r, a_faction) for r in self.a_results]
        self.d_pts_array = [get_pt(r, d_faction) for r in self.d_results]

        self.a_pts_array = [get_pt(r) for r in self.a_results]
        self.d_pts_array = [get_pt(r) for r in self.d_results]

        # เก็บรอบของ Animation
        self.anim_state = {
            'side': 'atk',
            'coin_idx': 0,
            'ticks': 0,
            'max_ticks': 15, # ความยาวของการหมุนต่อ 1 เหรียญ
            'a_current_total': a_base,
            'd_current_total': d_base,
            'start_pos': start_pos,
            'end_pos': end_pos,
            'attacker': attacker,
            'defender': defender,
            'attacker_died': False # ✨ บันทึกสถานะว่าโดนตาย (Distortion) หรือไม่
        }

        # เรียก Clock ให้หมุนเลขทุกๆ 0.05 วินาที
        self.spin_event = Clock.schedule_interval(self.animate_coin_step, 0.05)

    def animate_coin_step(self, dt):
        import random
        state = self.anim_state
        side = state['side']
        idx = state['coin_idx']

        # เช็คว่ากำลังแอนิเมทฝั่งไหน
        if side == 'atk':
            labels = self.atk_coin_labels
            final_pts = self.a_pts_array
            if idx >= len(final_pts):
                state['side'] = 'def' # สลับไปฝั่งกัน
                state['coin_idx'] = 0
                return
        else:
            labels = self.def_coin_labels
            final_pts = self.d_pts_array
            if idx >= len(final_pts):
                # จบแอนิเมชัน
                self.spin_event.cancel()
                self.finish_crash_animation()
                return

        target_val = final_pts[idx]
        lbl = labels[idx]

        if state['ticks'] < state['max_ticks']:
            # หมุนเลขหลอกๆ ให้ดูมีความพยายามตามเผ่า
            choices = [0, 1]
            if target_val in [2, 3]: choices = [1, 2, 3]
            elif target_val in [10, 100]: choices = [0, 10, 100]
            elif target_val in [-3, 4, 6]: choices = [-3, 4, 6]
            
            lbl.text = str(random.choice(choices))
            lbl.color = (1, 1, 1, 1)
            state['ticks'] += 1
        else:
            # จบรอบเหรียญ ยึดค่าจริง!
            lbl.text = str(target_val)
            
            # เอฟเฟกต์สีและการเด้งเมื่อติดคริติคอล
            if target_val <= 0:
                lbl.color = (0.5, 0.5, 0.5, 1) # เทา (0 หรือ -3)
            elif target_val == 1:
                lbl.color = (1, 1, 0.2, 1) # เหลือง
            elif target_val == 2:
                lbl.color = (1, 0.2, 0.2, 1) # แดง
                anim = Animation(font_size=24, duration=0.1) + Animation(font_size=16, duration=0.1)
                anim.start(lbl)
            elif target_val == 3:
                lbl.color = (0.2, 0.5, 1, 1) # น้ำเงิน
                anim = Animation(font_size=24, duration=0.1) + Animation(font_size=16, duration=0.1)
                anim.start(lbl)
            elif target_val == 4:
                lbl.color = (1, 0.6, 0.2, 1) # ส้ม
            elif target_val == 6:
                lbl.color = (0.6, 0.2, 1, 1) # ม่วง
                anim = Animation(font_size=24, duration=0.1) + Animation(font_size=16, duration=0.1)
                anim.start(lbl)
            elif target_val == 10:
                lbl.color = (0.4, 0.8, 1, 1) # ฟ้า
            elif target_val == 100:
                lbl.color = (0.2, 1, 0.2, 1) # เขียว
                anim = Animation(font_size=24, duration=0.1) + Animation(font_size=16, duration=0.1)
                anim.start(lbl)

            # บวกเลขลงช่อง crashรวม
            if side == 'atk':
                state['a_current_total'] += target_val
                self.atk_total_lbl.text = f"crash : {state['a_current_total']}"
            else:
                state['d_current_total'] += target_val
                self.def_total_lbl.text = f"crash : {state['d_current_total']}"

            # เตรียมเหรียญต่อไป
            state['coin_idx'] += 1
            state['ticks'] = 0

    def finish_crash_animation(self):
        a_tot = self.anim_state['a_current_total']
        d_tot = self.anim_state['d_current_total']

        if a_tot > d_tot:
            # ✨ โจมตีสำเร็จ
            result_text = "[color=00ff00]BREAKING[/color]"
            self.vs_lbl.text = result_text
            self.vs_lbl.font_size = '20sp'
            self.vs_lbl.markup = True
            Clock.schedule_once(self.execute_board_move, 1.5)
            
        elif a_tot == d_tot:
            # ✨ 1. เสมอ (Draw): วนลูปการทอยใหม่โดยอัตโนมัติ
            result_text = "[color=ffff00]DRAW[/color]"
            self.vs_lbl.text = result_text
            self.vs_lbl.font_size = '20sp'
            self.vs_lbl.markup = True
            
            # รันการต่อสู้ใหม่อีกครั้งหลังจากแสดงผล 1.5 วิ
            Clock.schedule_once(lambda dt: self.start_crash_animation(self.anim_state['start_pos'], self.anim_state['end_pos']), 1.5)
            
        else:
            # ✨ 2. โจมตีพลาด (a_tot < d_tot) 
            self.crash_stagger_count += 1
            if self.crash_stagger_count < 2:
                # พลาดครั้งแรก ให้ติดสถานะ STAGGER และทำการทอยสู้ต่อ
                result_text = "[color=ff8800]STAGGER[/color]" 
                self.vs_lbl.text = result_text
                self.vs_lbl.font_size = '20sp'
                self.vs_lbl.markup = True
                
                # รันการต่อสู้ใหม่อีกครั้ง
                Clock.schedule_once(lambda dt: self.start_crash_animation(self.anim_state['start_pos'], self.anim_state['end_pos']), 1.5)
            else:
                # พลาดครั้งที่สอง ติดสถานะ DISTORTION (หมากตาย)
                result_text = "[color=ff0000]DISTORTION[/color]" 
                self.vs_lbl.text = result_text
                self.vs_lbl.font_size = '20sp'
                self.vs_lbl.markup = True
                
                # ทำเครื่องหมายให้ตัวโจมตีตายและส่งผลให้กระดานทำงานต่อ
                self.anim_state['attacker_died'] = True 
                Clock.schedule_once(self.execute_board_move, 1.5)

    def execute_board_move(self, dt):
        start_pos = self.anim_state['start_pos']
        end_pos = self.anim_state['end_pos']
        
        # ✨ เพิ่มบรรทัดนี้: ดึงสถานะการตายออกมาจาก anim_state (ถ้าไม่มีค่าให้เป็น False)
        attacker_died = self.anim_state.get('attacker_died', False) 
        
        a_tot = self.anim_state['a_current_total']
        d_tot = self.anim_state['d_current_total']

        sr, sc = start_pos
        er, ec = end_pos

        is_attacker_won = (a_tot > d_tot)

        self.cancel_crash() # ปิดหน้าต่าง

        # ส่งสถานะ crash ลงไปที่ logic: ถ้าตายให้ค่าเป็น "died" ถ้าสู้จบให้เป็น boolean ชนะ/แพ้ปกติ
        crash_status = "died" if attacker_died else is_attacker_won
        
        # ดำเนินการลบหมากหรือเดินหมากจาก Logic กระดาน
        res = self.game.move_piece(sr, sc, er, ec, resolve_crash=True, crash_won=crash_status)

        if res == "promote":
            def do_p(cls):
                self.game.promote_pawn(end_pos[0], end_pos[1], cls)
                pop.dismiss()
                self.init_board_ui()
                self.check_ai_turn()
            # ✨ ลบการดึง theme แบบเก่าออก
            pop = PromotionPopup(self.game.board[end_pos[0]][end_pos[1]].color, do_p)
            pop.open()
            
        elif res == True:
            # เดินสำเร็จ (กินได้)
            self.selected = None
            self.init_board_ui()
            self.check_ai_turn()
            
        elif res == "died":
            # อัปเดต UI เมื่อหมากฝั่งบุกตาย
            self.selected = None
            self.init_board_ui()
            self.check_ai_turn()
            
        else:
            # เดินไม่สำเร็จ (ถูกถอยกลับจากการโจมตี)
            self.selected = None
            self.refresh_ui()
            self.check_ai_turn()

    # ✨ ฟังก์ชันแสดง Card/Pop-up โชว์ชื่อและแต้มของหมาก (อัปเดตเป็น base_points และ coins)
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
        
        img_path = self.get_piece_image_path(piece)
        img = Image(source=img_path, size_hint_x=0.4)
        self.status_popup.add_widget(img)
        text_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        
        # ชื่อหมาก
        name_lbl = Label(text=piece.__class__.__name__.upper(), bold=True, font_size='20sp', halign='left')
        name_lbl.bind(size=name_lbl.setter('text_size'))
        text_layout.add_widget(name_lbl)
        
        # แต้มหมาก
        p_base = getattr(piece, 'base_points', 5)
        pts_lbl = Label(text=f"{p_base} Points", font_size='16sp', color=(1, 0.8, 0.2, 1), halign='left')
        pts_lbl.bind(size=pts_lbl.setter('text_size')) 
        text_layout.add_widget(pts_lbl)

        # จำนวนเหรียญที่มี
        p_coins = getattr(piece, 'coins', 3)
        coins_lbl = Label(text=f"Coins: {p_coins}", font_size='14sp', color=(0.7, 0.8, 1, 1), halign='left')
        coins_lbl.bind(size=coins_lbl.setter('text_size'))
        text_layout.add_widget(coins_lbl)
        
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

    # ✨ ให้บอทสุ่มผล Crash ไปเลยโดยอัตโนมัติ
    def trigger_ai_move(self, dt):
        move = ChessAI.get_best_move(self.game, ai_color='black')
        if move:
            (sr, sc), (er, ec) = move
            res = self.game.move_piece(sr, sc, er, ec)
            
            if isinstance(res, tuple) and res[0] == "crash":
                _, attacker, defender = res
                a_base = getattr(attacker, 'base_points', 5)
                a_coins = getattr(attacker, 'coins', 3)
                d_base = getattr(defender, 'base_points', 5)
                d_coins = getattr(defender, 'coins', 3)
                
                from logic.crash_logic import calculate_total_points
                
                stagger_count = 0
                is_attacker_won = False
                attacker_died = False
                
                # ✨ ดึงค่า Faction สำหรับ AI (เหมือนกับจุดที่ 1)
                app = App.get_running_app()
                def get_faction_name(color):
                    theme = getattr(app, f'selected_unit_{color}', 'Medieval Knights')
                    if theme == "Ayothaya": return "ayothaya"
                    elif theme == "Demon": return "demon"
                    elif theme == "Heaven": return "heaven"
                    return "medieval"
                
                a_faction = get_faction_name(attacker.color)
                d_faction = get_faction_name(defender.color)

                # ✨ ลูปวนหาผลลัพธ์ของ AI (จำลองการ Draw และ Stagger)
                while True:
                    a_tot, _ = calculate_total_points(a_base, a_coins, a_faction)
                    d_tot, _ = calculate_total_points(d_base, d_coins, d_faction)
                    
                    if a_tot > d_tot:
                        is_attacker_won = True
                        break
                    elif a_tot == d_tot:
                        continue # Draw: รันวงจรใหม่
                    else:
                        stagger_count += 1
                        if stagger_count >= 2:
                            attacker_died = True
                            break # Stagger ครบ 2 ครั้ง ตาย(Distortion)
                
                # ✨ ส่งผลลัพธ์ลงไป
                crash_status = "died" if attacker_died else is_attacker_won
                res = self.game.move_piece(sr, sc, er, ec, resolve_crash=True, crash_won=crash_status)
            
            if res == "promote":
                from logic.pieces import Queen
                self.game.promote_pawn(er, ec, Queen)
            
            self.init_board_ui()