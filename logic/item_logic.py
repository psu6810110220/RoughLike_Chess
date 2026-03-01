class Item:
    def __init__(self, id, name, description, image_path):
        self.id = id
        self.name = name
        self.description = description
        self.image_path = image_path

ITEM_DATABASE = {
    1: Item(1, "Totem of Hollow Life", "เมื่อแพ้ Crash จะไม่ตายแต่ Base Point จะเหลือ 0 (ใช้แล้วพัง)", "assets/item/item1.png"),
    2: Item(2, "Clutch Protection", "ปิดการทอยเหรียญของศัตรูที่มาโจมตีเรา 1 ครั้ง (ใช้แล้วพัง)", "assets/item/item2.png"),
    3: Item(3, "Bloodlust Emblem", "ทุกครั้งที่ชนะ Crash จะได้รับ Base Point +5 ถาวร", "assets/item/item3.png"),
    4: Item(4, "Mirage Shield", "ปัดป้องการโจมตีจากศัตรูทิ้ง 1 ครั้ง (ใช้แล้วพัง)", "assets/item/item4.png"),
    5: Item(5, "Scythe of the Substitute", "เมื่อผู้สวมใส่ตาย จะเสก Pawn ฝ่ายเราลงแทนที่ในช่องนั้นทันที", "assets/item/item5.png"),
    6: Item(6, "Gambler's Coin", "เพิ่มจำนวนเหรียญทอย +1 แต่ลด Base Point -1 แต้มถาวร", "assets/item/item6.png"),
    7: Item(7, "Armor of Thorns", "หากแพ้จนตาย ศัตรูตัวที่ฆ่าเราจะติดสถานะ Stagger ทันที", "assets/item/item7.png"),
    8: Item(8, "Aura of Misfortune", "ศัตรูที่มา Crash กับเราจะถูกลดจำนวนเหรียญทอยลง 1 เหรียญ", "assets/item/item8.png"),
    9: Item(9, "Pegasus Boots", "สามารถเดินข้ามหมากตัวอื่นได้เหมือนม้า (Knight) ตลอดเวลา", "assets/item/item9.png"),
    10: Item(10, "Crown of the Usurper", "สวมใส่ให้ Pawn เท่านั้น: จะได้รับ Base Point และ Coin เท่ากับ King", "assets/item/item10.png"),
}