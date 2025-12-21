import requests
from bs4 import BeautifulSoup

def normalize_url(url):
    # Простая нормализация (добавьте если нет)
    from urllib.parse import urlparse, urlunparse
    parsed = urlparse(url)
    return urlunparse(parsed._replace(path=parsed.path.rstrip('/'), query=''))

def validate(url):
    errors = {}
    if not url:
        errors["url"] = "URL обязателен"
    elif not url.startswith(("http://", "https://")):
        errors["url"] = "Некорректный URL"
    return errors
def check_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  


        soup = BeautifulSoup(response.text, "html.parser")


        h1_tag = soup.find("h1")
        h1_content = h1_tag.text.strip() if h1_tag else ""


        title_tag = soup.find("title")
        title_content = title_tag.text.strip() if title_tag else ""


        meta_desc = soup.find("meta", attrs={"name": "description"})
        description_content = (
            meta_desc.get("content", "").strip() if meta_desc else ""
        )

        return {
            "h1": h1_content,
            "title": title_content,
            "description": description_content,
        }

    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None