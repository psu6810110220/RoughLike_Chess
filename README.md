ROGUELIKE CHESS (Enter the Dark Battlefield)
ROGUELIKE CHESS คือเกมหมากรุกที่ผสมผสานองค์ประกอบของแนว Roguelike เข้าไปอย่างลงตัว โดยมีการเพิ่มระบบเผ่าพันธุ์ (Tribes), ด่าน (Maps), ระบบไอเทม (Items), และการต่อสู้ที่ต้องใช้ค่าสถานะจริงในการตัดสินผล (Crash System)

Key Features
4 Strategic Battlefields: เลือกสนามรบได้ 4 รูปแบบ ได้แก่ Classic, Enchanted Forest, Desert Ruins และ Frozen Tundra ซึ่งแต่ละด่านจะมีธีมที่แตกต่างกัน

Divine Order & Dark Abyss (Tribes): ระบบเผ่าพันธุ์ที่มีให้เลือกถึง 4 เผ่า ได้แก่ Medieval Knights, Ayothaya, Demon และ Heaven โดยแต่ละเผ่าจะให้ความรู้สึกและคุณสมบัติที่ต่างกัน

Combat & Crash System: การกินหมากไม่ใช่แค่การยึดพื้นที่ แต่คือการปะทะ (Crash) ที่ต้องคำนวณผลลัพธ์ว่าใครจะเป็นผู้รอดชีวิต (Attacker vs Defender)

Rogue Inventory & Items: ระบบดรอปไอเทมแบบสุ่มเมื่อชนะการปะทะ 

Intelligent AI: ระบบสมองกลที่รองรับทั้งโหมดสุ่มเดิน (Random Move) และโหมดเน้นการกินหมาก (Priority Capture)

Project Structure
โปรเจกต์ถูกออกแบบโดยแยกส่วน Logic ออกจากหน้าจอการแสดงผล (UI) เพื่อความสะดวกในการทดสอบ:

logic/: ประกอบด้วยไฟล์ Board, Pieces, Crash Logic, Item Logic และ AI Logic

screens/: ส่วนการแสดงผลโดยใช้เฟรมเวิร์ก Kivy

tests/: รวมไฟล์ทดสอบระบบอัตโนมัติ (Automated Testing) ทั้งหมด

Technical Requirements
Language: Python 3.12.10

Environment: Virtual Environment (venv)

Libraries: Kivy (UI Framework), Pytest (Testing Framework)

Installation & Setup
ทำตามขั้นตอนต่อไปนี้เพื่อเตรียมสภาพแวดล้อมสำหรับการรันเกมและระบบเทสครับ:
1.ติดตั้ง Python 3.12.10

2.สร้าง Virtual Environment: python -m venv venv

3.Activate Virtual Environment: venv\Scripts\activate (Windows) หรือ source venv/bin/activate (Linux/Mac)

4.ติดตั้ง Library ที่จำเป็น (Kivy, Pytest): pip install kivy pytest

How to Run
1.รันเกม: python main.py

Development Team
6810110200 นายปัณณวิชญ์ กังพานิช หน้าที่ เขียนระบบ passive ,hidden passive, ออกแบบร่างตัวเกมพืนฐานโดยใช้ figma และ เป็นคนปรับ balance เกม

6810110220 นายพรหมธาดา คูนิอาจ  หน้าที่ setup base chess,เขียนระบบและออกแบบแมพ, uxui, sound effect ,testing ,เกมระบบ event และ ระบบ AI

6810110432 นายอิศม์อนีติ เพ็งแจ่ม หน้าที่ เขียนส่วนของ logic เกม ระบบการ crash ,ระบบเผ่า, item และวาด artของเกม

