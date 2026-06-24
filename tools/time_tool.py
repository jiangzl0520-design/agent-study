from datetime import datetime


def get_current_time():
    """
    获取当前本地时间。
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")