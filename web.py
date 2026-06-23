from flask import Flask, jsonify, send_from_directory
import os
from db import init_db, get_conn

app = Flask(__name__, static_folder='public')

@app.route('/')
def index():
    return send_from_directory('public', 'dashboard.html')

@app.route('/api/products')
def products():
    with get_conn() as c:
        rows = c.execute('''
            SELECT p.id, p.name, p.url, p.threshold,
                   (SELECT price FROM price_history WHERE product_id=p.id ORDER BY checked_at DESC LIMIT 1) last_price,
                   (SELECT MIN(price) FROM price_history WHERE product_id=p.id) min_price,
                   (SELECT MAX(price) FROM price_history WHERE product_id=p.id) max_price,
                   (SELECT COUNT(*) FROM price_history WHERE product_id=p.id) checks
            FROM products p WHERE active=1
        ''').fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/products/<int:pid>/history')
def history(pid):
    with get_conn() as c:
        rows = c.execute(
            'SELECT price, checked_at FROM price_history WHERE product_id=? ORDER BY checked_at',
            (pid,)
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/products/<int:pid>/check', methods=['POST'])
def check_one(pid):
    from tracker import fetch_price
    with get_conn() as c:
        p = c.execute('SELECT * FROM products WHERE id=? AND active=1', (pid,)).fetchone()
    if not p:
        return jsonify({'error': 'Producto no encontrado'}), 404
    price = fetch_price(p['url'], p['selector'])
    if price is None:
        return jsonify({'error': 'No se pudo obtener el precio'}), 502
    with get_conn() as c:
        c.execute('INSERT INTO price_history(product_id,price) VALUES(?,?)', (pid, price))
    alert = bool(p['threshold'] and price <= p['threshold'])
    return jsonify({'price': price, 'alert': alert})

if __name__ == '__main__':
    init_db()
    print('Dashboard -> http://localhost:5000')
    app.run(port=5000, debug=False)
