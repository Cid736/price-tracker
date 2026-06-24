# Price Tracker

Monitor prices from any website and get Telegram alerts when they drop below your threshold.

## Stack
Python · requests · BeautifulSoup4 · SQLite · Telegram Bot API

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env  # add your TELEGRAM_TOKEN and TELEGRAM_CHAT_ID
```

## Usage
```bash
# Add a product to monitor
python main.py add https://store.com/product --name "Headphones" --threshold 49.99

# Check prices now
python main.py check

# View all monitored products
python main.py list

# Price history
python main.py history

# Run as daemon (every 60 min)
python main.py run --interval 60
```

## Features
- Works with any e-commerce site (reads Open Graph price meta tags + common CSS patterns)
- Custom CSS selector support for any site layout
- SQLite price history
- Telegram alert when price drops below threshold

## Changelog

**v0.1.1** — 2026-06-24
- Security: SSRF protection on user-supplied URLs — private IPs, loopback and non-HTTP schemes are blocked
- Fix: Telegram notifier now catches network errors instead of crashing

**v0.1.0** — 2026-05-01
- Initial release: price scraping, threshold alerts, SQLite history, daemon mode
