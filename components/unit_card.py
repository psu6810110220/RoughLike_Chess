from kivy.uix.button import Button

class UnitCard(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.background_normal = ''
        self.background_color = (0.2, 0.2, 0.25, 1)  # สีพื้นหลังเริ่มต้น (เทาเข้ม)
        self.color = (0.8, 0.8, 0.8, 1)              # สีตัวอักษรเริ่มต้น
        self.font_size = '16sp'
        self.bold = True

    def set_selected(self, selected):
        """เปลี่ยนสีปุ่มเมื่อถูกเลือก หรือยกเลิกการเลือก"""
        if selected:
            # สีเมื่อถูกเลือก (สีน้ำเงินสว่าง)
            self.background_color = (0.2, 0.5, 0.8, 1)
            self.color = (1, 1, 1, 1)
        else:
            # กลับไปเป็นสีปกติเมื่อไม่ได้เลือก
            self.background_color = (0.2, 0.2, 0.25, 1)
            self.color = (0.8, 0.8, 0.8, 1)