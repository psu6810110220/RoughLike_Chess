import os
from PIL import Image, ImageDraw

def create_placeholder(path, color, label):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    # สร้างรูปสี่เหลี่ยม
    img = Image.new('RGBA', (128, 128), color)
    draw = ImageDraw.Draw(img)
    # เขียนตัวอักษรลงไปตรงกลาง (ใช้ตัวย่อชื่อหมาก)
    text_color = (0, 0, 0, 255) if sum(color[:3]) > 400 else (255, 255, 255, 255)
    draw.text((50, 50), label.upper()[:1], fill=text_color) 
    img.save(path)

pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'pawn']
for p in pieces:
    create_placeholder(f"assets/white/{p}.png", (240, 240, 240, 255), p)
    create_placeholder(f"assets/black/{p}.png", (40, 40, 40, 255), p)
print("✅ สร้างหมากแบบมีตัวอักษรเสร็จแล้ว!")