# logic/crash_logic.py
import random

def toss_coin_ayothaya():
    """ทำการทอยเหรียญ 1 ครั้ง ตามกติกา Crash: ก้อย(+0), เหลือง(+1), แดง(+2), น้ำเงิน(+3)"""
    # ระดับ 1: ก้อย (30%) vs เหลือง (70%)
    if random.random() < 0.30:
        return 0, "ก้อย"
    
    # ถ้าได้เหลือง มีโอกาส 60% ที่จะสุ่มต่อไประดับ 2
    if random.random() < 0.60:
        # ระดับ 2: เหลือง (60%) vs แดง (40%)
        if random.random() < 0.60:
            return 1, "หัวสีเหลือง"
        else:
            # ถ้าได้แดง มีโอกาส 30% ที่จะสุ่มต่อไประดับ 3
            if random.random() < 0.30:
                # ระดับ 3: แดง (70%) vs น้ำเงิน (30%)
                if random.random() < 0.70:
                    return 2, "หัวสีแดง"
                else:
                    return 3, "หัวสีน้ำเงิน"
            else:
                return 2, "หัวสีแดง"
    else:
        return 1, "หัวสีเหลือง"

def toss_coin_medieval():
    """ทำการทอยเหรียญ Medieval (สำหรับ Medieval Knight): ก้อย(+0), ฟ้า(s+10), เขียว(+100)"""
    # ระดับ 1: ก้อย (50%) vs ฟ้า (50%)
    if random.random() < 0.50:
        return 0, "ก้อย"

    # ถ้าได้ฟ้า มีโอกาส 1% ที่จะสุ่มต่อไประดับ 2
    if random.random() < 0.01:
        # ระดับ 2: เขียว (1%) vs ฟ้า (99%)
        if random.random() < 0.01:
            return 100, "หัวสีเขียว"
        else:
            return 10, "หัวสีฟ้า"
    else:
        return 10, "หัวสีฟ้า"

def toss_coin_demon():
    """ทอยเหรียญของ Demon: ก้อย(-3), ส้ม(+4), ม่วง(+6)"""
    # ก้อย ต่อ หัว 40:60
    if random.random() < 0.40:
        return -3, "ก้อย"
    
    # ถ้าได้ฟ้า มีโอกาส 20% ที่จะสุ่มต่อไประดับ 2
    if random.random() < 0.01:
        # ระดับ 2: ม่วง (20%) vs ส้ม (80%)
        if random.random() < 0.20:
            return 4, "หัวสีม่วง"
        else:
            return 6, "หัวสีส้ม"
    else:
        return 6, "หัวสีส้ม"

def toss_coin_heaven():
    """ทอยเหรียญของ Heaven: ก้อย(+0), เหลือง(+1)"""
    # ก้อย ต่อ หัว 50:50
    if random.random() < 0.50:
        return 0, "ก้อย"
    else:
        return 1, "หัวสีเหลือง"

def calculate_total_points(base_points, num_coins):
    """คำนวณแต้มรวมทั้งหมดจากการวนลูปทอยเหรียญโดยอิงตามเผ่า"""
    total = base_points
    results = []
    for _ in range(num_coins):
        if faction == "medieval":
            p, color = toss_coin_medieval()
        elif faction == "demon":
            p, color = toss_coin_demon()
        elif faction == "heaven":
            p, color = toss_coin_heaven()
        else:
            p, color = toss_coin_ayothaya()
            
        total += p
        results.append(color)
    return total, results

def resolve_crash(p1_name, p1_base, p1_coins, p2_name, p2_base, p2_coins):
    """ฟังก์ชันหลักสำหรับตัดสินการ Crash"""
    p1_total, p1_results = calculate_total_points(p1_base, p1_coins)
    p2_total, p2_results = calculate_total_points(p2_base, p2_coins)
    
    winner = None
    if p1_total > p2_total:
        winner = p1_name
    elif p2_total > p1_total:
        winner = p2_name
        
    return {
        "p1": {"name": p1_name, "total": p1_total, "results": p1_results},
        "p2": {"name": p2_name, "total": p2_total, "results": p2_results},
        "winner": winner
    }