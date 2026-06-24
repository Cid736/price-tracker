# Price Tracker

Monitoriza precios de cualquier web y recibe alertas por Telegram cuando bajan de tu umbral.

## Stack
Python · requests · BeautifulSoup4 · SQLite · Telegram Bot API

## Instalacion
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

## Funcionalidades
- Compatible con cualquier tienda online (lee meta tags Open Graph + patrones CSS comunes)
- Soporte para selector CSS personalizado para cualquier layout
- Historial de precios en SQLite
- Alerta por Telegram cuando el precio baja del umbral

## Historial de versiones

**v0.1.1** — 2026-06-24
- Fix: añadido try/except en el notificador de Telegram para evitar crash no controlado si la red falla

**v0.1.0** — 2026-05-01
- Publicación inicial: scraping de precios, alertas por umbral, historial SQLite, modo demonio
