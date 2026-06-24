from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re
import ast
import operator
from datetime import datetime
from pathlib import Path

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

MEMORY_FILE = Path("memory.json")


# ========== 工具1：安全计算器 ==========

def safe_calculator(expression):
    """
    只允许计算数字和 + - * / ** ()，避免执行危险代码。
    """

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def eval_node(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("只允许数字")

        if isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            op_type = type(node.op)

            if op_type not in allowed_operators:
                raise ValueError("不支持这个运算符")

            return allowed_operators[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operand = eval_node(node.operand)
            op_type = type(node.op)

            if op_type not in allowed_operators:
                raise ValueError("不支持这个一元运算符")

            return allowed_operators[op_type](operand)

        raise ValueError("表达式不安全")

    tree = ast.parse(expression, mode="eval")
    return eval_node(tree.body)


# ========== 工具2：获取当前时间 ==========

def get_current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# ========== 工具3：读取长期记忆 ==========

def load_memory():
    if not MEMORY_FILE.exists():
        return {"facts": []}

    try:
        content = MEMORY_FILE.read_text(encoding="utf-8")
        return json.loads(content)
    except Exception:
        return {"facts": []}


# ========== 工具4：写入长期记忆 ==========

def write_memory(data):
    MEMORY_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def save_memory(content):
    data = load_memory()

    fact = {
        "content": content,
        "created_at": get_current_time()
    }

    data["facts"].append(fact)
    write_memory(data)

    return f"已保存长期记忆：{content}"


# ========== 工具5：搜索长期记忆 ==========

def search_memory(query):
    data = load_memory()
    facts = data.get("facts", [])

    if not facts:
        return "目前没有长期记忆。"

    keywords = re.split(r"\s+|，|。|、|\?|？|！|!", query)
    keywords = [word for word in keywords if word.strip()]

    matches = []

    for fact in facts:
        content = fact["content"]

        if any(keyword in content for keyword in keywords):
            matches.append(fact)

    # 如果关键词没匹配到，就先返回全部记忆。
    # 现在记忆数量少，这样更适合初学阶段。
    if not matches:
        matches = facts

    result = []

    for index, fact in enumerate(matches, start=1):
        result.append(
            f"{index}. {fact['content']}（保存时间：{fact['created_at']}）"
        )

    return "\n".join(result)


# ========== 从模型回复中提取 JSON ==========

def extract_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return json.loads(match.group())

    raise ValueError("模型没有返回有效 JSON")


# ========== 让模型判断该用哪个工具 ==========

def decide_tool(user_input):
    system_prompt = """
你是一个工具选择 Agent。

你可以使用以下工具：

1. calculator
用途：数学计算。
参数：
{
  "expression": "数学表达式"
}

2. get_time
用途：获取当前时间。
参数：
{}

3. save_memory
用途：当用户要求你“记住”“保存”“记录”“以后记得”某个信息时使用。
参数：
{
  "content": "要保存的信息"
}

4. search_memory
用途：当用户询问“你记得什么”“我叫什么”“我的目标是什么”“我之前说过什么”时使用。
参数：
{
  "query": "用户想查询的记忆"
}

5. chat
用途：普通聊天、解释概念、学习建议、不需要调用工具的问题。
参数：
{
  "message": "用户原始问题"
}

你必须只返回 JSON，不要返回 Markdown，不要解释。

返回格式只能是以下五种之一：

{
  "tool": "calculator",
  "args": {
    "expression": "120 * 35"
  }
}

{
  "tool": "get_time",
  "args": {}
}

{
  "tool": "save_memory",
  "args": {
    "content": "用户叫小姜，正在学习 AI Agent"
  }
}

{
  "tool": "search_memory",
  "args": {
    "query": "用户叫什么"
  }
}

{
  "tool": "chat",
  "args": {
    "message": "用户原始问题"
  }
}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0
    )

    decision_text = response.choices[0].message.content
    return extract_json(decision_text)


# ========== 普通聊天 ==========

conversation_history = []


def normal_chat(user_input):
    memory_context = search_memory(user_input)

    messages = [
        {
            "role": "system",
            "content": f"""
你是一个耐心的 AI Agent 学习助手。
你适合帮助初学者学习 Python、AI Agent、工具调用和项目开发。
请使用简单、清楚、可执行的中文回答。

以下是你已经保存的长期记忆：
{memory_context}
"""
        }
    ]

    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    answer = response.choices[0].message.content

    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": answer})

    return answer


# ========== 工具结果总结 ==========

def summarize_tool_result(user_input, tool_name, tool_result):
    prompt = f"""
用户的问题是：
{user_input}

你调用的工具是：
{tool_name}

工具返回结果是：
{tool_result}

请根据工具结果，用自然、简洁的中文回答用户。
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一个会使用工具的 AI Agent，请根据工具结果回答用户。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ========== 主程序 ==========

print("Agent V4 已启动：我现在有工具调用和长期记忆。输入“退出”结束。")

while True:
    user_input = input("你：")

    if user_input == "退出":
        print("Agent：再见！")
        break

    try:
        decision = decide_tool(user_input)

        print("调试：模型选择了", decision)

        tool_name = decision["tool"]
        args = decision["args"]

        if tool_name == "calculator":
            expression = args["expression"]
            result = safe_calculator(expression)
            answer = summarize_tool_result(user_input, "calculator", result)
            print("Agent：" + answer)

        elif tool_name == "get_time":
            result = get_current_time()
            answer = summarize_tool_result(user_input, "get_time", result)
            print("Agent：" + answer)

        elif tool_name == "save_memory":
            content = args.get("content", user_input)
            result = save_memory(content)
            answer = summarize_tool_result(user_input, "save_memory", result)
            print("Agent：" + answer)

        elif tool_name == "search_memory":
            query = args.get("query", user_input)
            result = search_memory(query)
            answer = summarize_tool_result(user_input, "search_memory", result)
            print("Agent：" + answer)

        elif tool_name == "chat":
            message = args.get("message", user_input)
            answer = normal_chat(message)
            print("Agent：" + answer)

        else:
            print("Agent：我还不会使用这个工具。")

    except Exception as e:
        print("Agent：出错了：", e)