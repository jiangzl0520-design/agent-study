import streamlit as st

from agents.personal_agent import PersonalAgent


st.set_page_config(page_title="AI Agent Study - V8 Web UI")

st.title("AI Agent Study - V8 Web UI")
st.write("这是 V8 Streamlit 网页版 Agent。")

if "agent" not in st.session_state:
    st.session_state.agent = PersonalAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("请输入你的问题")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    try:
        decision, answer = st.session_state.agent.run_once(user_input)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.write(answer)

        with st.expander("调试信息"):
            st.write(decision)

    except Exception as e:
        st.error(f"Agent 调用出错：{e}")
