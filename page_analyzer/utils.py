from urllib.parse import urlparse
from bs4 import BeautifulSoup
from validators.url import url as validate_url


def normalize_url(url):
    result = urlparse(url)
    new_result = result._replace(path="", params="", query="", fragment="")
    return new_result.geturl()


def parse_html(html):
    soup = BeautifulSoup(html.text, "lxml")
    title = soup.find("title")
    h1 = soup.find("h1")
    description = soup.find("meta", attrs={"name": "description"})
    return {
        "title": title.text if title else None,
        "h1": h1.text if h1 else None,
        "description": (
            description["content"]
            if description and "content" in description.attrs
            else None
        ),
    }


def validate(url):
    errors = {}
    if not url:
        errors["url"] = "URL не должен быть пустым"
    elif len(url) >= 255:
        errors["url"] = "URL должен быть короче 255 символов"
    elif not validate_url(url):
        errors["url"] = "Некорректный URL"
    return errors
