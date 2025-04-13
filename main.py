import streamlit as st
import random
from datetime import datetime, timedelta

# ------------------------ 基础数据配置 ------------------------
zodiacs = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
tiangans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

nayin_map = {
    ("甲子", "乙丑"): ("海中金", "金"), ("丙寅", "丁卯"): ("炉中火", "火"),
    ("戊辰", "己巳"): ("大林木", "木"), ("庚午", "辛未"): ("路旁土", "土"),
    ("壬申", "癸酉"): ("剑锋金", "金"), ("甲戌", "乙亥"): ("山头火", "火"),
    ("丙子", "丁丑"): ("涧下水", "水"), ("戊寅", "己卯"): ("城头土", "土"),
    ("庚辰", "辛巳"): ("白蜡金", "金"), ("壬午", "癸未"): ("杨柳木", "木"),
    ("甲申", "乙酉"): ("泉中水", "水"), ("丙戌", "丁亥"): ("屋上土", "土"),
    ("戊子", "己丑"): ("霹雳火", "火"), ("庚寅", "辛卯"): ("松柏木", "木"),
    ("壬辰", "癸巳"): ("长流水", "水"), ("甲午", "乙未"): ("沙中金", "金"),
    ("丙申", "丁酉"): ("山下火", "火"), ("戊戌", "己亥"): ("平地木", "木"),
    ("庚子", "辛丑"): ("壁上土", "土"), ("壬寅", "癸卯"): ("金箔金", "金"),
    ("甲辰", "乙巳"): ("覆灯火", "火"), ("丙午", "丁未"): ("天河水", "水"),
    ("戊申", "己酉"): ("大驿土", "土"), ("庚戌", "辛亥"): ("钗钏金", "金"),
    ("壬子", "癸丑"): ("桑柘木", "木"), ("甲寅", "乙卯"): ("大溪水", "水"),
    ("丙辰", "丁巳"): ("沙中土", "土"), ("戊午", "己未"): ("天上火", "火"),
    ("庚申", "辛酉"): ("石榴木", "木"), ("壬戌", "癸亥"): ("大海水", "水")
}

rel_config = {
    "六合": [("鼠", "牛"), ("虎", "猪"), ("兔", "狗"), ("龙", "鸡"), ("蛇", "猴"), ("马", "羊")],
    "六冲": [("鼠", "马"), ("牛", "羊"), ("虎", "猴"), ("兔", "鸡"), ("龙", "狗"), ("蛇", "猪")],
    "六害": [("鼠", "羊"), ("牛", "马"), ("虎", "蛇"), ("兔", "龙"), ("狗", "鸡"), ("猴", "猪")],
    "三合": [["猴", "鼠", "龙"], ["虎", "马", "狗"], ["蛇", "鸡", "牛"], ["猪", "兔", "羊"]]
}

# ------------------------ 核心算法模块 ------------------------
def get_zodiac(year):
    return zodiacs[(year - 4) % 12]

def get_ganzhi(year):
    return tiangans[(year - 4) % 10] + dizhis[(year - 4) % 12]

def get_nayin(ganzhi):
    for key, value in nayin_map.items():
        if ganzhi in key:
            return value
    return ("未知", "未知")

