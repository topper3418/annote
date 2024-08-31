from datetime import datetime


def parse_date(date_str: str) -> datetime: 
    """given ollama's instructed date format of YYYY-MM-DD HH:MM, returns a datetime object"""
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
