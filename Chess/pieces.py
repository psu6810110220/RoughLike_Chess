# ไฟล์: pieces.py

class Piece:
    # แม่แบบของหมากทุกตัว
    def __init__(self, color, name):
        self.color = color  # 'white' หรือ 'black'
        self.name = name    # ตัวอักษรที่จะแสดงบนกระดาน เช่น 'R', 'n'
        
    def is_valid_move(self, start_pos, end_pos, board):
        # ฟังก์ชันนี้จะถูกเขียนทับ (Override) โดยหมากแต่ละชนิด
        pass

class Rook(Piece):
    def __init__(self, color):
        name = 'R' if color == 'white' else 'r'
        super().__init__(color, name)
        
    def is_valid_move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # เดินเส้นตรง
        if start_row == end_row or start_col == end_col:
            step_row = 0 if start_row == end_row else (1 if end_row > start_row else -1)
            step_col = 0 if start_col == end_col else (1 if end_col > start_col else -1)
            
            curr_row, curr_col = start_row + step_row, start_col + step_col
            while curr_row != end_row or curr_col != end_col:
                if board[curr_row][curr_col] is not None:
                    print(f"ผิดกติกา! มีหมากขวางทาง {self.name} อยู่")
                    return False
                curr_row += step_row
                curr_col += step_col
            return True
            
        print(f"ผิดกติกา! {self.name} (เรือ) ต้องเดินเป็นเส้นตรง")
        return False

class Knight(Piece):
    def __init__(self, color):
        name = 'N' if color == 'white' else 'n'
        super().__init__(color, name)
        
    def is_valid_move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        
        # เดินรูปตัว L
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True
            
        print(f"ผิดกติกา! {self.name} (ม้า) ต้องเดินเป็นรูปตัว L")
        return False

class Bishop(Piece):
    def __init__(self, color):
        name = 'B' if color == 'white' else 'b'
        super().__init__(color, name)
        
    def is_valid_move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # เดินแนวทแยง
        if abs(start_row - end_row) == abs(start_col - end_col):
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
            
            curr_row, curr_col = start_row + step_row, start_col + step_col
            while curr_row != end_row and curr_col != end_col:
                if board[curr_row][curr_col] is not None:
                    print(f"ผิดกติกา! มีหมากขวางทาง {self.name} อยู่")
                    return False
                curr_row += step_row
                curr_col += step_col
            return True
            
        print(f"ผิดกติกา! {self.name} (บิชอป) ต้องเดินแนวทแยง")
        return False

class Queen(Piece):
    def __init__(self, color):
        name = 'Q' if color == 'white' else 'q'
        super().__init__(color, name)
        
    def is_valid_move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        is_straight = (start_row == end_row or start_col == end_col)
        is_diagonal = (abs(start_row - end_row) == abs(start_col - end_col))
        
        # ควีน = เดินตรง (เรือ) + เดินเฉียง (บิชอป)
        if is_straight or is_diagonal:
            step_row = 0 if start_row == end_row else (1 if end_row > start_row else -1)
            step_col = 0 if start_col == end_col else (1 if end_col > start_col else -1)
            
            curr_row, curr_col = start_row + step_row, start_col + step_col
            while curr_row != end_row or curr_col != end_col:
                if board[curr_row][curr_col] is not None:
                    print(f"ผิดกติกา! มีหมากขวางทาง {self.name} อยู่")
                    return False
                curr_row += step_row
                curr_col += step_col
            return True
            
        print(f"ผิดกติกา! {self.name} (ควีน) ต้องเดินเป็นเส้นตรงหรือแนวทแยงเท่านั้น")
        return False

class King(Piece):
    def __init__(self, color):
        name = 'K' if color == 'white' else 'k'
        super().__init__(color, name)
        
    def is_valid_move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # คิงเดินได้รอบทิศทาง แต่ไปได้แค่ทีละ 1 ช่อง
        if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
            return True
            
        print(f"ผิดกติกา! {self.name} (คิง) เดินได้แค่ทีละ 1 ช่องรอบตัว")
        return False

class Pawn(Piece):
    def __init__(self, color):
        name = 'P' if color == 'white' else 'p'
        super().__init__(color, name)
        
    def is_valid_move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        target_piece = board[end_row][end_col]
        
        # กำหนดทิศทาง: สีขาวเดินขึ้น (-1), สีดำเดินลง (+1)
        direction = -1 if self.color == 'white' else 1
        # แถวเริ่มต้น: สีขาวเริ่มที่แถว 6, สีดำเริ่มที่แถว 1
        start_row_initial = 6 if self.color == 'white' else 1
        
        # กติกาที่ 1: เดินตรง 1 ช่อง (ช่องเป้าหมายต้องเป็นช่องว่าง)
        if start_col == end_col and end_row == start_row + direction:
            if target_piece is None:
                return True
            else:
                print("ผิดกติกา! เบี้ยเดินตรงไปกินหมากไม่ได้")
                return False
                
        # กติกาที่ 2: เดินตรง 2 ช่อง (ทำได้เฉพาะก้าวแรก และไม่มีอะไรขวาง)
        if start_col == end_col and start_row == start_row_initial and end_row == start_row + (2 * direction):
            if target_piece is None and board[start_row + direction][start_col] is None:
                return True
            else:
                print("ผิดกติกา! มีหมากขวางทาง หรือช่องเป้าหมายไม่ว่าง")
                return False
                
        # กติกาที่ 3: กินเฉียง 1 ช่อง (ต้องมีหมากฝ่ายตรงข้ามอยู่)
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            if target_piece is not None:
                # ระบบสีเดียวกันห้ามกินถูกเช็คใน board.py แล้ว ตรงนี้เลยผ่านได้
                return True
            else:
                print("ผิดกติกา! เบี้ยเดินเฉียงช่องว่างไม่ได้ (ต้องกินเท่านั้น)")
                return False
                
        print(f"ผิดกติกา! {self.name} (เบี้ย) เดินแบบนั้นไม่ได้")
        return False