# AI Agent Study Project 项目复盘：V1 - V6

## 一、项目背景

这是我的第一个 AI Agent 学习项目。

我从最基础的规则 Agent 开始，逐步实现了大模型聊天、工具调用、长期记忆、任务规划和学习进度记录功能。整个项目的目标不是一开始就使用复杂框架，而是先用 Python 手写一个 Agent 的核心流程，从底层理解 Agent 是如何工作的。

通过这个项目，我逐步理解了：

* 什么是 Agent Loop
* 如何调用大模型 API
* 如何使用 Prompt 控制模型行为
* 如何让模型选择工具
* 如何用 Python 函数执行工具
* 如何保存长期记忆
* 如何进行任务规划
* 如何记录学习进度
* 如何用 Git 和 GitHub 管理项目版本

---

## 二、项目整体演进路线

项目从 V1 到 V6 的演进路线如下：

```text
V1：规则 Agent
↓
V2：大模型聊天 Agent
↓
V3：工具调用 Agent
↓
V4：长期记忆 Agent
↓
V5：任务规划 Agent
↓
V6：学习进度记录 Agent
```

每个版本都在前一个版本的基础上增加一个核心能力。

---

## 三、V1：规则 Agent

### 1. 实现内容

V1 是最基础的规则 Agent。

它不调用大模型，而是通过 Python 的 `if / elif / else` 判断用户输入，然后返回固定回复。

例如：

```python
if user_input == "退出":
    break

elif "你好" in user_input:
    print("Agent：你好，很高兴认识你！")

elif "天气" in user_input:
    print("Agent：我暂时不会查天气。")
```

### 2. 核心原理

V1 的核心是规则判断。

流程是：

```text
用户输入
↓
程序判断关键词
↓
命中规则
↓
执行对应回复
```

这让我理解了 Agent 最基础的运行循环：

```text
输入 → 判断 → 执行 → 输出
```

### 3. 学到的内容

通过 V1，我理解了 Agent 不一定一开始就需要大模型。最简单的 Agent 其实就是一个能够接收输入、判断任务并返回结果的程序。

V1 帮我建立了 Agent Loop 的基础概念。

---

## 四、V2：大模型聊天 Agent

### 1. 实现内容

V2 开始接入大模型 API。

我使用 OpenAI 兼容 SDK，通过 DeepSeek API 调用大模型，让 Agent 可以根据用户输入动态生成回答。

核心逻辑是：

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

answer = response.choices[0].message.content
```

### 2. 核心原理

V2 的流程是：

```text
用户输入
↓
把用户输入放进 messages
↓
调用大模型 API
↓
模型生成回答
↓
返回给用户
```

相比 V1，V2 不再依赖固定规则，而是让大模型理解用户问题并生成回答。

### 3. messages 的作用

`messages` 是对话上下文。

常见角色包括：

```text
system：系统指令，告诉模型应该扮演什么角色
user：用户输入
assistant：模型回复
```

例如：

```python
messages = [
    {
        "role": "system",
        "content": "你是一个耐心的 AI Agent 学习助手"
    },
    {
        "role": "user",
        "content": "什么是 AI Agent？"
    }
]
```

### 4. 学到的内容

通过 V2，我理解了大模型 Agent 的基本结构：

```text
Prompt + Messages + LLM API = AI Chat Agent
```

我也理解了为什么 API Key 不能写死在代码里，而应该放在 `.env` 文件中。

---

## 五、V2.5：短期记忆 Agent

### 1. 实现内容

在 V2 的基础上，我加入了短期记忆。

实现方式是：每次用户输入后，把用户内容保存到 `messages`；每次模型回复后，也把模型回复保存到 `messages`。

核心代码：

```python
messages.append({
    "role": "user",
    "content": user_input
})

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

answer = response.choices[0].message.content

