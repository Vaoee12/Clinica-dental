
Frontend estático para el Sistema Web de Gestión y Control Odontológico (SGO), desarrollado con:

- HTML
- CSS
- JavaScript
- Bootstrap
- Fetch API

## Cómo ejecutarlo

1. Levantar PostgreSQL con Docker Compose:

```bash
docker compose up -d
```

2. Ejecutar el backend Flask:

```bash
python app.py
```

3. Abrir el archivo:

```text
frontend/index.html
```

También se puede abrir con la extensión Live Server de VS Code.

## Conexión con la API

El archivo `js/api.js` usa:

```js
const API_URL = "http://localhost:5000";
```

Cambiarlo solo si Flask corre en otro puerto.

## Endpoints que sí usa

- GET /
- POST /login
- GET /pacientes
- POST /pacientes
- DELETE /pacientes/:id_cedula
- GET /sucursales
- POST /sucursales
- DELETE /sucursales/:id_sucursal
- GET /odontologos
- POST /odontologos
- DELETE /odontologos/:cedula
- GET /consultorios
- POST /consultorios
- DELETE /consultorios/:id_sucursal/:num_cos