def get_sizhu(birth_time):
    """四柱排盘（简化版）"""
    year = birth_time.year
    month = birth_time.month
    day = birth_time.day
    hour = birth_time.hour
    
    # 年柱
    year_gan = tiangans[(year - 4) % 10]
    year_zhi = dizhis[(year - 4) % 12]
    
    # 月柱（年上起月）
    month_gan = tiangans[((year - 4) % 10 * 2 + month) % 10]
    month_zhi = dizhis[(month + 1) % 12]
    
    # 日柱（简版固定算法）
    day_gan = tiangans[(day - 1) % 10]
    day_zhi = dizhis[(day - 1) % 12]
    
    # 时柱（日上起时）
    hour_gan = tiangans[((day - 1) % 10 * 2 + (hour + 1)//2) % 10]
    hour_zhi = dizhis[((hour + 1)//2) % 12]
    
    return {
        "年柱": f"{year_gan}{year_zhi}",
        "月柱": f"{month_gan}{month_zhi}",
        "日柱": f"{day_gan}{day_zhi}",
        "时柱": f"{hour_gan}{hour_zhi}"
    }

def analyze_zodiac(z1, z2):
    """生肖关系分析"""
    relations = []
    for rel_type, pairs in rel_config.items():
        if rel_type == "三合":
            if any(z1 in group and z2 in group for group in pairs):
                relations.append(rel_type)
        else:
            if (z1, z2) in pairs or (z2, z1) in pairs:
                relations.append(rel_type)
    return relations or ["普通"]

def wuxing_relation(w1, w2):
    """五行生克分析"""
    shengke = {
        "木": {"生": "火", "克": "土"},
        "火": {"生": "土", "克": "金"},
        "土": {"生": "金", "克": "水"},
        "金": {"生": "水", "克": "木"},
        "水": {"生": "木", "克": "火"}
    }
    if w2 == shengke[w1]["生"]: return "相生", f"{w1}→{w2}"
    if w2 == shengke[w1]["克"]: return "相克", f"{w1}→{w2}"
    if w1 == shengke[w2]["生"]: return "相生", f"{w2}→{w1}" 
    if w1 == shengke[w2]["克"]: return "相克", f"{w2}→{w1}"
    return "平衡", ""

def calculate_score(z_rels, wx_rel, nayin_match):
    """综合评分算法"""
    score = 60
    score += len(z_rels) * 10
    if "六合" in z_rels: score += 15
    if "三合" in z_rels: score += 10
    if "相生" in wx_rel[0]: score += 20
    if "相克" in wx_rel[0]: score -= 15
    if nayin_match: score += 10
    return max(min(score, 100), 30)

# ------------------------ 界面模块 ------------------------
def display_analysis(man, woman):
    """显示完整分析报告"""
    with st.expander(f"配对分析：{man['生肖']}({man['年柱']}) & {woman['生肖']}({woman['年柱']})", expanded=True):
        # 四柱信息
        cols = st.columns(2)
        cols[0].markdown(f"**男方四柱**\n" + "\n".join([f"{k}: {v}" for k,v in man["四柱"].items()]))
        cols[1].markdown(f"**女方四柱**\n" + "\n".join([f"{k}: {v}" for k,v in woman["四柱"].items()]))
        
        # 生肖分析
        z_rels = analyze_zodiac(man["生肖"], woman["生肖"])
        st.markdown(f"### 生肖关系：{'+'.join(z_rels)}")
        
        # 五行分析
        wx_rel = wuxing_relation(man["五行"], woman["五行"])
        st.markdown(f"### 五行关系：{wx_rel[0]} ({wx_rel[1]})")
        
        # 纳音分析
        nayin_match = man["纳音"][0][-1] == woman["纳音"][0][-1]
        st.markdown(f"### 纳音配对：{man['纳音'][0]} vs {woman['纳音'][0]} {'(相合)' if nayin_match else ''}")
        
        # 综合评分
        score = calculate_score(z_rels, wx_rel, nayin_match)
        st.progress(score/100)
        st.markdown(f"#### 婚配指数：{score}/100")
        
        # 双版本批语
        st.markdown(classic_comment(z_rels, wx_rel))
        st.markdown(modern_comment(score))
        
        # 婚期推荐
        st.markdown(f"### 推荐婚期：{recommend_date(man['生肖'])}")
        
        # 子嗣预测
        st.markdown(f"### 子嗣运势：{child_prediction(wx_rel)}")

def classic_comment(z_rels, wx_rel):
    """古法批语"""
    comment = []
    if "六合" in z_rels:
        comment.append("乾坤交泰，天作之合")
    if "相生" in wx_rel[0]:
        comment.append(f"{wx_rel[1]} 生生不息")
    return f"> 📜 古法批断：{'，'.join(comment) if comment else '阴阳和合，中平之配'}"

def modern_comment(score):
    """现代解读"""
    if score >= 85: return f"💎 现代解读：天作之合（TOP {100-score}%）"
    if score >= 70: return f"🎯 现代解读：良好婚配（超越{score}%情侣）"
    return f"⚠️ 现代解读：需要努力经营（建议详细合婚）"

# ------------------------ 主程序 ------------------------
def main():
    st.set_page_config("周易婚配系统", layout="wide")
    st.title("🎎 八字婚配分析系统")
    st.caption("《三命通会》· 婚配卷 算法实现")
    
    if st.button("🎲 生成随机测试数据（5对）"):
        for _ in range(5):
            # 生成随机生日（1940-2050）
            man_date = datetime(1940,1,1) + timedelta(days=random.randint(0, 40200))
            woman_date = datetime(1940,1,1) + timedelta(days=random.randint(0, 40200))
            
            # 处理数据
            man = {
                "生肖": get_zodiac(man_date.year),
                "四柱": get_sizhu(man_date),
                "纳音": get_nayin(get_ganzhi(man_date.year)),
                "五行": get_nayin(get_ganzhi(man_date.year))[1]
            }
            woman = {
                "生肖": get_zodiac(woman_date.year),
                "四柱": get_sizhu(woman_date),
                "纳音": get_nayin(get_ganzhi(woman_date.year)),
                "五行": get_nayin(get_ganzhi(woman_date.year))[1]
            }
            
            display_analysis(man, woman)
            st.divider()

if __name__ == "__main__":
    main()
