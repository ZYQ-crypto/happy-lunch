import json
import random

# 读取数据
with open('data.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# 心情 → 标签映射
emotion_map = {
    "清凉": ["甜品", "泰国菜"],
    "重口味": ["辣", "咸"],
    "让胃舒服": ["面", "汤"],
    "外焦里嫩": ["铁板烧", "炸鸡"],
    "日常菜推荐": ["沙县小吃", "兰州拉面", "快餐"],
    "热气腾腾": ["火锅", "面"]
}

# 推荐语模板
taste_templates = {
    "辣": [
        "这家的{dish}辣得恰到好处，唤醒你的味蕾！",
        "一口{dish}，尽享麻辣鲜香，热辣非凡！",
        "喜欢辣味的你，千万不要错过这道{dish}。"
    ],
    "甜品": [
        "用{dish}来犒劳一下自己，甜而不腻，幸福感爆棚！",
        "这款{dish}入口即化，是夏日解暑的绝佳选择！"
    ],
    "汤": [
        "一碗热气腾腾的{dish}，让你的胃瞬间舒适下来。",
        "喝上一口{dish}，整个人都暖洋洋的。"
    ]
}

# 生成推荐语
def generate_recommendation(dish, tags):
    templates_pool = []
    for tag in tags:
        if tag in taste_templates:
            templates_pool.extend(taste_templates[tag])
    if not templates_pool:
        templates_pool = [
            "{dish}美味可口，值得一试！",
            "推荐你试试{dish}，一定不会失望。",
            "{dish}风味独特，快来尝尝吧！"
        ]
    template = random.choice(templates_pool)
    return template.format(dish=dish)

# 核心推荐逻辑
def recommend(description, budget):
    description_lower = description.lower()

    # 根据心情映射标签
    mapped_tags = []
    for key, tags in emotion_map.items():
        if key in description_lower:
            mapped_tags.extend(tags)

    # 按预算过滤
    budget_filtered = [r for r in restaurants if r['price_per_person'] <= budget]
    if not budget_filtered:
        budget_filtered = restaurants

    # 匹配餐厅
    results = []
    for r in budget_filtered:
        direct_match = any(tag in description_lower for tag in r['tags'])
        mapped_match = any(tag in r['tags'] for tag in mapped_tags)
        if direct_match or mapped_match:
            results.append(r)

    if not results:
        results = budget_filtered

    # 加入推荐语
    for r in results:
        r['recommendation'] = generate_recommendation(r['signature_dish'], r['tags'])

    # 返回最多5条
    return random.sample(results, min(5, len(results)))
