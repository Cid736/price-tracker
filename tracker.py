import requests
from bs4 import BeautifulSoup
import re, ipaddress
from urllib.parse import urlparse

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

def _resolve_safe(host: str) -> bool:
    """Return True only if ALL resolved IPs for host are public/routable."""
    import socket
    try:
        results = socket.getaddrinfo(host, None)
    except Exception:
        return False
    for res in results:
        ip_str = res[4][0]
        try:
            addr = ipaddress.ip_address(ip_str)
            if (addr.is_private or addr.is_loopback or addr.is_link_local
                    or addr.is_reserved or addr.is_multicast
                    or addr.is_unspecified):
                return False
        except ValueError:
            return False
    return bool(results)


def _is_safe_url(url: str) -> bool:
    try:
        p = urlparse(url)
        if p.scheme not in ('http', 'https'):
            return False
        host = (p.hostname or '').lower()
        if not host or host == 'localhost':
            return False
        # Reject bare IP literals that are private
        try:
            addr = ipaddress.ip_address(host)
            if (addr.is_private or addr.is_loopback or addr.is_link_local
                    or addr.is_reserved or addr.is_multicast
                    or addr.is_unspecified):
                return False
            # IP literal is public — allow
            return True
        except ValueError:
            pass  # hostname, not IP literal — fall through to DNS check
        # DNS rebinding protection: resolve now and verify all IPs are public
        return _resolve_safe(host)
    except Exception:
        return False

def fetch_price(url, selector=None):
    if not _is_safe_url(url):
        print(f'  [!] URL bloqueada (privada o inválida): {url}')
        return None
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return _extract(r.text, selector)

    except Exception as e:
        print(f'  [!] Error en {url}: {e}')
        return None
