import os
import requests
from dotenv import load_dotenv

load_dotenv()

_TOKEN   = os.getenv('TELEGRAM_TOKEN')
_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_alert(name, price, url, threshold):
    if not _TOKEN or not _CHAT_ID:
        return
    text = (
        f'*Bajada de precio detectada*\n\n'
        f'{name}\n'
        f'Precio actual: *{price:.2f} EUR*\n'
        f'Tu umbral: {threshold:.2f} EUR\n\n'
        f'[Ver producto]({url})'
    )
    try:
        requests.post(
            f'https://api.telegram.org/bot{_TOKEN}/sendMessage',
            json={'chat_id': _CHAT_ID, 'text': text, 'parse_mode': 'Markdown'},
            timeout=10,
        )
    except Exception:
        pass
