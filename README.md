# AI Agent Study Project

这是我的第一个 AI Agent 学习项目。

项目从最基础的规则 Agent 开始，逐步升级到大模型聊天、工具调用、长期记忆和模块化项目结构。

---

## 项目目标

通过这个项目，我希望掌握 AI Agent 的核心开发流程：

* 理解 Agent 的基本运行循环
* 学会调用大模型 API
* 学会实现短期对话记忆
* 学会让 Agent 调用工具
* 学会实现本地长期记忆
* 学会拆分 Python 项目结构
* 最终做出可以放到 GitHub 和简历中的 Agent 项目

---

## 已完成版本

### V1：规则 Agent

文件：

```text
versions/v1_rule_agent.py
```

V1 是一个基于规则的 Agent。

它使用 Python 的 `if / elif / else` 判断用户输入，然后返回预设回复。

核心原理：

```text
用户输入
↓
规则判断
↓
执行对应逻辑
↓
返回结果
```

这个版本帮助我理解了 Agent 最基础的运行循环：

```text
输入 → 判断 → 执行 → 输出
```

---

### V2：AI Chat Agent

文件：

```text
versions/v2_chat_agent.py
```

V2 接入了大模型 API，让 Agent 不再只依赖固定规则，而是可以根据用户输入生成动态回答。

核心原理：

```text
用户输入
↓
发送给大模型
↓
大模型生成回答
↓
返回给用户
```

这个版本让我理解了：

* API Key
* `.env`
* OpenAI 兼容 SDK
* system prompt
* user message
* assistant message
* messages 对话结构

---

### V2.5：短期记忆 Agent

V2 后续增加了短期记忆能力。

短期记忆的实现方式是：把用户输入和模型回复都保存到 `messages` 列表中。

核心原理：

```text
用户输入
↓
保存到 messages
↓
调用大模型
↓
模型回答
↓
把模型回答也保存到 messages
↓
下一轮对话时继续带上历史记录
```

这种记忆只存在程序运行期间。程序关闭后，`messages` 变量会消失，所以它属于短期记忆。

---

### V3：工具调用 Agent

文件：

```text
versions/v3_tools_agent.py
```

V3 增加了工具调用能力。

Agent 可以根据用户输入选择不同工具：

* `calculator`：计算数学表达式
* `get_time`：获取当前时间
* `chat`：普通聊天

核心原理：

```text
用户输入
↓
大模型判断要使用哪个工具
↓
返回 JSON 格式的工具选择
↓
Python 根据 JSON 调用对应函数
↓
工具返回结果
↓
Agent 组织语言回答用户
```

这个版本让我理解了 Tool Calling / Function Calling 的基本原理：

```text
大模型负责理解和判断
Python 工具负责执行具体任务
Agent 负责连接模型和工具
```

例如用户输入：

```text
帮我计算 120 * 35
```

模型会返回类似：

```json
{
  "tool": "calculator",
  "args": {
    "expression": "120 * 35"
  }
}
```

然后 Python 调用计算器工具，得到结果：

```text
4200
```

最后 Agent 把工具结果整理成自然语言回复用户。

---

### V4：长期记忆 Agent

文件：

```text
versions/v4_single_file_agent.py
```

V4 在 V3 的基础上加入了长期记忆。

新增工具：

* `save_memory`：保存用户信息
* `search_memory`：搜索用户记忆

记忆被保存到本地文件：

```text
memory.json
```

核心原理：

```text
用户要求记住某件事
↓
Agent 调用 save_memory
↓
写入 memory.json
↓
下次用户询问时
↓
Agent 调用 search_memory
↓
读取 memory.json
↓
根据记忆回答用户
```

V4 和 V2 短期记忆的区别：

| 版本 | 记忆方式             | 程序关闭后是否保留 |
| -- | ---------------- | --------- |
| V2 | `messages` 列表    | 不保留       |
| V4 | `memory.json` 文件 | 保留        |

---

## 当前重构版项目结构

当前版本已经把单文件 V4 拆分成多个模块。

```text
agent-study/
│
├── main.py                    # 项目主入口，运行当前重构版 Agent
├── README.md                  # 项目说明文档
├── requirements.txt           # 项目依赖
├── .gitignore                 # Git 忽略文件配置
├── .env                       # API Key 配置文件，不上传 GitHub
├── memory.json                # 本地长期记忆文件，不上传 GitHub
│
├── agents/
│   ├── __init__.py
│   └── personal_agent.py      # Agent 核心逻辑：工具选择、模型调用、对话处理
│
├── tools/
│   ├── __init__.py
│   ├── calculator.py          # 计算器工具
│   ├── time_tool.py           # 当前时间工具
│   └── memory_tool.py         # 长期记忆工具
│
├── utils/
│   ├── __init__.py
│   └── json_parser.py         # 解析模型返回的 JSON
│
└── versions/
    ├── v1_rule_agent.py        # V1：规则 Agent
    ├── v2_chat_agent.py        # V2：大模型聊天 Agent
    ├── v3_tools_agent.py       # V3：工具调用 Agent
    └── v4_single_file_agent.py # V4：单文件长期记忆 Agent
```

