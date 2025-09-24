"""
servidor.py
API REST mínima con:
- POST /registro   -> crear usuario (almacena contraseña hasheada)
- POST /login      -> verificar credenciales
- GET  /tareas     -> página HTML de bienvenida (protegida con HTTP Basic Auth)

Dependencias principales:
- Flask
- Flask-HTTPAuth
- passlib[bcrypt]
"""

from flask import Flask, request, g, jsonify, abort, render_template_string
from flask_httpauth import HTTPBasicAuth
from passlib.hash import bcrypt
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.sqlite")

app = Flask(__name__)
auth = HTTPBasicAuth()


# ---------- DB helpers ----------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    db = sqlite3.connect(DB_PATH)
    c = db.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """
    )
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        done INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """
    )
    db.commit()
    db.close()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# Initialize DB at startup if missing
if not os.path.exists(DB_PATH):
    init_db()


# ---------- User model helpers ----------
def create_user(username: str, password: str):
    hashed = bcrypt.hash(password)
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed),
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def get_user_by_username(username: str):
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    return row


def verify_user(username: str, password: str) -> bool:
    row = get_user_by_username(username)
    if not row:
        return False
    return bcrypt.verify(password, row["password_hash"])


# ---------- Sample tasks ----------
def add_sample_task_for_user(user_id: int, title: str):
    db = get_db()
    db.execute("INSERT INTO tasks (user_id, title) VALUES (?, ?)", (user_id, title))
    db.commit()


def ensure_sample_tasks():
    db = get_db()
    cur = db.execute("SELECT COUNT(*) as c FROM tasks")
    count = cur.fetchone()["c"]
    if count == 0:
        # create a demo user if none exists
        cur2 = db.execute("SELECT id FROM users LIMIT 1")
        row = cur2.fetchone()
        if not row:
            # create demo user demo/demo
            create_user("demo", "demo")
            row = db.execute(
                "SELECT id FROM users WHERE username = ?", ("demo",)
            ).fetchone()
        user_id = row["id"]
        add_sample_task_for_user(user_id, "Comprar leche")
        add_sample_task_for_user(user_id, "Preparar presentación")
        add_sample_task_for_user(user_id, "Aprender Flask")


# Ensure sample tasks are present on startup
with app.app_context():
    ensure_sample_tasks()


# ---------- Auth for /tareas ----------
@auth.verify_password
def verify_password(username, password):
    # Called by Flask-HTTPAuth when a protected endpoint is accessed
    if username and password and verify_user(username, password):
        # return user identity (we can return username)
        return username
    return None


# ---------- Routes ----------
@app.route("/registro", methods=["POST"])
def registro():
    """
    JSON body: {"usuario": "...", "contraseña": "..."}
    """
    if not request.is_json:
        return jsonify({"error": "Se requiere JSON"}), 400
    data = request.get_json()
    usuario = data.get("usuario") or data.get("username")
    contrasena = (
        data.get("contraseña") or data.get("contrasena") or data.get("password")
    )
    if not usuario or not contrasena:
        return jsonify({"error": "Faltan campos 'usuario' y/o 'contraseña'"}), 400

    created = create_user(usuario, contrasena)
    if not created:
        return jsonify({"error": "El usuario ya existe"}), 409
    return jsonify({"message": "Usuario creado correctamente", "usuario": usuario}), 201


@app.route("/login", methods=["POST"])
def login():
    """
    Verifica credenciales.
    Recibe JSON {"usuario": "...", "contraseña": "..."}
    Devuelve 200 si correcto, 401 si no.
    Nota: El endpoint /tareas está protegido con HTTP Basic Auth.
    """
    if not request.is_json:
        return jsonify({"error": "Se requiere JSON"}), 400
    data = request.get_json()
    usuario = data.get("usuario") or data.get("username")
    contrasena = (
        data.get("contraseña") or data.get("contrasena") or data.get("password")
    )
    if not usuario or not contrasena:
        return jsonify({"error": "Faltan campos 'usuario' y/o 'contraseña'"}), 400

    if verify_user(usuario, contrasena):
        return (
            jsonify(
                {
                    "message": "Credenciales correctas. Ahora puede acceder a /tareas usando HTTP Basic Auth."
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401


@app.route("/tareas", methods=["GET"])
@auth.login_required
def tareas():
    username = auth.current_user()
    # fetch tasks for this user
    user_row = get_user_by_username(username)
    db = get_db()
    cur = db.execute(
        "SELECT title, done FROM tasks WHERE user_id = ?", (user_row["id"],)
    )
    tasks = [{"title": r["title"], "done": bool(r["done"])} for r in cur.fetchall()]

    html = """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>Bienvenido</title>
      </head>
      <body>
        <h1>Bienvenido, {{username}}!</h1>
        <p>Estas son tus tareas:</p>
        <ul>
        {% for t in tasks %}
          <li>{{ t.title }} {% if t.done %}(completada){% endif %}</li>
        {% endfor %}
        </ul>
        <p>Nota: este endpoint está protegido con HTTP Basic Auth.</p>
      </body>
    </html>
    """
    return render_template_string(html, username=username, tasks=tasks)


# Root simple message
@app.route("/", methods=["GET"])
def index():
    return jsonify(
        {
            "message": "API REST con registro/login y endpoint /tareas (protegido por HTTP Basic Auth).",
            "endpoints": [
                "/registro (POST)",
                "/login (POST)",
                "/tareas (GET, Basic Auth)",
            ],
        }
    )


if __name__ == "__main__":
    # NO usar in production; para pruebas locales OK
    app.run(host="0.0.0.0", port=5000, debug=True)
