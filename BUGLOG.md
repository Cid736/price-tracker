# Bug Log — Price Tracker

No se han encontrado vulnerabilidades ni bugs significativos en la revisión automatizada de seguridad del 2026-06-25 (revisiones 1 y 2).

---

## 2026-06-25 — Revisión 3

### [MEDIUM] `/api/products/<pid>/check` accesible sin autenticación (SSRF amplification)
- **Archivo:** `web.py` línea 33
- **Fix:** Añadida función `_check_local()`: requiere `X-Control-Token` si la variable de entorno `CONTROL_TOKEN` está definida, o restringe el acceso a `127.0.0.1`/`::1` en caso contrario.
