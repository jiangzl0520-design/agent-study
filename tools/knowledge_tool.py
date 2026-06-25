import re
from pathlib import Path


KNOWLEDGE_FILE = Path("knowledge/knowledge.txt")


def load_knowledge():
    """
    读取本地知识库文本。
    """
    if not KNOWLEDGE_FILE.exists():
        return "知识库文件不存在，请先创建 knowledge/knowledge.txt。"

    content = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    if not content.strip():
        return "知识库文件是空的。"

    return content


def split_knowledge(text):
    """
    按空行切分知识库段落。
    """
    paragraphs = re.split(r"\n\s*\n", text)
    return [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]


def search_knowledge(query, top_k=3):
    """
    使用简单关键词匹配搜索知识库。
    """
    text = load_knowledge()

    if text.startswith("知识库文件不存在") or text.startswith("知识库文件是空的"):
        return text

    paragraphs = split_knowledge(text)
    keywords = re.split(r"\s+|，|。|、|\?|？|！|!|：|:|,|\.", query)
    keywords = [word for word in keywords if word.strip()]

    scored_results = []

    for paragraph in paragraphs:
        score = 0

        for keyword in keywords:
            if keyword in paragraph:
                score += 1

        if score > 0:
            scored_results.append((score, paragraph))

    if not scored_results:
        return "知识库中没有找到相关内容"

    scored_results.sort(key=lambda item: item[0], reverse=True)
    results = [paragraph for _, paragraph in scored_results[:top_k]]

    return "\n\n".join(results)
