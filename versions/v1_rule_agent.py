while True:
    user_input = input("你：")

    if user_input == "退出":
        print("Agent：再见！")
        break

    elif "天气" in user_input:
        print("Agent：我暂时不会查天气。")

    elif "你好" in user_input:
        print("Agent：你好，很高兴认识你！")

    else:
        print("Agent：我还没有学会这个功能。")
