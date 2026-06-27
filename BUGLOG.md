# Bug Log — Price Tracker

No se han encontrado vulnerabilidades ni bugs significativos en la revisión automatizada de seguridad del 2026-06-25 (revisiones 1 y 2).

---

## 2026-06-25 — Revisión 3

### [MEDIUM] `/api/products/<pid>/check` accesible sin autenticación (SSRF amplification)
- **Archivo:** `web.py` línea 33
- **Fix:** Añadida función `_check_local()`: requiere `X-Control-Token` si la variable de entorno `CONTROL_TOKEN` está definida, o restringe el acceso a `127.0.0.1`/`::1` en caso contrario.

---

## 2026-06-28 — Revisión 4

### [HIGH] DNS Rebinding — SSRF bypass vía hostname
- **Archivo:** `tracker.py` línea 34–50
- **Descripción:** `_is_safe_url()` solo rechazaba IPs privadas literales en la URL. Un atacante podía usar un hostname público (ej. `attacker.com`) que resolviera a una IP interna (ej. `192.168.1.1`). La comprobación pasaba y el scraper realizaba la petición a la red interna.
- **Fix:** Añadida función `_resolve_safe()` que ejecuta `socket.getaddrinfo()` para el hostname antes de la petición y verifica que TODOS los IPs resueltos sean públicos. Si alguno es privado/loopback/reservado, la URL se bloquea.

### [MEDIUM] Inyección en mensajes Telegram (MarkdownV1)
- **Archivo:** `notifier.py` líneas 10–25
- **Descripción:** El nombre del producto y la URL (ambos provenientes de input del usuario) se insertaban sin escapar en un mensaje con `parse_mode: 'Markdown'`. Un atacante podía inyectar texto con formato arbitrario o links maliciosos en la alerta.
- **Fix:** Migrado a `parse_mode: 'MarkdownV2'` con función `_escape_md2()` que escapa todos los caracteres especiales en campos controlados por el usuario.

### [LOW] Cabecera Content-Security-Policy ausente
- **Archivo:** `web.py` líneas 19–24
- **Descripción:** Sin CSP, el dashboard era vulnerable a ataques XSS basados en inyección de scripts externos.
- **Fix:** Añadida cabecera `Content-Security-Policy` restringiendo scripts a `'self'` y `cdn.jsdelivr.net`.

### [LOW] Dependencias vulnerables y sin declarar
- **Archivo:** `requirements.txt`
- **Descripción:** `requests==2.31.0` tiene CVEs conocidos (CVE-2023-32681). `flask` y `lxml` se usaban pero no estaban declaradas en requirements.txt.
- **Fix:** Actualizado a `requests==2.32.3`, añadidos `flask==3.0.3` y `lxml==5.2.2`.
