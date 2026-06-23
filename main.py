#!/usr/bin/env python3
import argparse, sys, time
from db       import init_db, get_conn
from tracker  import fetch_price
from notifier import send_alert

def cmd_add(a):
    price = fetch_price(a.url, a.selector)
    if price is None:
        sys.exit('[ERROR] No se pudo obtener el precio. Prueba con --selector <css>.')
    name = a.name or a.url.split('/')[2]
    with get_conn() as c:
        try:
            c.execute(
                'INSERT INTO products(name,url,selector,threshold) VALUES(?,?,?,?)',
                (name, a.url, a.selector, a.threshold)
            )
            pid = c.execute('SELECT last_insert_rowid()').fetchone()[0]
            c.execute('INSERT INTO price_history(product_id,price) VALUES(?,?)', (pid, price))
        except Exception as e:
            sys.exit(f'Error: {e}')
    print(f'[OK] {name} — {price:.2f} EUR' + (f'  (alerta < {a.threshold:.2f} EUR)' if a.threshold else ''))

def cmd_list(_):
    with get_conn() as c:
        rows = c.execute('''
            SELECT p.id, p.name, p.url, p.threshold,
                   (SELECT price FROM price_history WHERE product_id=p.id ORDER BY checked_at DESC LIMIT 1) price
            FROM products p WHERE active=1
        ''').fetchall()
    if not rows:
        return print('Sin productos monitorizados.')
    print(f'\n{"#":<4} {"Nombre":<26} {"Precio":<10} {"Umbral":<10} URL')
    print('-' * 85)
    for r in rows:
        p = f'{r["price"]:.2f} €' if r['price'] else '—'
        t = f'{r["threshold"]:.2f} €' if r['threshold'] else '—'
        print(f'{r["id"]:<4} {r["name"][:25]:<26} {p:<10} {t:<10} {r["url"][:40]}')
    print()

def cmd_check(_):
    with get_conn() as c:
        products = c.execute('SELECT * FROM products WHERE active=1').fetchall()
    if not products:
        return print('Sin productos activos.')
    for p in products:
        price = fetch_price(p['url'], p['selector'])
        if price is None:
            continue
        with get_conn() as c:
            c.execute('INSERT INTO price_history(product_id,price) VALUES(?,?)', (p['id'], price))
        alert = p['threshold'] and price <= p['threshold']
        print(f'{"[ALERTA]" if alert else "[OK]"} {p["name"]}: {price:.2f} EUR')
        if alert:
            send_alert(p['name'], price, p['url'], p['threshold'])

def cmd_history(a):
    with get_conn() as c:
        rows = c.execute('''
            SELECT p.name, h.price, h.checked_at
            FROM price_history h JOIN products p ON p.id=h.product_id
            WHERE (? IS NULL OR p.id=?)
            ORDER BY h.checked_at DESC LIMIT 50
        ''', (a.id, a.id)).fetchall()
    if not rows:
        return print('Sin historial.')
    print(f'\n{"Producto":<26} {"Precio":<10} Fecha')
    print('-' * 55)
    for r in rows:
        print(f'{r["name"][:25]:<26} {r["price"]:.2f} €  {r["checked_at"]}')
    print()

def cmd_remove(a):
    with get_conn() as c:
        c.execute('UPDATE products SET active=0 WHERE id=?', (a.id,))
    print(f'Producto #{a.id} eliminado.')

def cmd_run(a):
    print(f'Comprobando cada {a.interval} minutos. Ctrl+C para parar.\n')
    while True:
        cmd_check(a)
        time.sleep(a.interval * 60)

def main():
    init_db()
    ap = argparse.ArgumentParser(description='Price Tracker — alertas Telegram cuando baja el precio')
    sp = ap.add_subparsers(dest='cmd', required=True)

    p = sp.add_parser('add', help='Añadir producto a monitorizar')
    p.add_argument('url');  p.add_argument('-n', '--name'); p.add_argument('-t', '--threshold', type=float, metavar='PRECIO', help='Alerta si baja de este precio'); p.add_argument('-s', '--selector', metavar='CSS', help='Selector CSS del elemento precio'); p.set_defaults(func=cmd_add)

    p = sp.add_parser('list', help='Ver productos monitorizados'); p.set_defaults(func=cmd_list)
    p = sp.add_parser('check', help='Comprobar precios ahora'); p.set_defaults(func=cmd_check)

    p = sp.add_parser('history', help='Historial de precios')
    p.add_argument('--id', type=int, help='ID del producto (todos si no se indica)'); p.set_defaults(func=cmd_history)

    p = sp.add_parser('remove', help='Dejar de monitorizar')
    p.add_argument('id', type=int); p.set_defaults(func=cmd_remove)

    p = sp.add_parser('run', help='Ejecutar en bucle')
    p.add_argument('-i', '--interval', type=int, default=60, metavar='MIN', help='Minutos entre comprobaciones (default: 60)'); p.set_defaults(func=cmd_run)

    args = ap.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