messages.append({
    "role": "assistant",
    "content": answer
})
```

### 2. 核心原理

短期记忆的流程是：

```text
用户输入
↓
保存到 messages
↓
模型回答
↓
模型回答也保存到 messages
↓
下一轮对话继续带上历史记录
```

这样模型就能在当前程序运行期间记住前面说过的话。

### 3. 局限性

这种记忆只存在 Python 变量里。

```text
程序运行时：记得
程序关闭后：忘记
```

所以它是短期记忆，不是长期记忆。

### 4. 学到的内容

我理解了短期记忆的本质：不是模型真的永久记住了信息，而是程序每次调用模型时，把历史对话一起传给模型。

---

## 六、V3：工具调用 Agent

### 1. 实现内容

V3 增加了工具调用能力。

我给 Agent 增加了几个工具：

```text
calculator：计算器工具
get_time：当前时间工具
chat：普通聊天工具
```

当用户输入：

```text
帮我计算 120 * 35
```

大模型会先判断应该使用 `calculator` 工具，并返回 JSON：

```json
{
  "tool": "calculator",
  "args": {
    "expression": "120 * 35"
  }
}
```

Python 程序解析 JSON 后，调用对应函数执行计算。

### 2. 核心原理

V3 的核心流程是：

```text
用户输入
↓
大模型判断需要哪个工具
↓
模型返回 JSON
↓
Python 解析 JSON
↓
调用对应工具函数
↓
工具返回结果
↓
Agent 整理成自然语言回答
```

### 3. Tool Calling 的本质

Tool Calling 的核心分工是：

```text
大模型：负责理解用户意图和选择工具
Python 工具：负责真正执行任务
Agent 程序：负责连接模型和工具
```

### 4. 为什么使用 JSON

大模型返回自然语言，程序不好处理。

但是如果模型返回 JSON：

```json
{
  "tool": "calculator",
  "args": {
    "expression": "120 * 35"
  }
}
```

Python 可以很容易读取：

```python
tool_name = decision["tool"]
args = decision["args"]
```

所以 JSON 的作用是把大模型的判断转成程序能执行的结构化指令。

### 5. 安全计算器

计算器工具没有直接使用 `eval()`，而是使用 `ast` 和 `operator` 做安全解析。

这样只允许：

```text
数字
加法
减法
乘法
除法
幂运算
括号
```

避免用户输入恶意 Python 代码。

### 6. 学到的内容

通过 V3，我理解了 Agent 和普通聊天机器人的重要区别：

普通聊天机器人只回答问题，而 Agent 可以根据任务选择工具并执行操作。

---

## 七、V4：长期记忆 Agent

### 1. 实现内容

V4 在 V3 的基础上加入了长期记忆。

新增工具：

```text
save_memory：保存长期记忆
search_memory：查询长期记忆
```

记忆保存在本地文件：

```text
memory.json
```

例如用户输入：

```text
请记住：我叫小姜，我正在学习 AI Agent
```

Agent 会调用 `save_memory`，把内容写入 `memory.json`。

之后用户问：

```text
我叫什么？我正在学什么？
```

Agent 会调用 `search_memory`，从 `memory.json` 中读取之前保存的信息。

### 2. 核心原理

V4 的流程是：

```text
用户要求记住信息
↓
模型选择 save_memory
↓
Python 写入 memory.json
↓
用户询问之前的信息
↓
模型选择 search_memory
↓
Python 读取 memory.json
↓
Agent 根据记忆回答
```

### 3. 长期记忆和短期记忆的区别

| 类型   | 保存位置           | 程序关闭后是否保留 |
| ---- | -------------- | --------- |
| 短期记忆 | messages 变量    | 不保留       |
| 长期记忆 | memory.json 文件 | 保留        |

### 4. 学到的内容

通过 V4，我理解了长期记忆并不是模型本身永久记住了信息，而是程序把信息保存到外部存储中。下次需要时，再读取出来传给模型。

这也是很多真实 Agent 的重要设计思想。

---

## 八、V4 Refactor：模块化重构

### 1. 实现内容

最开始 V4 是一个单文件程序，所有代码都写在一个文件里。

后面我把项目拆分成模块化结构：

```text
agent-study/
│
├── main.py
├── agents/
│   └── personal_agent.py
│
├── tools/
│   ├── calculator.py
│   ├── time_tool.py
│   ├── memory_tool.py
│   ├── planner_tool.py
│   └── progress_tool.py
│
├── utils/
│   └── json_parser.py
│
└── versions/
```

### 2. 每个模块的作用

```text
main.py
```

项目入口，负责启动程序和接收用户输入。

```text
agents/personal_agent.py
```

Agent 核心逻辑，负责工具选择、模型调用、工具执行和结果总结。

```text
tools/
```

存放具体工具函数，比如计算器、时间、记忆、规划、进度记录。

```text
utils/
```

存放通用辅助函数，比如 JSON 解析。

```text
versions/
```

保存 V1 到 V4 的历史版本，方便回顾项目演进过程。

### 3. 学到的内容

通过模块化重构，我理解了项目不能一直写成一个大文件。拆分模块可以让项目结构更清晰，也更方便后续扩展。

---

## 九、V5：任务规划 Agent

### 1. 实现内容

V5 在 V4 的基础上新增了任务规划能力。

新增工具：

```text
make_plan：任务规划工具
```

对应文件：

```text
tools/planner_tool.py
```

当用户输入：

```text
我想两个月后找 Agent 实习，请帮我制定学习计划
```

Agent 会判断这是规划任务，调用 `make_plan` 工具，生成学习计划。

### 2. 核心原理

V5 的流程是：

```text
用户提出目标
↓
decide_tool 判断这是规划任务
↓
模型返回 tool: make_plan
↓
Python 调用 make_plan()
↓
planner_tool 生成结构化 Prompt
↓
大模型根据 Prompt 输出计划
↓
返回给用户
```

### 3. planner_tool.py 的作用

`planner_tool.py` 不是直接生成计划，而是生成一个高质量的规划 Prompt。

它会要求模型按照固定结构输出：

```text
目标分析
阶段拆解
今天立刻执行的 3 个任务
注意事项
```

这让计划输出更稳定、更清晰。

### 4. Planning 的含义

V5 涉及 Agent 中的重要能力：

```text
Planning
任务规划
Task Decomposition
任务拆解
```

也就是把一个大目标拆成多个阶段和具体任务。

### 5. 学到的内容

通过 V5，我理解了 Agent 不只是回答问题，还可以帮助用户拆解目标、制定计划。

这让 Agent 从“聊天助手”进一步变成“任务助手”。

---

## 十、V6：学习进度记录 Agent

### 1. 实现内容

V6 在 V5 的基础上新增了学习进度记录功能。

新增工具：

```text
save_progress：保存学习进度
search_progress：查询学习进度
```

对应文件：

```text
tools/progress_tool.py
```

学习进度保存在：

```text
progress.json
```

例如用户输入：

```text
请记录：我今天完成了 Agent V6 学习进度记录功能
```

Agent 会调用 `save_progress`，把记录写入 `progress.json`。

之后用户问：

```text
我最近完成了什么？
```

Agent 会调用 `search_progress`，查询之前的学习记录。

### 2. 核心原理

V6 的流程是：

```text
用户要求记录学习进度
↓
模型选择 save_progress
↓
Python 写入 progress.json
↓
用户询问学习进度
↓
模型选择 search_progress
↓
Python 读取 progress.json
↓
Agent 总结后回答用户
```

### 3. progress.json 和 memory.json 的区别

| 文件            | 作用                  |
| ------------- | ------------------- |
| memory.json   | 保存用户长期信息，比如名字、目标、偏好 |
| progress.json | 保存学习进度，比如今天完成了什么    |

可以这样理解：

```text
memory.json = 用户档案
progress.json = 学习日志
```

### 4. 学到的内容

通过 V6，我理解了 Agent 可以不只是“记住用户信息”，还可以持续记录用户的任务进展。

这让 Agent 更像一个真正的学习助手。

---

## 十一、Git 和 GitHub 管理过程

在开发过程中，我使用 Git 进行版本管理，并把项目上传到了 GitHub。

核心命令包括：

```powershell
git init
git add .
git commit -m "init agent v4 project"
git push
```

后续开发 V5、V6 时，我使用了 Git 分支：

```text
agent-v5-planner
agent-v6-progress
```

开发流程是：

```text
main 保持稳定
↓
新建功能分支
↓
在分支上开发新功能
↓
测试通过后提交
↓
push 到 GitHub
↓
合并回 main
```

这个过程让我理解了真实项目中常见的分支开发流程。

---

## 十二、Codex 辅助开发过程

在 V6 开发时，我开始使用 Codex 辅助工作。

我没有直接让 Codex 随意修改项目，而是先创建了 `codex.md` 作为规则文件，约束 Codex 的行为。

核心规则包括：

```text
只做用户明确要求的任务
不擅自重构项目
不删除文件
不修改 .env
不引入新依赖
先给计划，再执行修改
```

使用 Codex 时，我采用的流程是：

```text
先让 Codex 阅读项目和 codex.md
↓
让 Codex 输出最小修改计划
↓
我确认计划
↓
Codex 执行具体修改
↓
我自己运行测试
↓
我自己提交 Git
```

这个过程让我理解了如何把 AI 编程工具作为助手，而不是完全依赖它。

---

## 十三、项目当前能力总结

当前项目已经具备以下能力：

```text
普通聊天
计算器工具
当前时间工具
长期记忆
任务规划
学习进度记录
GitHub 项目管理
模块化项目结构
```

用户可以输入：

```text
帮我计算 120 * 35
```

Agent 会调用计算器工具。

用户可以输入：

```text
请记住：我叫小姜，我正在学习 AI Agent
```

Agent 会保存到长期记忆。

用户可以输入：

```text
我想两个月后找 Agent 实习，请帮我制定学习计划
```

Agent 会调用任务规划工具。

用户可以输入：

```text
请记录：我今天完成了 Agent V6
```

Agent 会保存学习进度。

---

## 十四、项目中理解最深的核心概念

### 1. Agent Loop

Agent 的基本循环是：

```text
输入 → 判断 → 执行 → 输出
```

### 2. Tool Calling

大模型负责选择工具，Python 负责执行工具。

```text
大模型：判断应该做什么
Python：真正执行任务
Agent：连接模型和工具
```

### 3. Memory

记忆不是模型自动永久保存的，而是程序把信息写入文件。

```text
memory.json：保存长期用户信息
progress.json：保存学习进度
```

### 4. Planning

Planning 是把大目标拆成多个阶段和任务。

```text
目标 → 阶段 → 任务 → 今日行动
```

### 5. 模块化

模块化让项目更清晰：

```text
agents/ 负责 Agent 逻辑
tools/ 负责具体工具
utils/ 负责辅助函数
main.py 负责启动
```

---

## 十五、项目不足

当前项目仍然有一些不足：

1. 工具选择依赖大模型返回 JSON，稳定性还可以继续提升。
2. 记忆和进度只是简单 JSON 文件，没有使用数据库。
3. search_memory 和 search_progress 只是简单关键词匹配，不够智能。
4. 还没有网页界面，目前只能在命令行中使用。
5. 还没有 RAG，不能读取外部文档知识库。
6. 没有任务状态系统，比如“未开始、进行中、已完成”。
7. 没有自动测试文件。

---

## 十六、下一步计划

下一步可以继续开发：

### V7：任务状态管理 Agent

目标：

```text
让 Agent 管理任务状态
```

例如：

```text
任务：学习 RAG
状态：进行中

