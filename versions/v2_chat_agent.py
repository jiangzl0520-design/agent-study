from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

messages = [
    {
        "role": "system",
        "content": "你是一个耐心的AI Agent学习助手，适合初学者，用简单清楚的中文回答。"
    }
]

print("AI Chat Agent V2 已启动。输入“退出”结束对话。")

while True:
    user_input = input("你：")

    if user_input == "退出":
        print("Agent：再见！")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    answer = response.choices[0].message.content

    print("Agent：" + answer)

    messages.append({
        "role": "assistant",
        "content": answer
    })