# Proyecto: API REST con Flask + SQLite (Registro, Login, Tareas protegidas)

## Objetivos

-   Implementar endpoints REST básicos.
-   Usar hashing de contraseñas.
-   Persistencia con SQLite.
-   Cliente de consola que interactúa con la API.

## Estructura de archivos

-   `servidor.py` -\> API Flask + SQLite
-   `cliente.py` -\> Cliente de consola
-   `requirements.txt`
-   `database.sqlite` (se crea automáticamente)
-   `README.md`

## Requisitos

-   Python 3.8+
-   pip

## Instalación (entorno local)

1.  Clona el repositorio:

    ``` bash
    git clone <tu-repo-url>
    cd <tu-repo-dir>
    ```

2.  Crea un entorno virtual (recomendado):

    ``` bash
    python -m venv venv
    source venv/bin/activate    # Linux/macOS
    venv\Scripts\activate       # Windows
    ```

3.  Instala dependencias:

    ``` bash
    pip install -r requirements.txt
    ```

## Ejecución del servidor

``` bash
python servidor.py
```

por defecto escucha `http://0.0.0.0:5000`.

## Probar la API (ejemplos)

### 1) Registro

``` bash
curl -X POST http://127.0.0.1:5000/registro   -H "Content-Type: application/json"   -d '{"usuario": "juan", "contraseña": "secreto"}'
```

### 2) Login (verifica credenciales)

``` bash
curl -X POST http://127.0.0.1:5000/login   -H "Content-Type: application/json"   -d '{"usuario": "juan", "contraseña": "secreto"}'
```

### 3) Obtener /tareas (requiere HTTP Basic Auth)

``` bash
curl -u juan:secreto http://127.0.0.1:5000/tareas
```

## Uso del cliente de consola

``` bash
python cliente.py
```

Sigue el menú para registrar, loguear y pedir `/tareas`.

## Capturas de Pantalla

1.  Ejecuta `python servidor.py` en una terminal.
2.  En otra terminal realiza el `curl` de registro y login (ver
    ejemplos).
3.  Toma capturas de:
    -   Respuesta de `curl /registro` (HTTP 201)
    -   Respuesta de `curl /login` (HTTP 200)
    -   Resultado de `curl -u usuario:pass /tareas` (HTML) Guarda las
        imágenes en `screenshots/` y súbelas al repo.

## Despliegue / Notas sobre GitHub Pages

-   **GitHub Pages** solo sirve para sitios estáticos (docs, README) ---
    no puede ejecutar el servidor Flask.\
-   Para publicar la API en la web, deploy posible en: Railway, Render,
    Fly.io, Heroku (si está disponible), etc.
-   Puedes usar GitHub Pages para alojar este README y la documentación
    del proyecto.

## Respuestas conceptuales

### ¿Por qué hashear contraseñas?

-   **Seguridad**: si la base de datos se filtra, los atacantes no
    obtienen contraseñas en texto plano.
-   **Irreversibilidad**: hashes seguros (bcrypt) no permiten recuperar
    la contraseña original.
-   **Protección contra ataques**: algoritmos como bcrypt son lentos y
    con sal (salt) incorporada, dificultando ataques por fuerza bruta y
    tablas rainbow.

### Ventajas de usar SQLite aquí

-   **Simplicidad**: sin servidor de base de datos aparte; ideal para
    prácticas y prototipos.
-   **Portabilidad**: la BD es un único archivo (`database.sqlite`)
    fácil de versionar (con cuidado).
-   **Bajo mantenimiento**: no requiere administración ni procesos
    adicionales.
-   **Suficiente** para aplicaciones pequeñas o pruebas locales (o
    demos).

## Buenas prácticas / mejoras posibles

-   Usar HTTPS (especialmente si usas Basic Auth).
-   Implementar tokens (JWT) para sesiones en aplicaciones más
    complejas.
-   Añadir rate-limiting y protección contra fuerza bruta.
-   Validaciones más completas y manejo de errores más detallado.