任务：完成 Agent V6
状态：已完成
```

### V8：Streamlit 网页界面

目标：

```text
给 Agent 增加简单网页界面
```

### V9：RAG 文档问答 Agent

目标：

```text
让 Agent 可以读取文档，并基于文档回答问题
```

### V10：项目作品集完善

目标：

```text
完善 README
补充截图
准备简历描述
准备面试讲解
```

---

## 十七、面试介绍版本

如果面试官问我这个项目，我可以这样介绍：

> 这是我从零开始做的一个 AI Agent 学习项目。我没有一开始直接使用复杂框架，而是先用 Python 手写 Agent 的核心流程。
> V1 是规则 Agent，用 if 判断用户输入。V2 接入大模型 API，实现动态聊天。V3 增加工具调用，让模型选择 calculator、get_time 等工具，由 Python 执行。V4 加入长期记忆，用 memory.json 保存用户信息。V5 增加任务规划能力，可以根据用户目标生成学习计划。V6 增加学习进度记录，用 progress.json 保存用户完成过的任务。
> 这个项目让我理解了 Agent 的几个核心部分：大模型负责理解和决策，工具负责执行任务，记忆负责保存上下文，程序负责把这些模块连接起来。

---

## 十八、一句话总结

这个项目的核心价值是：

> 我通过从 V1 到 V6 的逐步开发，完整理解了一个 AI Agent 从规则判断、大模型聊天、工具调用、长期记忆、任务规划到进度追踪的演进过程。
## V7：任务状态管理 Agent
V7 在 V6 的学习进度记录基础上，新增了任务状态管理能力。

新增工具：
- add_task：添加任务
- update_task_status：更新任务状态
- search_tasks：查询任务

任务数据保存在 tasks.json 中，格式包括 title、status、created_at、updated_at。

V7 的核心原理是：
用户输入任务相关请求后，decide_tool() 让大模型判断应该调用哪个任务工具。
如果用户要求添加任务，就调用 add_task。
如果用户要求修改状态，就调用 update_task_status。
如果用户查询任务列表，就调用 search_tasks。
Python 工具负责读写 tasks.json，大模型负责理解意图和整理回答。

V7 让我理解了 Agent 不只是记录学习日志，还可以管理任务状态。
## V8：Streamlit 网页界面

V8 在前面命令行 Agent 的基础上，新增了一个 Streamlit 网页界面。

在 V8 之前，Agent 只能通过终端运行，用户需要在命令行输入问题。V8 新增了 `app.py`，让用户可以在浏览器中和 Agent 对话。

V8 主要新增内容：

- 新建 `app.py`
- 在 `requirements.txt` 中新增 `streamlit`
- 使用 `st.chat_input()` 接收用户输入
- 使用 `st.chat_message()` 展示用户和 Agent 的对话
- 使用 `st.session_state` 保存网页会话状态
- 复用原有 `PersonalAgent`，不重写 Agent 核心逻辑

V8 的核心原理是：

用户在网页输入问题后，Streamlit 页面把输入传给 `PersonalAgent.run_once()`，Agent 继续按照原来的工具调用流程处理问题，然后把回答返回到网页显示。

V8 让我理解了如何把一个命令行 AI Agent 包装成可以在浏览器中使用的简单 Web 应用。
## V9：本地知识库问答 Agent

V9 在 V8 网页版 Agent 的基础上，新增了本地知识库问答能力。

本版本没有使用向量数据库，也没有使用 embedding，而是先实现一个简单版 RAG 流程：

用户提问
↓
Agent 判断需要查询知识库
↓
调用 search_knowledge 工具
↓
读取 knowledge/knowledge.txt
↓
按段落搜索相关内容
↓
把检索结果交给大模型总结回答

V9 新增文件：

- knowledge/knowledge.txt：本地知识库内容
- tools/knowledge_tool.py：知识库读取与搜索工具

V9 修改文件：

- agents/personal_agent.py：接入 search_knowledge 工具

V9 的核心原理是 RAG，也就是 Retrieval-Augmented Generation，检索增强生成。它不是直接让大模型凭空回答，而是先从本地知识库中找出相关内容，再让大模型基于这些内容回答。

这个版本让我理解了 RAG 的基础流程：文档读取、文本切分、内容检索、基于上下文回答。