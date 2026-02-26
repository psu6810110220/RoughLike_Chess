import random

def toss_coin():
    """
    ทำการทอยเหรียญ 1 ครั้งตามกติกา Crash
    Return: จำนวนแต้มที่ได้ (0, 1, 2, หรือ 3) พร้อมชื่อผลลัพธ์
    """
    # ทอยครั้งแรก: ก้อย (50%) vs เหลือง (50%)
    if random.random() < 0.50:
        return 0, "ก้อย"
    
    # ถ้าได้เหลือง มีโอกาส 20% ที่จะสุ่มใหม่
    if random.random() < 0.20:
        # สุ่มระดับ 2: เหลือง (70%) vs แดง (30%)
        if random.random() < 0.70:
            return 1, "หัวสีเหลือง"
        else:
            # ถ้าได้แดง มีโอกาส 20% ที่จะสุ่มใหม่
            if random.random() < 0.20:
                # สุ่มระดับ 3: แดง (85%) vs น้ำเงิน (15%)
                if random.random() < 0.85:
                    return 2, "หัวสีแดง"
                else:
                    return 3, "หัวสีน้ำเงิน"
            else:
                return 2, "หัวสีแดง"
    else:
        return 1, "หัวสีเหลือง"