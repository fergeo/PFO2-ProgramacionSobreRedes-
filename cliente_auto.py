# cliente_auto.py
# Cliente de consola que hace: registro -> login -> obtener /tareas y guarda HTML

import requests
from getpass import getpass
import os

BASE = "http://127.0.0.1:5000"


def registrar(session, usuario, contraseña):
    resp = session.post(
        f"{BASE}/registro", json={"usuario": usuario, "contraseña": contraseña}
    )
    print("Registro:", resp.status_code, resp.text)
    return resp


def login(session, usuario, contraseña):
    resp = session.post(
        f"{BASE}/login", json={"usuario": usuario, "contraseña": contraseña}
    )
    print("Login:", resp.status_code, resp.text)
    return resp


def obtener_tareas(session, out_file="tareas.html"):
    resp = session.get(f"{BASE}/tareas")
    print("GET /tareas:", resp.status_code)
    if resp.status_code == 200:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(resp.text)
        print("HTML guardado en", out_file)
    else:
        print("Respuesta:", resp.text)


if __name__ == "__main__":
    s = requests.Session()
    usuario = input("Usuario (ej: juan): ").strip()
    contraseña = getpass("Contraseña: ")
    # registrar (ignorar si ya existe)
    registrar(s, usuario, contraseña)
    # login
    login(s, usuario, contraseña)
    # obtener tareas (usa sesión)
    obtener_tareas(s)
    print("Fin.")
