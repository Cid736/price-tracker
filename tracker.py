import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
}

def _parse_price(text):
    text = str(text).replace(' ', '').replace(',', '.')
    m = re.search(r'\d+\.?\d*', text)
    return float(m.group()) if m else None

def _extract(html, selector=None):
    soup = BeautifulSoup(html, 'html.parser')
    if selector:
        el = soup.select_one(selector)
        if el:
            return _parse_price(el.get_text())
    for prop in ('product:price:amount', 'og:price:amount'):
        tag = soup.find('meta', property=prop) or soup.find('meta', attrs={'name': prop})
        if tag and tag.get('content'):
            return _parse_price(tag['content'])
    for pattern in (r'price', r'precio', r'sale.?price', r'offer.?price'):
        el = soup.find(class_=re.compile(pattern, re.I))
        if el:
            p = _parse_price(el.get_text())
            if p:
                return p
    return None

def fetch_price(url, selector=None):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return _extract(r.text, selector)

    except Exception as e:
        print(f'  [!] Error en {url}: {e}')
        return None
