import json
import re
from pathlib import Path

from tools.time_tool import get_current_time


PROGRESS_FILE = Path("progress.json")


def load_progress():
    """
    读取学习进度。
    如果 progress.json 不存在，就返回空记录。
    """
    if not PROGRESS_FILE.exists():
        return {"records": []}

    try:
        content = PROGRESS_FILE.read_text(encoding="utf-8")
        return json.loads(content)
    except Exception:
        return {"records": []}


def write_progress(data):
    """
    写入学习进度。
    """
    PROGRESS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def save_progress(content):
    """
    保存一条学习进度。
    """
    data = load_progress()

    record = {
        "content": content,
        "created_at": get_current_time()
    }

    data["records"].append(record)
    write_progress(data)

    return f"已保存学习进度：{content}"


def search_progress(query):
    """
    搜索学习进度。
    """
    data = load_progress()
    records = data.get("records", [])

    if not records:
        return "目前没有学习进度记录。"

    keywords = re.split(r"\s+|，|。|、|\?|？|！|!", query)
    keywords = [word for word in keywords if word.strip()]

    matches = []

    for record in records:
        content = record["content"]

        if any(keyword in content for keyword in keywords):
            matches.append(record)

    if not matches:
        matches = records

    result = []

    for index, record in enumerate(matches, start=1):
        result.append(
            f"{index}. {record['content']}（记录时间：{record['created_at']}）"
        )

    return "\n".join(result)
