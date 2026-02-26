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


def calculate_total_points(base_points, num_coins):
    """
    คำนวณแต้มรวมทั้งหมดของตัวละคร
    """
    total_points = base_points
    coin_results = []
    
    for _ in range(num_coins):
        points, color = toss_coin()
        total_points += points
        coin_results.append(color)
        
    return total_points, coin_results


def resolve_crash(player1_name, p1_base, p1_coins, player2_name, p2_base, p2_coins):
    """
    ระบบ Crash ระหว่าง 2 ฝ่าย
    """
    # คำนวณฝ่ายที่ 1
    p1_total, p1_results = calculate_total_points(p1_base, p1_coins)
    
    # คำนวณฝ่ายที่ 2
    p2_total, p2_results = calculate_total_points(p2_base, p2_coins)
    
    # สรุปผล
    winner = None
    if p1_total > p2_total:
        winner = player1_name
    elif p2_total > p1_total:
        winner = player2_name
    else:
        winner = "เสมอ"
        
    return {
        "player1": {
            "name": player1_name,
            "base_points": p1_base,
            "coins": p1_coins,
            "coin_results": p1_results,
            "total_points": p1_total
        },
        "player2": {
            "name": player2_name,
            "base_points": p2_base,
            "coins": p2_coins,
            "coin_results": p2_results,
            "total_points": p2_total
        },
        "winner": winner
    }