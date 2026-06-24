import json
import re


def extract_json(text):
    """
    尽量从模型回复里提取 JSON。
    有些模型可能会返回 ```json ... ```，所以这里做了兼容处理。
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return json.loads(match.group())

    raise ValueError("模型没有返回有效 JSON")