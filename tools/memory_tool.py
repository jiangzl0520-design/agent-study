import json
import re
from pathlib import Path

from tools.time_tool import get_current_time


MEMORY_FILE = Path("memory.json")


def load_memory():
    """
    读取长期记忆。
    如果 memory.json 不存在，就返回空记忆。
    """
    if not MEMORY_FILE.exists():
        return {"facts": []}

    try:
        content = MEMORY_FILE.read_text(encoding="utf-8")
        return json.loads(content)
    except Exception:
        return {"facts": []}


def write_memory(data):
    """
    写入长期记忆。
    """
    MEMORY_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def save_memory(content):
    """
    保存一条长期记忆。
    """
    data = load_memory()

    fact = {
        "content": content,
        "created_at": get_current_time()
    }

    data["facts"].append(fact)
    write_memory(data)

    return f"已保存长期记忆：{content}"


def search_memory(query):
    """
    搜索长期记忆。
    """
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

    if not matches:
        matches = facts

    result = []

    for index, fact in enumerate(matches, start=1):
        result.append(
            f"{index}. {fact['content']}（保存时间：{fact['created_at']}）"
        )

    return "\n".join(result)