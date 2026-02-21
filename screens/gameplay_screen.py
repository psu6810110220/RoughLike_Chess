# screens/gameplay_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from logic.board import ChessBoard
from components.chess_square import ChessSquare
from components.sidebar_ui import SidebarUI

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
        self.game = ChessBoard()
        self.selected = None
        
        self.board_area = BoxLayout(orientation='vertical', size_hint_x=0.75)
        self.info_label = Label(text="WHITE'S TURN", size_hint_y=0.1, color=(1,1,1,1), bold=True)
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
        ranks = GridLayout(cols=1, size_hint_x=0.05)
        rank_order = range(8, 0, -1) if self.game.current_turn == 'white' else range(1, 9)
        for i in rank_order: ranks.add_widget(Label(text=str(i), color=(1, 1, 1, 1)))
        self.container.add_widget(ranks)
        
        self.grid = GridLayout(cols=8, rows=8)
        self.squares = {}
        row_order = range(8) if self.game.current_turn == 'white' else range(7, -1, -1)
        col_order = range(8) if self.game.current_turn == 'white' else range(7, -1, -1)
        for r in row_order:
            for c in col_order:
                sq = ChessSquare(row=r, col=c)
                sq.bind(on_release=self.on_square_tap)
                self.grid.add_widget(sq)
                self.squares[(r, c)] = sq
        self.container.add_widget(self.grid)
        self.refresh_ui()

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
                    self.init_board_ui() # ✨ เปลี่ยนมาเคลียร์กระดานเฉยๆ ไม่เรียก AI แล้ว
                pop = PromotionPopup(self.game.board[r][c].color, do_p)
                pop.open()
            elif res == True:
                self.selected = None
                self.init_board_ui() # ✨ เปลี่ยนมาเคลียร์กระดานเฉยๆ ไม่เรียก AI แล้ว
            else: 
                self.selected = None
                self.refresh_ui()