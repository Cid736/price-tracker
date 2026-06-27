import os
import requests
from dotenv import load_dotenv

load_dotenv()

_TOKEN   = os.getenv('TELEGRAM_TOKEN')
_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def _escape_md2(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    special = r'\_*[]()~`>#+-=|{}.!'
    return ''.join('\\' + c if c in special else c for c in str(text))


def send_alert(name, price, url, threshold):
    if not _TOKEN or not _CHAT_ID:
        return
    # Use MarkdownV2 — all user-supplied strings are escaped to prevent injection
    text = (
        f'*Bajada de precio detectada*\n\n'
        f'{_escape_md2(name)}\n'
        f'Precio actual: *{_escape_md2(f"{price:.2f}")} EUR*\n'
        f'Tu umbral: {_escape_md2(f"{threshold:.2f}")} EUR\n\n'
        f'[Ver producto]({_escape_md2(url)})'
    )
    try:
        resp = requests.post(
            f'https://api.telegram.org/bot{_TOKEN}/sendMessage',
            json={'chat_id': _CHAT_ID, 'text': text, 'parse_mode': 'MarkdownV2'},
            timeout=10,
        )
        resp.raise_for_status()
    except Exception as e:
        print(f'  [!] Error al enviar alerta Telegram: {e}')
