import json
import re
from pathlib import Path

from tools.time_tool import get_current_time


TASKS_FILE = Path("tasks.json")
VALID_STATUSES = {"未开始", "进行中", "已完成"}


def load_tasks():
    """
    读取任务列表。
    如果 tasks.json 不存在，就返回空任务列表。
    """
    if not TASKS_FILE.exists():
        return {"tasks": []}

    try:
        content = TASKS_FILE.read_text(encoding="utf-8")
        return json.loads(content)
    except Exception:
        return {"tasks": []}


def write_tasks(data):
    """
    写入任务列表。
    """
    TASKS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def add_task(title, status="未开始"):
    """
    添加一个任务。
    """
    if status not in VALID_STATUSES:
        status = "未开始"

    data = load_tasks()
    now = get_current_time()

    task = {
        "title": title,
        "status": status,
        "created_at": now,
        "updated_at": now
    }

    data["tasks"].append(task)
    write_tasks(data)

    return f"已添加任务：{title}，状态：{status}"


def update_task_status(title, status):
    """
    更新任务状态。
    """
    if status not in VALID_STATUSES:
        return "任务状态只能是：未开始、进行中、已完成。"

    data = load_tasks()
    tasks = data.get("tasks", [])

    matches = []

    for task in tasks:
        if title in task["title"]:
            matches.append(task)

    if not matches:
        return f"没有找到任务：{title}"

    if len(matches) > 1:
        result = ["找到多个匹配任务，请说得更具体一点："]

        for index, task in enumerate(matches, start=1):
            result.append(f"{index}. {task['title']}（当前状态：{task['status']}）")

        return "\n".join(result)

    task = matches[0]
    task["status"] = status
    task["updated_at"] = get_current_time()
    write_tasks(data)

    return f"已更新任务：{task['title']}，当前状态：{status}"


def search_tasks(query):
    """
    搜索任务。
    """
    data = load_tasks()
    tasks = data.get("tasks", [])

    if not tasks:
        return "目前没有任务。"

    keywords = re.split(r"\s+|，|。|、|\?|？|！|!|：|:", query)
    keywords = [word for word in keywords if word.strip()]

    matches = []

    for task in tasks:
        title = task["title"]
        status = task["status"]

        if any(keyword in title or keyword in status for keyword in keywords):
            matches.append(task)

    if not matches:
        matches = tasks

    result = []

    for index, task in enumerate(matches, start=1):
        result.append(
            f"{index}. {task['title']}（状态：{task['status']}，创建时间：{task['created_at']}，更新时间：{task['updated_at']}）"
        )

    return "\n".join(result)
