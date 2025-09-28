# servidor.py
# API Flask + SQLite (compatible Flask 3.1+ con contexto correcto)

from flask import Flask, request, g, jsonify, session, render_template_string
import sqlite3
import os
from passlib.hash import pbkdf2_sha256

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "usuarios.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "clave_para_dev")

# --- DB helpers ---
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña_hash TEXT NOT NULL
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            titulo TEXT NOT NULL
        );
        """
    )
    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# --- Utilidades ---
def crear_usuario(usuario, contraseña):
    if not usuario or not contraseña:
        return False, "Faltan campos 'usuario' o 'contraseña'."
    if len(usuario.strip()) == 0:
        return False, "Usuario vacío no permitido."
    contraseña_hash = pbkdf2_sha256.hash(contraseña)
    db = get_db()
    try:
        db.execute(
            "INSERT INTO usuarios (usuario, contraseña_hash) VALUES (?, ?)",
            (usuario, contraseña_hash),
        )
        db.execute("INSERT INTO tareas (usuario, titulo) VALUES (?, ?)", (usuario, "Aprender Flask"))
        db.execute("INSERT INTO tareas (usuario, titulo) VALUES (?, ?)", (usuario, "Probar endpoints"))
        db.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "El usuario ya existe."

def verificar_credenciales(usuario, contraseña):
    db = get_db()
    cur = db.execute("SELECT contraseña_hash FROM usuarios WHERE usuario = ?", (usuario,))
    row = cur.fetchone()
    if row is None:
        return False
    return pbkdf2_sha256.verify(contraseña, row["contraseña_hash"])

# --- Rutas ---
@app.before_request
def ensure_db():
    if not hasattr(g, "_db_initialized"):
        init_db()
        g._db_initialized = True

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "mensaje": "API Flask activa. Endpoints: POST /registro, POST /login, GET /tareas"
    })

@app.route("/registro", methods=["POST"])
def registro():
    if not request.is_json:
        return jsonify({"error": "Se debe enviar JSON con 'usuario' y 'contraseña'."}), 400
    data = request.get_json()
    usuario = data.get("usuario")
    contraseña = data.get("contraseña")
    ok, err = crear_usuario(usuario, contraseña)
    if not ok:
        return jsonify({"error": err}), 400
    return jsonify({"mensaje": "Usuario registrado correctamente", "usuario": usuario}), 201

@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "Se debe enviar JSON con 'usuario' y 'contraseña'."}), 400
    data = request.get_json()
    usuario = data.get("usuario")
    contraseña = data.get("contraseña")
    if not usuario or not contraseña:
        return jsonify({"error": "Faltan campos 'usuario' o 'contraseña'."}), 400
    if verificar_credenciales(usuario, contraseña):
        session.clear()
        session["usuario"] = usuario
        return jsonify({"mensaje": "Login exitoso"}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@app.route("/tareas", methods=["GET"])
def tareas():
    usuario = session.get("usuario")
    if not usuario:
        return render_template_string(
            """
            <!doctype html>
            <html><head><meta charset='utf-8'><title>Acceso denegado</title></head>
            <body><h1>Acceso denegado</h1><p>No estás autenticado. Haz POST /login con tus credenciales.</p></body></html>
            """
        ), 401
    db = get_db()
    cur = db.execute("SELECT titulo FROM tareas WHERE usuario = ?", (usuario,))
    tareas = [r["titulo"] for r in cur.fetchall()]
    return render_template_string(
        """
        <!doctype html>
        <html><head><meta charset='utf-8'><title>Tareas</title></head>
        <body>
          <h1>Bienvenido, {{usuario}}!</h1>
          <p>Tus tareas:</p>
          <ul>{% for t in tareas %}<li>{{t}}</li>{% endfor %}</ul>
        </body></html>
        """ ,
        usuario=usuario,
        tareas=tareas,
    )

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensaje": "Logout exitoso"}), 200

# --- Inicio del servidor con contexto correcto ---
if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
