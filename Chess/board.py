# ไฟล์: board.py
from pieces import Rook, Knight, Bishop, Queen, King, Pawn

class ChessBoard:
    def __init__(self):
        self.board = self.create_initial_board()

    def create_initial_board(self):
        # สร้างตาราง 8x8 ใส่ None (ช่องว่าง) ไว้ก่อน
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # จัดวางหมากสีดำ (แถว 0 และ 1)
        board[0] = [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')]
        board[1] = [Pawn('black') for _ in range(8)]
        
        # จัดวางหมากสีขาว (แถว 6 และ 7)
        board[6] = [Pawn('white') for _ in range(8)]
        board[7] = [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')]
        
        return board

    def display(self):
        print("\n  0 1 2 3 4 5 6 7")
        print("  ----------------")
        for i, row in enumerate(self.board):
            # ถ้ามีหมาก ให้ดึงชื่อ (piece.name) มาโชว์, ถ้าเป็น None ให้โชว์ '.'
            row_display = [piece.name if piece is not None else '.' for piece in row]
            print(f"{i}|" + " ".join(row_display))
        print("\n")

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        target_piece = self.board[end_row][end_col]

        # 1. เช็คว่าช่องที่เลือกมีหมากไหม
        if piece is None:
            print("ไม่มีหมากในช่องเริ่มต้น!")
            return False

        # 2. กฎสากล: ห้ามกินพวกเดียวกัน
        if target_piece is not None and piece.color == target_piece.color:
            print(f"ผิดกติกา! {piece.name} กิน {target_piece.name} ไม่ได้ เพราะสี {piece.color} เหมือนกัน")
            return False

        # 3. โยนหน้าที่ให้ตัวหมากเป็นคนเช็คกติกาการเดินของมันเอง
        # ส่งตำแหน่งเริ่มต้น, เป้าหมาย และสถานะกระดานไปให้มันคำนวณ
        if not piece.is_valid_move((start_row, start_col), (end_row, end_col), self.board):
            return False

        # 4. ถ้าย้ายได้ ให้ลบช่องเดิม และเอาหมากไปใส่ช่องใหม่
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        
        print(f"ย้าย {piece.name} สำเร็จ! จาก ({start_row},{start_col}) ไป ({end_row},{end_col})")
        return True