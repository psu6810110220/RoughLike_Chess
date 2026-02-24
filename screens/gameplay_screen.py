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
        self.main_layout = BoxLayout(orientation='horizontal')
        self.add_widget(self.main_layout)

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
            self.init_board_ui()

    def on_square_tap(self, instance):
        if self.game.game_result: return 
        
        if getattr(self, 'game_mode', 'PVP') == 'PVE' and self.game.current_turn == 'black':
            return 

        r, c = instance.row, instance.col
        
        if self.selected is None:
            if self.game.board[r][c] and self.game.board[r][c].color == self.game.current_turn:
                self.selected = (r, c)
                self.refresh_ui(self.game.get_legal_moves((r, c)))
        else:
            sr, sc = self.selected
            res = self.game.move_piece(sr, sc, r, c)
            
            if res == "promote":
                def do_p(cls): 
                    self.game.promote_pawn(r, c, cls)
                    pop.dismiss()
                    self.init_board_ui()
                    self.check_ai_turn() 
                pop = PromotionPopup(self.game.board[r][c].color, do_p)
                pop.open()
            elif res == True:
                self.selected = None
                self.init_board_ui()
                self.check_ai_turn() 
            else: 
                self.selected = None
                self.refresh_ui()

    def check_ai_turn(self):
        if getattr(self, 'game_mode', 'PVP') == 'PVE' and self.game.current_turn == 'black' and not self.game.game_result:
            Clock.schedule_once(self.trigger_ai_move, 0.8)

    def trigger_ai_move(self, dt):
        move = ChessAI.get_best_move(self.game, ai_color='black')
        if move:
            (sr, sc), (er, ec) = move
            res = self.game.move_piece(sr, sc, er, ec)
            
            if res == "promote":
                from logic.pieces import Queen
                self.game.promote_pawn(er, ec, Queen)
            
            self.init_board_ui()