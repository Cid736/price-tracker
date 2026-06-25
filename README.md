<p align="center">
  <a href="#english">🇬🇧 English</a> &nbsp;·&nbsp; <a href="#español">🇪🇸 Español</a>
</p>

---

<a name="english"></a>

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

## Security

Automated security reviews are powered by [Claude](https://claude.ai) (Anthropic AI) and run on every significant change to detect vulnerabilities, insecure patterns and dependency risks. Findings are tracked in [`BUGLOG.md`](BUGLOG.md).

**Last review:** 2026-06-25 — No significant issues found.

Found a vulnerability? Open an issue or contact directly.

---

<a name="español"></a>

# Price Tracker

Monitoriza precios de cualquier web y recibe alertas por Telegram cuando bajen de tu umbral.

## Stack
Python · requests · BeautifulSoup4 · SQLite · Telegram Bot API

## Instalación
```bash
pip install -r requirements.txt
cp .env.example .env  # añade tu TELEGRAM_TOKEN y TELEGRAM_CHAT_ID
```

## Uso
```bash
# Añadir un producto a monitorizar
python main.py add https://tienda.com/producto --name "Auriculares" --threshold 49.99

# Comprobar precios ahora
python main.py check

# Ver todos los productos monitorizados
python main.py list

# Historial de precios
python main.py history

# Ejecutar como demonio (cada 60 min)
python main.py run --interval 60
```

## Características
- Compatible con cualquier web de e-commerce (lee meta tags Open Graph de precio + patrones CSS comunes)
- Soporte de selector CSS personalizado para cualquier layout
- Historial de precios en SQLite
- Alerta Telegram cuando el precio baja del umbral

## Seguridad

Las revisiones de seguridad automatizadas utilizan [Claude](https://claude.ai) (Anthropic AI) y se ejecutan en cada cambio significativo para detectar vulnerabilidades, patrones inseguros y riesgos en dependencias. Los hallazgos se registran en [`BUGLOG.md`](BUGLOG.md).

**Última revisión:** 2026-06-25 (rev 3) — 1 vulnerabilidad encontrada (media) — parcheada. Revisión 3: `/api/products/<pid>/check` protegido — solo accesible desde localhost o con `CONTROL_TOKEN`.

¿Encontraste una vulnerabilidad? Abre un issue o contacta directamente.
## Licencia

MIT
