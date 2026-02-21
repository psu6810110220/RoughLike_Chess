import sys
import os
from pieces import Rook, Knight, Bishop, Queen, King, Pawn

class ChessBoard:
    def __init__(self):
        self.board = self.create_initial_board()
        self.current_turn = 'white'  # เริ่มเกมที่สีขาวเสมอ

    def create_initial_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        # หมากสีดำ (ด้านบนสุด แถวที่ 0 และ 1)
        board[0] = [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')]
        board[1] = [Pawn('black') for _ in range(8)]
        
        # หมากสีขาว (ด้านล่างสุด แถวที่ 6 และ 7)
        board[6] = [Pawn('white') for _ in range(8)]
        board[7] = [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')]
        return board

    def display(self):
        print("\n  0 1 2 3 4 5 6 7")
        print("  ----------------")
        for i, row in enumerate(self.board):
            row_display = [piece.__class__.__name__[:1] if piece else '.' for piece in row]
            print(f"{i}|" + " ".join(row_display))
        print("\n")

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                # เช็คจากชื่อคลาสตรงๆ เพื่อความแม่นยำ
                if p and p.__class__.__name__.lower() == 'king' and p.color == color:
                    return (r, c)
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos: return False

        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            for r in range(8):
                for c in range(8):
                    p = self.board[r][c]
                    if p and p.color != color:
                        if p.is_valid_move((r, c), king_pos, self.board):
                            return True
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color): return False

        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            for r in range(8):
                for c in range(8):
                    p = self.board[r][c]
                    if p and p.color == color:
                        for tr in range(8):
                            for tc in range(8):
                                if p.is_valid_move((r, c), (tr, tc), self.board):
                                    target = self.board[tr][tc]
                                    self.board[r][c] = None
                                    self.board[tr][tc] = p
                                    still_check = self.is_in_check(color)
                                    self.board[r][c] = p
                                    self.board[tr][tc] = target
                                    if not still_check: return False
        finally:
            sys.stdout.close()
            sys.stdout = old_stdout
        return True

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        target = self.board[end_row][end_col]

        # เช็คว่าเป็นตาของตัวเองหรือไม่
        if not piece: return False
        if piece.color != self.current_turn: return False
        
        # เช็คกฎการเดิน
        if target and target.color == piece.color: return False
        if not piece.is_valid_move((start_row, start_col), (end_row, end_col), self.board): return False

        # จำลองการเดิน (Self-Check)
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        is_self_check = self.is_in_check(piece.color)
        
        # คืนค่าก่อน (Rollback)
        self.board[start_row][start_col] = piece
        self.board[end_row][end_col] = target

        if is_self_check:
            print(f"❌ ผิดกติกา! คิงสี {piece.color} จะโดนรุก")
            return False

        # --- เดินจริง ---
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        
        # สลับตาเดิน
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        print(f"✅ ย้ายสำเร็จ! ต่อไปตาของ: {self.current_turn.upper()}")

        # เช็ครุก/รุกฆาต
        enemy = self.current_turn
        if self.is_in_check(enemy):
            if self.is_checkmate(enemy):
                print(f"💀 รุกฆาต!! (CHECKMATE) สี {piece.color} ชนะ!")
            else:
                print(f"🔥 รุก! (Check) คิงสี {enemy} อันตราย!")
        
        return True