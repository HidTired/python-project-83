import re
from urllib.parse import urlparse, urlunparse


def normalize_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, '', '', '', ''))


def validate(url):
    """Валидация URL"""
    if not url:
        return {"name": "URL обязателен"}
    
    if not re.match(r'^https?://[^\s<>"]+|www\.[^\s<>"]+', url):
        return {"name": "Некорректный URL"}
    
    return None