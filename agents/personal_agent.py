import os

from dotenv import load_dotenv
from openai import OpenAI

from tools.calculator import safe_calculator
from tools.time_tool import get_current_time
from tools.memory_tool import save_memory, search_memory
from utils.json_parser import extract_json
from tools.planner_tool import build_plan_prompt

class PersonalAgent:
    """
    一个带工具调用和长期记忆的个人 Agent。
    """

    def __init__(self):
        load_dotenv(override=True)

        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

        self.conversation_history = []

    def decide_tool(self, user_input):
        """
        让大模型判断应该使用哪个工具。
        """
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
5. make_plan
用途：当用户要求制定计划、学习路线、项目路线、任务拆解、实习准备计划时使用。
参数：
{
  "goal": "用户想要实现的目标"
}
6. chat
用途：普通聊天、解释概念、学习建议、不需要调用工具的问题。
参数：
{
  "message": "用户原始问题"
}

你必须只返回 JSON，不要返回 Markdown，不要解释。

返回格式只能是以下六种之一：

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
  "tool": "make_plan",
  "args": {
    "goal": "用户想要实现的目标"
  }
}
{
  "tool": "chat",
  "args": {
    "message": "用户原始问题"
  }
}
"""

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0
        )

        decision_text = response.choices[0].message.content
        return extract_json(decision_text)

    def normal_chat(self, user_input):
        """
        普通聊天。
        会把长期记忆作为上下文给模型。
        """
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

        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        answer = response.choices[0].message.content

        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": answer})

        return answer

    def summarize_tool_result(self, user_input, tool_name, tool_result):
        """
        把工具结果整理成自然语言回答。
        """
        prompt = f"""
用户的问题是：
{user_input}

你调用的工具是：
{tool_name}

工具返回结果是：
{tool_result}

请根据工具结果，用自然、简洁的中文回答用户。
"""

        response = self.client.chat.completions.create(
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
    def make_plan(self, user_goal):
        """
        根据用户目标生成任务规划。
        """
        plan_prompt = build_plan_prompt(user_goal)

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个擅长制定学习计划、项目计划和任务拆解的 AI Agent。"
                },
                {
                    "role": "user",
                    "content": plan_prompt
                }
            ]
        )

        return response.choices[0].message.content
    def run_once(self, user_input):
        """
        处理用户的一次输入。
        """
        decision = self.decide_tool(user_input)

        tool_name = decision["tool"]
        args = decision["args"]

        if tool_name == "calculator":
            expression = args["expression"]
            result = safe_calculator(expression)
            answer = self.summarize_tool_result(user_input, "calculator", result)
            return decision, answer

        if tool_name == "get_time":
            result = get_current_time()
            answer = self.summarize_tool_result(user_input, "get_time", result)
            return decision, answer

        if tool_name == "save_memory":
            content = args.get("content", user_input)
            result = save_memory(content)
            answer = self.summarize_tool_result(user_input, "save_memory", result)
            return decision, answer

        if tool_name == "search_memory":
            query = args.get("query", user_input)
            result = search_memory(query)
            answer = self.summarize_tool_result(user_input, "search_memory", result)
            return decision, answer
        if tool_name == "make_plan":
            goal = args.get("goal", user_input)
            answer = self.make_plan(goal)
            return decision, answer
        if tool_name == "chat":
            message = args.get("message", user_input)
            answer = self.normal_chat(message)
            return decision, answer

        return decision, "我还不会使用这个工具。"