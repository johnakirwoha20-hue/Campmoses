from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'app_py.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/notes', methods=['GET'])
def list_notes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, content, created_at FROM notes ORDER BY id DESC')
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/notes', methods=['POST'])
def create_note():
    data = request.get_json(force=True) or {}
    content = data.get('content')
    if not content:
        return jsonify({'error': 'content is required'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    conn.commit()
    nid = cur.lastrowid
    conn.close()
    return jsonify({'id': nid, 'content': content}), 201

# Serve static files (index.html, img/)
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def static_proxy(path):
    # Security: ensure requests stay within project folder
    full = os.path.join(BASE_DIR, path)
    if os.path.isfile(full):
        return send_from_directory(BASE_DIR, path)
    return send_from_directory(BASE_DIR, 'index.html')

if __name__ == '__main__':
    init_db()
    # default to port 8000 to avoid colliding with Node server on 3000
    app.run(host='0.0.0.0', port=8000)
