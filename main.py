from agents.personal_agent import PersonalAgent


def main():
    agent = PersonalAgent()

    print("Agent V4 Refactor 已启动：我现在有工具调用和长期记忆。输入“退出”结束。")

    while True:
        user_input = input("你：")

        if user_input == "退出":
            print("Agent：再见！")
            break

        try:
            decision, answer = agent.run_once(user_input)

            print("调试：模型选择了", decision)
            print("Agent：" + answer)

        except Exception as e:
            print("Agent：出错了：", e)


if __name__ == "__main__":
    main()