---

## 当前功能

当前重构版 Agent 支持：

* 调用大模型 API
* 普通聊天
* 工具选择
* 工具调用
* 计算器工具
* 当前时间工具
* 保存长期记忆
* 搜索长期记忆
* 使用 `memory.json` 保存本地记忆
* 使用 `.env` 管理 API Key

---

## 技术栈

* Python
* OpenAI Python SDK
* DeepSeek API
* python-dotenv
* JSON
* VS Code
* PowerShell

---

## 如何运行

### 1. 创建虚拟环境

```powershell
python -m venv .venv
```

---

### 2. 激活虚拟环境

```powershell
.\.venv\Scripts\Activate.ps1
```

激活成功后，终端前面应该出现：

```text
(.venv)
```

---

### 3. 安装依赖

```powershell
python -m pip install -r requirements.txt
```

---

### 4. 创建 `.env` 文件

在项目根目录创建 `.env` 文件，并写入：

```env
DEEPSEEK_API_KEY=你的真实API_Key
```

注意：

* 不要把 `.env` 上传到 GitHub
* 不要把 API Key 写进 Python 代码
* 不要把 API Key 截图发给别人

---

### 5. 运行当前重构版 Agent

```powershell
python main.py
```

正常启动后会看到：

```text
Agent V4 Refactor 已启动：我现在有工具调用和长期记忆。输入“退出”结束。
你：
```

---

## 测试示例

### 测试计算器工具

```text
帮我计算 120 * 35
```

预期效果：

```text
Agent 会选择 calculator 工具，并返回 4200。
```

---

### 测试时间工具

```text
现在几点了？
```

预期效果：

```text
Agent 会选择 get_time 工具，并返回当前时间。
```

---

### 测试长期记忆保存

```text
请记住：我叫小姜，我正在学习 AI Agent
```

预期效果：

```text
Agent 会选择 save_memory 工具，把信息保存到 memory.json。
```

---

### 测试长期记忆搜索

```text
我叫什么？我正在学什么？
```

预期效果：

```text
Agent 会选择 search_memory 工具，从 memory.json 读取记忆并回答。
```

---

## 我学到的核心概念

通过这个项目，我学习了以下 Agent 开发概念：

* Agent Loop
* LLM API 调用
* Prompt
* Messages
* Short-term Memory
* Long-term Memory
* Tool Calling
* Function Calling
* JSON 工具路由
* `.env` 环境变量管理
* Python 模块化拆分
* 项目结构整理
* requirements.txt 依赖管理
* .gitignore 安全配置

---

## 关键理解

### 什么是 Agent？

Agent 可以理解为一个能够接收用户输入、判断任务、选择行动并返回结果的程序。

最基础的 Agent 流程是：

```text
用户输入
↓
Agent 判断任务
↓
Agent 执行动作
↓
Agent 返回结果
```

---

### 什么是 Tool Calling？

Tool Calling 是让大模型决定是否调用工具。

大模型本身负责理解问题和选择工具，真正执行任务的是 Python 函数。

```text
大模型：判断应该用哪个工具
Python：执行工具
Agent：连接模型和工具
```

---

### 什么是长期记忆？

长期记忆是指程序关闭后仍然保留的信息。

在这个项目中，我使用 `memory.json` 保存长期记忆。

```text
保存记忆 → 写入 memory.json
搜索记忆 → 读取 memory.json
```

---

### 为什么要模块化拆分？

最开始的 V4 是一个大文件，所有代码都写在一起，不方便维护。

重构后，不同功能被拆分到不同文件中：

```text
agents/ 负责 Agent 主逻辑
tools/ 负责工具函数
utils/ 负责通用辅助函数
main.py 负责启动程序
```

这样项目更清晰，也更接近真实开发中的项目结构。

---

## 下一步计划

接下来计划继续升级项目：

* 上传到 GitHub
* 开发 Agent V5：任务规划 Agent
* 增加学习进度记录功能
* 增加更多工具
* 使用 Streamlit 做一个简单网页界面
* 学习 RAG
* 学习 LangChain / LangGraph
* 准备 Agent 实习项目展示和面试介绍

---

## 项目当前状态

已完成：

* V1：规则 Agent
* V2：大模型聊天 Agent
* V3：工具调用 Agent
* V4：长期记忆 Agent
* V4 Refactor：模块化重构版 Agent

当前推荐运行方式：

```powershell
python main.py
```
## 运行方式

### 1. 命令行运行

```bash
python main.py