from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from board import ChessBoard

class ChessSquare(Button):
    def __init__(self, row, col, **kwargs):
        super().__init__(**kwargs)
        self.row = row
        self.col = col
        self.background_normal = '' 
        self.background_down = ''
        self.update_color()

        # สร้าง Image ฝังไว้ในปุ่มเลย (ตอนแรกยังไม่โชว์รูป)
        self.piece_img = Image(allow_stretch=True, keep_ratio=True, opacity=0)
        self.add_widget(self.piece_img)

        # ผูกตำแหน่งและขนาดของรูป ให้ขยายและขยับตามปุ่มเสมอ
        self.bind(pos=self.update_img_pos_size, size=self.update_img_pos_size)

    def update_img_pos_size(self, *args):
        """จัดตำแหน่งรูปหมากให้อยู่ตรงกลางและมีขนาดพอดีกับช่อง"""
        margin_x = self.width * 0.075
        margin_y = self.height * 0.075
        self.piece_img.size = (self.width * 0.85, self.height * 0.85)
        self.piece_img.pos = (self.x + margin_x, self.y + margin_y)

    def update_color(self, highlight=False):
        if highlight:
            self.background_color = (1, 0.9, 0.3, 0.6)  # สีเหลืองไฮไลต์
        elif (self.row + self.col) % 2 == 0:
            self.background_color = (0.93, 0.93, 0.85, 1)  # สีครีม
        else:
            self.background_color = (0.46, 0.58, 0.34, 1)  # สีเขียวมะกอก

    def set_piece(self, img_path):
        """อัปเดตรูปภาพหมากในช่องนี้"""
        if img_path:
            self.piece_img.source = img_path
            self.piece_img.opacity = 1  # โชว์รูป
        else:
            self.piece_img.opacity = 0  # ซ่อนรูปถ้าไม่มีหมาก

class ChessGameUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.game = ChessBoard()
        self.selected_square = None
        
        self.board_container = BoxLayout(orientation='horizontal')
        self.create_ui()
        self.add_widget(self.board_container)

    def create_ui(self):
        # แถบตัวเลข 8-1 ด้านซ้าย
        ranks = GridLayout(cols=1, size_hint_x=0.05)
        for i in range(8, 0, -1):
            ranks.add_widget(Label(text=str(i), color=(0.2, 0.2, 0.2, 1)))
        self.board_container.add_widget(ranks)

        # สร้างตาราง 8x8
        self.grid = GridLayout(cols=8, rows=8)
        self.squares = {}
        for r in range(8):
            for c in range(8):
                square = ChessSquare(row=r, col=c)
                square.bind(on_release=self.on_square_click)
                self.grid.add_widget(square)
                self.squares[(r, c)] = square
        
        self.board_container.add_widget(self.grid)
        self.update_board_ui()

    def update_board_ui(self):
        """วาดกระดานและอัปเดตหมากใหม่ทั้งหมด"""
        for (r, c), square in self.squares.items():
            square.update_color(highlight=(self.selected_square == (r, c)))
            
            piece = self.game.board[r][c]
            if piece:
                piece_name = piece.__class__.__name__.lower()
                img_path = f"assets/{piece.color}/{piece_name}.png"
                square.set_piece(img_path)
            else:
                square.set_piece(None)

    def on_square_click(self, instance):
        r, c = instance.row, instance.col
        
        if self.selected_square is None:
            if self.game.board[r][c] and self.game.board[r][c].color == self.game.current_turn:
                self.selected_square = (r, c)
            elif self.game.board[r][c]:
                print(f"❌ ยังไม่ใช่ตาของสี {self.game.board[r][c].color}!")
        else:
            start_r, start_c = self.selected_square
            self.game.move_piece(start_r, start_c, r, c)
            self.selected_square = None
        
        self.update_board_ui()

class ChessApp(App):
    def build(self):
        self.title = "Roguelike Chess - Pro Edition"
        return ChessGameUI()

if __name__ == "__main__":
    ChessApp().run()