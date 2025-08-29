import os
from dotenv import load_dotenv
import openai
import json

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_tags_from_description(description):
    """
    使用 GPT 将用户的感性描述提取为数据库关键词标签
    """
    prompt = f"""
你是一个餐饮推荐系统的助手。
请根据以下用户的感性描述，从这个词库中挑选最相关的关键词（tags）：
词库示例：辣, 酸, 甜, 咸, 川菜, 湘菜, 麻辣烫, 冒菜, 面, 海鲜, 甜品, 轻食, 烧烤, 日料, 泰国菜

用户描述: "{description}"

请以JSON数组格式返回关键词列表，例如：
["辣", "川菜", "冒菜"]
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=50
        )
        tags_text = response.choices[0].message.content.strip()
        # 将模型输出转换为 Python 列表
        tags = json.loads(tags_text)
        return tags
    except Exception as e:
        print("调用API或解析JSON失败:", e)
        return []

if __name__ == "__main__":
    print("=== 餐饮标签提取 Demo ===")
    user_input = input("请输入你的心情或想吃的东西（输入 q 退出）：")
    while user_input.lower() != "q":
        tags = extract_tags_from_description(user_input)
        print("提取到的tags关键词：", tags)
        user_input = input("请输入你的心情或想吃的东西（输入 q 退出）：")
