"""
cliente.py
Cliente de consola para interactuar con la API.
Permite:
- registrar usuario
- loguear (verifica credenciales)
- obtener /tareas usando HTTP Basic Auth
"""

import requests
from getpass import getpass
from requests.auth import HTTPBasicAuth

BASE = "http://127.0.0.1:5000"

def registrar():
    usuario = input("Usuario a registrar: ").strip()
    contrasena = getpass("Contraseña: ")
    r = requests.post(f"{BASE}/registro", json={"usuario": usuario, "contraseña": contrasena})
    print(r.status_code, r.json())

def login():
    usuario = input("Usuario: ").strip()
    contrasena = getpass("Contraseña: ")
    r = requests.post(f"{BASE}/login", json={"usuario": usuario, "contraseña": contrasena})
    print(r.status_code, r.json())
    return usuario, contrasena, r.status_code == 200

def ver_tareas(usuario, contrasena):
    r = requests.get(f"{BASE}/tareas", auth=HTTPBasicAuth(usuario, contrasena))
    if r.status_code == 200:
        print("Contenido HTML de /tareas:\n")
        print(r.text)
    else:
        print("Error al obtener tareas:", r.status_code, r.text)

def menu():
    while True:
        print("\nOpciones:\n1) Registrar\n2) Login\n3) Obtener /tareas (usa Basic Auth)\n4) Salir")
        opt = input("Elegí: ").strip()
        if opt == "1":
            registrar()
        elif opt == "2":
            usuario, contrasena, ok = login()
        elif opt == "3":
            usuario = input("Usuario para Basic Auth: ").strip()
            contrasena = getpass("Contraseña: ")
            ver_tareas(usuario, contrasena)
        elif opt == "4":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
