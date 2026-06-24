from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re
import ast
import operator
from datetime import datetime

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


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


# ========== 解析模型返回的 JSON ==========

def extract_json(text):
    """
    尽量从模型回复里提取 JSON。
    """

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return json.loads(match.group())

    raise ValueError("模型没有返回有效 JSON")


# ========== 让模型判断是否需要工具 ==========

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

3. chat
用途：普通聊天、解释概念、学习建议。
参数：
{
  "message": "用户问题"
}

你必须只返回 JSON，不要返回 Markdown，不要解释。

返回格式只能是以下三种之一：

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

messages = [
    {
        "role": "system",
        "content": "你是一个耐心的 AI Agent 学习助手，用适合初学者的中文回答。"
    }
]


def normal_chat(user_input):
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    answer = response.choices[0].message.content

    messages.append({"role": "assistant", "content": answer})

    return answer


# ========== 工具结果总结 ==========

def summarize_tool_result(user_input, tool_name, tool_result):
    prompt = f"""
用户的问题是：
{user_input}

你调用了工具：
{tool_name}

工具返回结果是：
{tool_result}

请用自然中文回答用户。
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

print("Agent V3 已启动：我现在可以使用工具了。输入“退出”结束。")

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

        elif tool_name == "chat":
            answer = normal_chat(args["message"])
            print("Agent：" + answer)

        else:
            print("Agent：我还不会使用这个工具。")

    except Exception as e:
        print("Agent：出错了：", e)