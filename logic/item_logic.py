# logic/item_logic.py

class Item:
    def __init__(self, id, name, description, image_path):
        self.id = id
        self.name = name
        self.description = description
        self.image_path = image_path

ITEM_DATABASE = {
    1: Item(1, "Totem of Hollow Life", "Survive a lethal Crash, but Base Points drop to 0. (Consumable)", "assets/item/item1.png"),
    2: Item(2, "Clutch Protection", "Nullify the attacker's coin toss entirely for 1 turn. (Consumable)", "assets/item/item2.png"),
    3: Item(3, "Bloodlust Emblem", "Gain +5 Base Points permanently upon winning a Crash.", "assets/item/item3.png"),
    4: Item(4, "Mirage Shield", "Block and cancel an incoming attack completely. (Consumable)", "assets/item/item4.png"),
    5: Item(5, "Scythe of the Substitute", "Spawns a friendly Pawn on this tile upon death.", "assets/item/item5.png"),
    6: Item(6, "Gambler's Coin", "+1 Coin but permanently lose 1 Base Point.", "assets/item/item6.png"),
    7: Item(7, "Armor of Thorns", "If killed, the attacker permanently loses 1 Coin.", "assets/item/item7.png"),
    8: Item(8, "Aura of Misfortune", "Reduces the attacker's coins by 1 during a Crash.", "assets/item/item8.png"),
    9: Item(9, "Pegasus Boots", "Can leap over other pieces like a Knight.", "assets/item/item9.png"),
    10: Item(10, "Crown of the Usurper", "Pawn only: Base Points become 5 and Coins become 3.", "assets/item/item10.png"),
}