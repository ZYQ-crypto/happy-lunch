from flask import Flask, render_template, request, jsonify
import random
import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

all_recommendations = [
  {
    "name": "川味小馆",
    "signature_dish": "酸辣粉",
    "price_per_person": 25,
    "rating": 4.6,
    "distance": 1.2,
    "recommendation": "酸辣开胃，川菜经典",
    "link": "https://meituan.com/shop/123"
  },
  {
    "name": "快乐麻辣烫",
    "signature_dish": "麻辣烫",
    "price_per_person": 20,
    "rating": 4.5,
    "distance": 0.8,
    "recommendation": "麻辣鲜香，性价比高",
    "link": "https://meituan.com/shop/124"
  },
  {
    "name": "泰香咖喱屋",
    "signature_dish": "冬阴功汤",
    "price_per_person": 45,
    "rating": 4.7,
    "distance": 2.0,
    "recommendation": "酸辣浓郁，泰国风味正宗",
    "link": "https://meituan.com/shop/125"
  },
  {
    "name": "寿司物语",
    "signature_dish": "三文鱼寿司",
    "price_per_person": 60,
    "rating": 4.8,
    "distance": 1.5,
    "recommendation": "新鲜美味，日料推荐",
    "link": "https://meituan.com/shop/126"
  },
  {
    "name": "甜蜜蜜甜品屋",
    "signature_dish": "芒果班戟",
    "price_per_person": 28,
    "rating": 4.9,
    "distance": 0.5,
    "recommendation": "甜品精致，口感丰富",
    "link": "https://meituan.com/shop/127"
  },
  {
    "name": "老北京炸酱面",
    "signature_dish": "炸酱面",
    "price_per_person": 18,
    "rating": 4.4,
    "distance": 1.0,
    "recommendation": "传统北京味道，家常美食",
    "link": "https://meituan.com/shop/128"
  },
  {
    "name": "湘味人家",
    "signature_dish": "剁椒鱼头",
    "price_per_person": 55,
    "rating": 4.6,
    "distance": 1.8,
    "recommendation": "辣味十足，湘菜经典",
    "link": "https://meituan.com/shop/129"
  },
  {
    "name": "法式小馆",
    "signature_dish": "鹅肝",
    "price_per_person": 120,
    "rating": 4.9,
    "distance": 3.5,
    "recommendation": "高端法餐，味道正宗",
    "link": "https://meituan.com/shop/130"
  },
  {
    "name": "新疆大盘鸡",
    "signature_dish": "大盘鸡",
    "price_per_person": 40,
    "rating": 4.5,
    "distance": 2.2,
    "recommendation": "份量足，香辣可口",
    "link": "https://meituan.com/shop/131"
  },
  {
    "name": "港式茶餐厅",
    "signature_dish": "菠萝包",
    "price_per_person": 30,
    "rating": 4.7,
    "distance": 1.3,
    "recommendation": "港式风味，甜点经典",
    "link": "https://meituan.com/shop/132"
  },
  {
    "name": "牛肉粉世家",
    "signature_dish": "桂林米粉",
    "price_per_person": 22,
    "rating": 4.5,
    "distance": 0.9,
    "recommendation": "地道米粉，口感丰富",
    "link": "https://meituan.com/shop/133"
  },
  {
    "name": "重庆小面",
    "signature_dish": "重庆小面",
    "price_per_person": 15,
    "rating": 4.4,
    "distance": 0.7,
    "recommendation": "麻辣鲜香，地道重庆风味",
    "link": "https://meituan.com/shop/134"
  },
  {
    "name": "印度咖喱馆",
    "signature_dish": "黄咖喱鸡",
    "price_per_person": 48,
    "rating": 4.6,
    "distance": 2.8,
    "recommendation": "咖喱浓郁，印度风味正宗",
    "link": "https://meituan.com/shop/135"
  },
  {
    "name": "韩式拌饭屋",
    "signature_dish": "石锅拌饭",
    "price_per_person": 38,
    "rating": 4.5,
    "distance": 1.4,
    "recommendation": "食材丰富，韩式经典",
    "link": "https://meituan.com/shop/136"
  },
  {
    "name": "越南粉坊",
    "signature_dish": "牛肉河粉",
    "price_per_person": 35,
    "rating": 4.6,
    "distance": 1.9,
    "recommendation": "汤鲜味美，越南风味",
    "link": "https://meituan.com/shop/137"
  },
  {
    "name": "铁板烧屋",
    "signature_dish": "铁板牛肉",
    "price_per_person": 80,
    "rating": 4.8,
    "distance": 3.0,
    "recommendation": "肉质鲜嫩，日料推荐",
    "link": "https://meituan.com/shop/138"
  },
  {
    "name": "沙县小吃",
    "signature_dish": "拌面",
    "price_per_person": 12,
    "rating": 4.3,
    "distance": 0.6,
    "recommendation": "家常小吃，实惠美味",
    "link": "https://meituan.com/shop/139"
  },
  {
    "name": "兰州拉面",
    "signature_dish": "牛肉拉面",
    "price_per_person": 18,
    "rating": 4.5,
    "distance": 1.1,
    "recommendation": "汤鲜面筋道，西北风味",
    "link": "https://meituan.com/shop/140"
  },
  {
    "name": "西班牙海鲜饭",
    "signature_dish": "海鲜饭",
    "price_per_person": 95,
    "rating": 4.8,
    "distance": 3.8,
    "recommendation": "海鲜丰富，西餐经典",
    "link": "https://meituan.com/shop/141"
  },
  {
    "name": "烤肉达人",
    "signature_dish": "羊肉串",
    "price_per_person": 50,
    "rating": 4.7,
    "distance": 2.5,
    "recommendation": "肉质鲜美，烧烤经典",
    "link": "https://meituan.com/shop/142"
  },
  {
    "name": "幸福甜品屋",
    "signature_dish": "芒果千层蛋糕",
    "price_per_person": 35,
    "rating": 4.7,
    "distance": 1.1,
    "recommendation": "甜品精致，口感丰富",
    "link": "https://meituan.com/shop/421"
  },
  {
    "name": "日式乌冬屋",
    "signature_dish": "咖喱乌冬面",
    "price_per_person": 42,
    "rating": 4.5,
    "distance": 2.4,
    "recommendation": "日式风味，咖喱香浓",
    "link": "https://meituan.com/shop/422"
  },
  {
    "name": "新疆大盘鸡",
    "signature_dish": "大盘鸡",
    "price_per_person": 58,
    "rating": 4.6,
    "distance": 3.0,
    "recommendation": "香辣味足，新疆风味",
    "link": "https://meituan.com/shop/423"
  },
  {
    "name": "港味茶餐厅",
    "signature_dish": "菠萝油",
    "price_per_person": 28,
    "rating": 4.4,
    "distance": 1.7,
    "recommendation": "港式甜点，下午茶推荐",
    "link": "https://meituan.com/shop/424"
  },
  {
    "name": "泰味小馆",
    "signature_dish": "冬阴功汤",
    "price_per_person": 52,
    "rating": 4.7,
    "distance": 2.0,
    "recommendation": "酸辣浓郁，泰国正宗风味",
    "link": "https://meituan.com/shop/425"
  },
  {
    "name": "小龙虾之家",
    "signature_dish": "十三香小龙虾",
    "price_per_person": 88,
    "rating": 4.8,
    "distance": 3.3,
    "recommendation": "香辣下酒，夜宵必选",
    "link": "https://meituan.com/shop/426"
  },
  {
    "name": "意面物语",
    "signature_dish": "奶油培根意面",
    "price_per_person": 46,
    "rating": 4.5,
    "distance": 1.9,
    "recommendation": "西餐经典，口感浓郁",
    "link": "https://meituan.com/shop/427"
  },
  {
    "name": "东北铁锅炖",
    "signature_dish": "铁锅炖大鹅",
    "price_per_person": 68,
    "rating": 4.6,
    "distance": 3.8,
    "recommendation": "东北风味，热气腾腾",
    "link": "https://meituan.com/shop/428"
  },
  {
    "name": "韩式炸鸡站",
    "signature_dish": "甜辣炸鸡",
    "price_per_person": 55,
    "rating": 4.7,
    "distance": 2.2,
    "recommendation": "韩式风味，下酒美食",
    "link": "https://meituan.com/shop/429"
  },
  {
    "name": "椰香印尼馆",
    "signature_dish": "椰浆饭",
    "price_per_person": 48,
    "rating": 4.4,
    "distance": 2.5,
    "recommendation": "东南亚风味，异域美食",
    "link": "https://meituan.com/shop/430"
  },
  {
    "name": "老北京炸酱面",
    "signature_dish": "炸酱面",
    "price_per_person": 22,
    "rating": 4.5,
    "distance": 1.3,
    "recommendation": "传统老北京味道，家常美食",
    "link": "https://meituan.com/shop/431"
  },
  {
    "name": "川香麻辣烫",
    "signature_dish": "自选麻辣烫",
    "price_per_person": 28,
    "rating": 4.6,
    "distance": 1.6,
    "recommendation": "麻辣鲜香，自选丰富",
    "link": "https://meituan.com/shop/432"
  },
  {
    "name": "湘味剁椒鱼头",
    "signature_dish": "剁椒鱼头",
    "price_per_person": 66,
    "rating": 4.7,
    "distance": 2.8,
    "recommendation": "辣味十足，湘菜经典",
    "link": "https://meituan.com/shop/433"
  },
  {
    "name": "手作寿司坊",
    "signature_dish": "三文鱼寿司",
    "price_per_person": 58,
    "rating": 4.8,
    "distance": 2.1,
    "recommendation": "新鲜生鱼片，日料推荐",
    "link": "https://meituan.com/shop/434"
  },
  {
    "name": "古早味蛋糕屋",
    "signature_dish": "古早味海绵蛋糕",
    "price_per_person": 32,
    "rating": 4.5,
    "distance": 1.0,
    "recommendation": "松软香甜，甜品推荐",
    "link": "https://meituan.com/shop/435"
  },
  {
    "name": "川渝冒菜馆",
    "signature_dish": "麻辣冒菜",
    "price_per_person": 26,
    "rating": 4.6,
    "distance": 1.4,
    "recommendation": "麻辣鲜香，川菜经典",
    "link": "https://meituan.com/shop/436"
  },
  {
    "name": "羊肉泡馍坊",
    "signature_dish": "羊肉泡馍",
    "price_per_person": 38,
    "rating": 4.7,
    "distance": 2.6,
    "recommendation": "西北风味，暖胃美食",
    "link": "https://meituan.com/shop/437"
  },
  {
    "name": "奶茶森林",
    "signature_dish": "黑糖珍珠奶茶",
    "price_per_person": 18,
    "rating": 4.5,
    "distance": 0.9,
    "recommendation": "饮品甜美，解渴推荐",
    "link": "https://meituan.com/shop/438"
  },
  {
    "name": "越南米粉屋",
    "signature_dish": "牛肉河粉",
    "price_per_person": 42,
    "rating": 4.4,
    "distance": 2.0,
    "recommendation": "汤鲜味美，越南风味",
    "link": "https://meituan.com/shop/439"
  },
  {
    "name": "西餐牛排馆",
    "signature_dish": "菲力牛排",
    "price_per_person": 120,
    "rating": 4.9,
    "distance": 3.9,
    "recommendation": "牛排鲜嫩，西餐经典",
    "link": "https://meituan.com/shop/440"
  },
  {
    "name": "蜜汁烤鸭店",
    "signature_dish": "蜜汁烤鸭",
    "price_per_person": 65,
    "rating": 4.7,
    "distance": 2.1,
    "recommendation": "北京风味，烤鸭经典",
    "link": "https://meituan.com/shop/451"
  },
  {
    "name": "火锅江湖",
    "signature_dish": "鸳鸯火锅",
    "price_per_person": 90,
    "rating": 4.8,
    "distance": 3.4,
    "recommendation": "火锅经典，辣鲜美味",
    "link": "https://meituan.com/shop/452"
  },
  {
    "name": "甜蜜蜜冰淇淋",
    "signature_dish": "草莓冰淇淋",
    "price_per_person": 22,
    "rating": 4.6,
    "distance": 1.0,
    "recommendation": "清凉甜品，口感丰富",
    "link": "https://meituan.com/shop/453"
  },
  {
    "name": "日式炸鸡店",
    "signature_dish": "照烧炸鸡",
    "price_per_person": 48,
    "rating": 4.5,
    "distance": 1.7,
    "recommendation": "香脆美味，日料推荐",
    "link": "https://meituan.com/shop/454"
  },
  {
    "name": "台湾卤味坊",
    "signature_dish": "卤味拼盘",
    "price_per_person": 35,
    "rating": 4.7,
    "distance": 1.5,
    "recommendation": "卤味丰富，台式风味",
    "link": "https://meituan.com/shop/455"
  },
  {
    "name": "韩味炸酱面",
    "signature_dish": "炸酱面",
    "price_per_person": 27,
    "rating": 4.4,
    "distance": 1.2,
    "recommendation": "韩式风味，面香浓郁",
    "link": "https://meituan.com/shop/456"
  },
  {
    "name": "西北面馆",
    "signature_dish": "羊肉面片",
    "price_per_person": 30,
    "rating": 4.5,
    "distance": 2.0,
    "recommendation": "西北特色，汤鲜味美",
    "link": "https://meituan.com/shop/457"
  },
  {
    "name": "港式烧腊",
    "signature_dish": "烧鹅饭",
    "price_per_person": 38,
    "rating": 4.6,
    "distance": 1.6,
    "recommendation": "港式风味，肉质鲜美",
    "link": "https://meituan.com/shop/458"
  },
  {
    "name": "日式拉面馆",
    "signature_dish": "豚骨拉面",
    "price_per_person": 45,
    "rating": 4.8,
    "distance": 2.3,
    "recommendation": "汤浓面滑，日料推荐",
    "link": "https://meituan.com/shop/459"
  },
  {
    "name": "手工甜品坊",
    "signature_dish": "抹茶千层",
    "price_per_person": 32,
    "rating": 4.7,
    "distance": 1.1,
    "recommendation": "抹茶香浓，甜品精致",
    "link": "https://meituan.com/shop/460"
  }

]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    description = data.get("description", "")
    budget = float(data.get("budget", 50))

    # 根据预算过滤
    filtered = [r for r in all_recommendations if r["price_per_person"] <= budget]
    if not filtered:
        filtered = all_recommendations  # 如果都超预算，则返回全部

    # 随机抽取 5 条推荐
    recommended = random.sample(filtered, min(5, len(filtered)))

    return jsonify(recommended)

if __name__ == "__main__":
    app.run(debug=True)
