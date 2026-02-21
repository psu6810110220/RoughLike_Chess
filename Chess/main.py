# ไฟล์: main.py
from board import ChessBoard

if __name__ == "__main__":
    game = ChessBoard()
    
    print("--- กระดานเริ่มต้น ---")
    game.display()

    print("\n--- ทดสอบที่ 1: เบี้ยขาวตาแรก เดินตรง 2 ช่อง ---")
    game.move_piece(6, 4, 4, 4) 
    game.display()
    
    print("\n--- ทดสอบที่ 2: เบี้ยดำตาแรก เดินตรง 2 ช่อง (มาจ๊ะเอ๋กันพอดี) ---")
    game.move_piece(1, 4, 3, 4) 
    game.display()
    
    print("\n--- ทดสอบที่ 3: เบี้ยขาวพยายามเดินชนเบี้ยดำตรงๆ (ต้องผิดกติกา) ---")
    game.move_piece(4, 4, 3, 4) 
    game.display()

    print("\n--- ทดสอบที่ 4: เบี้ยขาวกินเฉียง (เราจะขยับเบี้ยดำอีกตัวมาให้กิน) ---")
    game.move_piece(1, 3, 3, 3) # ขยับเบี้ยดำอีกตัวลงมา
    game.move_piece(4, 4, 3, 3) # สั่งเบี้ยขาวกินเฉียง!
    game.display()