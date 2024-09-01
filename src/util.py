from datetime import datetime


def parse_date(date_str: str | None) -> datetime | None: 
    """given ollama's instructed date format of YYYY-MM-DD HH:MM, returns a datetime object"""
    if date_str is None: return
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
