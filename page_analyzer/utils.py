import requests
from bs4 import BeautifulSoup
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

def check_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')

        h1 = soup.find('h1')
        h1_text = h1.get_text(strip=True) if h1 else ''

        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else ''
        
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        description = desc_tag.get('content', '').strip() if desc_tag else ''
        
        return {
            'status_code': response.status_code,  
            'h1': h1_text[:255],       
            'title': title[:255],
            'description': description[:255]
        }
    except:
        return None