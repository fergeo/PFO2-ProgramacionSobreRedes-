# 🧩 Proyecto API REST con Flask y SQLite

**Repositorio oficial:** [PFO2-ProgramacionSobreRedes-](https://github.com/PFO2-ProgramacionSobreRedes-)

---

## 📘 Descripción del Proyecto

Este proyecto implementa una **API REST** utilizando **Flask** y **SQLite**, que permite:

- Registrar usuarios.
- Iniciar sesión con autenticación mediante sesiones seguras.
- Visualizar tareas personalizadas por usuario autenticado.

Las contraseñas se almacenan de forma segura usando el algoritmo **PBKDF2-SHA256** de la librería **Passlib**.

---

## 🎯 Objetivos del Trabajo Práctico

1. Implementar una API REST con endpoints funcionales.
2. Utilizar autenticación básica con protección de contraseñas.
3. Gestionar datos persistentes mediante SQLite.
4. Construir un cliente (en consola o navegador) que interactúe con la API.

---

## ⚙️ Tecnologías Utilizadas

- 🐍 **Python 3.12+**
- 🔥 **Flask 3.1+**
- 🗄️ **SQLite3**
- 🔑 **Passlib (PBKDF2-SHA256)**
- 🧪 **cURL / Postman** para pruebas

---## 🚀 Instalación y Ejecución

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/PFO2-ProgramacionSobreRedes-.git
cd PFO2-ProgramacionSobreRedes-

2️⃣ Crear un entorno virtual (recomendado)

python -m venv venv
venv\Scripts\activate   # En Windows
source venv/bin/activate  # En Linux o Mac

3️⃣ Instalar dependencias

pip install flask passlib[bcrypt] requests

4️⃣ Ejecutar el servidor

python servidor.py

Luego abrir en el navegador:
👉 http://127.0.0.1:5000/
🔗 Endpoints Disponibles
🔹 POST /registro

Registra un nuevo usuario.

Ejemplo de entrada JSON:

{
  "usuario": "fernando",
  "contraseña": "1234"
}

Respuesta esperada:

{
  "mensaje": "Usuario registrado correctamente",
  "usuario": "fernando"
}

🔹 POST /login

Inicia sesión con un usuario registrado.

Entrada JSON:

{
  "usuario": "fernando",
  "contraseña": "1234"
}

Respuesta exitosa:

{"mensaje": "Login exitoso"}

Error (credenciales inválidas):

{"error": "Credenciales inválidas"}

🔹 GET /tareas

Muestra una página HTML con las tareas del usuario autenticado.

Ejemplo de salida:

<h1>Bienvenido, fernando!</h1>
<ul>
  <li>Aprender Flask</li>
  <li>Probar endpoints</li>
</ul>

🔹 POST /logout

Cierra la sesión actual.

Respuesta:

{"mensaje": "Logout exitoso"}

🧪 Cómo Probar la API
🔸 Desde el navegador

Abrir: http://127.0.0.1:5000/
🔸 Desde PowerShell (Windows)
1️⃣ Registrar usuario

curl.exe -X POST http://127.0.0.1:5000/registro -H "Content-Type: application/json" -d "{\"usuario\":\"fernando\",\"contraseña\":\"1234\"}"

2️⃣ Iniciar sesión (guardar cookie)

curl.exe -c cookies.txt -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "{\"usuario\":\"fernando\",\"contraseña\":\"1234\"}"

3️⃣ Ver tareas autenticado

curl.exe -b cookies.txt http://127.0.0.1:5000/tareas

⚠️ Posibles Errores y Soluciones
❌ ModuleNotFoundError: No module named 'flask'

Causa: Flask no está instalado.
✅ Solución:

pip install Flask

❌ Working outside of application context

Causa: Se llamó a init_db() fuera del contexto de la aplicación Flask.
✅ Solución:

with app.app_context():
    init_db()

❌ Error con bcrypt o passlib

Causa: Incompatibilidad entre versiones en Windows.
✅ Solución: Se reemplazó por pbkdf2_sha256, más estable y portable.
❌ Problemas con acentos o ñ en PowerShell

Causa: PowerShell no interpreta UTF-8 correctamente.
✅ Solución: Escapar comillas o reemplazar "contraseña" por "password".
❌ “Acceso denegado” en /tareas

Causa: Falta de sesión autenticada.
✅ Solución: Loguearse con curl o Postman (usa cookies automáticamente).
📂 Estructura del Proyecto

📦 PFO2-ProgramacionSobreRedes-
 ┣ 📜 servidor.py
 ┣ 📜 cliente.py
 ┣ 📜 README.md
 ┗ 📄 usuarios.db   # generado automáticamente al ejecutar el servidor

💡 Preguntas Conceptuales
🔒 ¿Por qué hashear contraseñas?

Guardar contraseñas en texto plano es un riesgo grave de seguridad.
El hashing genera una cadena irreversible que protege los datos incluso si la base de datos es comprometida.
💾 Ventajas de usar SQLite

    No requiere instalación ni configuración externa.

    Ideal para proyectos pequeños o educativos.

    Almacena los datos en un solo archivo .db.

    Permite realizar consultas SQL completas.

👨‍💻 Autor

Trabajo Práctico – PFO2 Programación sobre Redes
Desarrollado con Python 3.12, Flask 3.1 y SQLite3.

📦 Repositorio oficial: PFO2-ProgramacionSobreRedes-


Incluye documentación completa y solución de errores reales durante el desarrollo.



```
