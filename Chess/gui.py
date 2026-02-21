# ไฟล์: gui.py
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Line 
from board import ChessBoard
from components.sidebar_ui import SidebarUI 

class ChessSquare(Button):
    def __init__(self, row, col, **kwargs):
        super().__init__(**kwargs)
        self.row, self.col = row, col
        self.background_normal = '' 
        self.background_down = ''
        self.piece_img = Image(allow_stretch=True, keep_ratio=True, opacity=0)
        self.add_widget(self.piece_img)
        self.is_last_move = False
        self.is_legal = False
        self.update_square_style()
        self.bind(pos=self.sync_layout, size=self.sync_layout)

    def sync_layout(self, *args):
        self.piece_img.size = (self.width * 0.85, self.height * 0.85)
        self.piece_img.center = self.center
        self.canvas.after.clear()
        with self.canvas.after:
            if self.is_legal:
                Color(0.1, 1, 0.1, 1) 
                Line(rectangle=(self.x + 1, self.y + 1, self.width - 2, self.height - 2), width=3)
            elif self.is_last_move:
                Color(1, 0.5, 0, 1) 
                Line(rectangle=(self.x, self.y, self.width, self.height), width=2.5)

    def update_square_style(self, highlight=False, is_legal=False, is_check=False, is_last=False):
        self.is_last_move = is_last
        self.is_legal = is_legal
        if (self.row + self.col) % 2 == 0: self.background_color = (0.94, 0.94, 0.91, 1) 
        else: self.background_color = (0.46, 0.59, 0.74, 1)
        if is_check: self.background_color = (1, 0.2, 0.2, 0.8) 
        elif highlight: self.background_color = (1, 1, 0, 0.6) 
        self.sync_layout()

    def set_piece_icon(self, path):
        if path:
            self.piece_img.source = path
            self.piece_img.opacity = 1
        else: self.piece_img.opacity = 0

class PromotionPopup(ModalView):
    def __init__(self, color, callback, **kwargs):
        super().__init__(size_hint=(0.6, 0.2), auto_dismiss=False, **kwargs)
        layout = GridLayout(cols=4, padding=10, spacing=10)
        from pieces import Queen, Rook, Bishop, Knight
        ops = [Queen, Rook, Bishop, Knight]; names = ['queen', 'rook', 'bishop', 'knight']
        for cls, n in zip(ops, names):
            btn = Button(background_normal=f"assets/{color}/{n}.png")
            btn.bind(on_release=lambda b, c=cls: callback(c))
            layout.add_widget(btn)
        self.add_widget(layout)

class ChessGameUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.game = ChessBoard()
        self.selected = None
        
        self.board_area = BoxLayout(orientation='vertical', size_hint_x=0.75)
        self.info_label = Label(text="WHITE'S TURN", size_hint_y=0.1, color=(1,1,1,1), bold=True)
        self.board_area.add_widget(self.info_label)
        
        self.container = BoxLayout(orientation='horizontal')
        self.board_area.add_widget(self.container)
        self.add_widget(self.board_area)

        self.sidebar = SidebarUI(on_undo_callback=self.on_undo_click)
        self.add_widget(self.sidebar)

        self.init_board_ui()

    def init_board_ui(self):
        """✨ ฟังก์ชันวาดกระดานใหม่ ถูกอัปเกรดให้รองรับการกลับหัว (Flip Board)"""
        self.container.clear_widgets()
        ranks = GridLayout(cols=1, size_hint_x=0.05)
        
        # 1. สลับตัวเลข 1-8 ด้านซ้ายกระดาน
        rank_order = range(8, 0, -1) if self.game.current_turn == 'white' else range(1, 9)
        for i in rank_order: 
            ranks.add_widget(Label(text=str(i), color=(1, 1, 1, 1)))
        self.container.add_widget(ranks)
        
        self.grid = GridLayout(cols=8, rows=8)
        self.squares = {}
        
        # 2. สลับทิศทางการเรียงช่องกระดาน
        # ตาสีขาว: เรียงจากซ้ายไปขวา (0->7), บนลงล่าง (0->7)
        # ตาสีดำ: เรียงจากขวาไปซ้าย (7->0), ล่างขึ้นบน (7->0) เพื่อให้หมากดำมาอยู่ด้านล่าง
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
            sq.set_piece_icon(f"assets/{p.color}/{p.__class__.__name__.lower()}.png" if p else None)
        
        self.sidebar.update_history_text(self.game.history.move_text_history)

    def on_undo_click(self):
        if self.game.undo_move():
            self.selected = None
            # ✨ เมื่อกด Undo เปลี่ยนมาเรียก init_board_ui เพื่อสั่งให้หมุนกระดานกลับด้วย
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
                    self.init_board_ui() # ✨ รีบิลด์เมื่อเปลี่ยนหมากเสร็จ
                pop = PromotionPopup(self.game.board[r][c].color, do_p)
                pop.open()
            elif res == True:
                # ✨ ถ้าเดินสำเร็จ (สลับตาแล้ว) ให้วาดกระดานใหม่เพื่อสลับด้าน
                self.selected = None
                self.init_board_ui()
            else:
                self.selected = None
                self.refresh_ui()

class ChessApp(App):
    def build(self): 
        self.title = "Roguelike Chess - Auto Flip Board"
        return ChessGameUI()

if __name__ == "__main__": ChessApp().run()