from urllib.parse import urlparse, urlunparse

import validators


def normalize_url(url):
    """Нормализует URL до scheme://netloc"""
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, '', '', '', ''))


def validate_url(url):
    """Валидация URL с подробными ошибками"""
    if not url:
        return {"name": "URL обязателен"}
    
    if len(url) > 255:
        return {"name": "URL превышает 255 символов"}
    
    if not validators.url(url):
        return {"name": "Некорректный URL"}
    
    return None