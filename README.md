# Clinica-dental
Clinica dental x docker
PASOS para subirlo a docker
1. Descargar docker destop y abrirlo.
2. Descargar el archivo .yml y la carpeta db
3. Guardarlos en una misma carpeta
4. Abrir la dirección de la carpeta en la terminal
5. Usar el comando docker compose up -d
6. Usar el comando docker logs clinica_postgres deberá aparecer algo como "database system is ready to accept connections"
7. Listo :))


# Documentación Oficial de la API REST v1.0 (SGO)

Este documento contiene la especificación completa de los endpoints desarrollados para la capa de lógica de negocio y persistencia de datos del sistema distribuido **SGO**.

### Información General
- **Base URL:** `http://localhost:5000`
- **Formato de datos:** `application/json`
- **Arquitectura:** Microservicios contenerizados mediante Docker y Flask.

### Integrantes del Proyecto (Backend)
- Tapia Ledesma Angel Hazel (Líder de Backend)
- Dominguez Zavala Valentina
- Salinas Ángel Laura Itzel
- Castillo Bautista Samantha Lucia
- Galindo Granados Abner Alejandro

---

## 1. Módulo de Autenticación Básica

### `POST /login`
Simula el inicio de sesión del administrador del sistema.
- **Cuerpo de la Petición (JSON):**
  ```json
  {
    "usuario": "admin",
    "password": "admin123"
  }

```

* **Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "¡Login exitoso!",
  "rol": "Administrador",
  "token": "token-simulado-sgo-admin-999",
  "usuario": "admin"
}

```


* **Respuesta de Error (401 Unauthorized):**
```json
{
  "error": "Credenciales incorrectas. Acceso denegado."
}

```



---

## 2. CRUD de Sucursales

### `GET /sucursales`

Obtiene la lista completa de sucursales registradas.

* **Respuesta Exitosa (200 OK):**
```json
[
  {
    "id_sucursal": 1,
    "nombre_s": "Sucursal Norte",
    "calle": "Av. Reforma",
    "numero": 101,
    "ciudad": "CDMX"
  }
]

```



### `POST /sucursales`

Registra una nueva sucursal en el sistema.

* **Cuerpo de la Petición (JSON):**
```json
{
  "id_sucursal": 5,
  "nombre_s": "Sucursal Centro",
  "calle": "Madero",
  "numero": 55,
  "ciudad": "CDMX"
}

```


* **Respuesta Exitosa (201 Created):**
```json
{
  "mensaje": "¡Sucursal creada exitosamente!"
}

```



### `PUT /sucursales/<int:id_sucursal>`

Actualiza los datos de una sucursal existente. El ID viaja en la URL (ej. `/sucursales/5`).

* **Cuerpo de la Petición (JSON):**
```json
{
  "nombre_s": "Sucursal Centro Remodelada",
  "calle": "Francisco I. Madero",
  "numero": 100,
  "ciudad": "CDMX"
}

```


* **Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "¡Sucursal actualizada con éxito!"
}

```



### `DELETE /sucursales/<int:id_sucursal>`

Elimina una sucursal siempre y cuando no tenga consultorios vinculados. El ID viaja en la URL.

* **Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "¡Sucursal eliminada, mi rey!"
}

```



---

## 3. CRUD de Pacientes

### `GET /pacientes`

Obtiene la lista completa de pacientes con sus datos generales.

* **Respuesta Exitosa (200 OK):**
```json
[
  {
    "id_cedula": 20000001,
    "nomp": "Juan",
    "app": "Pérez",
    "amp": "López",
    "monto_mensual": 1200.0,
    "num_a": 200001
  }
]

```



### `POST /pacientes`

Registra de forma síncrona a un afiliado, su perfil de paciente y su teléfono móvil utilizando un procedimiento almacenado.

* **Cuerpo de la Petición (JSON):**
```json
{
  "num_a": 300001,
  "tipoafiliado": "INDIVIDUAL",
  "costo_m": 1500.00,
  "id_cedula": 88888888,
  "nomp": "Angel",
  "app": "Tapia",
  "amp": "Ledesma",
  "monto_mensual": 1500.00,
  "telefono": 5511223344
}

```


* **Respuesta Exitosa (201 Created):**
```json
{
  "mensaje": "¡Paciente, afiliación y teléfono registrados con éxito en un solo movimiento!"
}

```



### `PUT /pacientes/<int:id_cedula>`

Modifica la información personal del paciente.

* **Cuerpo de la Petición (JSON):**
```json
{
  "nomp": "Angel Hazel",
  "app": "Tapia",
  "amp": "Ledesma",
  "monto_mensual": 1650.00
}

```


* **Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "¡Paciente actualizado con éxito!"
}

```



### `DELETE /pacientes/<int:id_cedula>`

Elimina un paciente purgando primero sus referencias telefónicas dependientes.

* **Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "¡Paciente eliminado del sistema!"
}

```



---

## 4. CRUD de Odontólogos

### `GET /odontologos`

Lista todos los odontólogos con sus horarios establecidos.

* **Respuesta Exitosa (200 OK):**
```json
[
  {
    "cedula": 30000001,
    "nomo": "Carlos",
    "apo": "Lopez",
    "amo": "Martinez",
    "especialidad": "Ortodoncia",
    "horario_con": "2024-06-03 09:00:00",
    "horario_suc": "2024-06-03 14:00:00",
    "num_cos": 10,
    "id_sucursal": 1
  }
]

```



### `POST /odontologos`

Registra un nuevo odontólogo asignándole un consultorio y sucursal.

* **Cuerpo de la Petición (JSON):**
```json
{
  "cedula": 30000005,
  "horario_con": "2026-06-03 09:00:00",
  "horario_suc": "2026-06-03 15:00:00",
  "especialidad": "Endodoncia",
  "nomo": "Hugo",
  "apo": "Sánchez",
  "amo": "Márquez",
  "num_cos": 10,
  "id_sucursal": 1
}

```


* **Respuesta Exitosa (201 Created):**
```json
{
  "mensaje": "¡Odontólogo registrado con éxito!"
}

```



### `PUT /odontologos/<int:cedula>`

Actualiza los horarios, especialidad o asignación física del especialista.

* **Cuerpo de la Petición (JSON):**
```json
{
  "horario_con": "2026-06-03 10:00:00",
  "horario_suc": "2026-06-03 18:00:00",
  "especialidad": "Endodoncia",
  "nomo": "Hugo",
  "apo": "Sánchez",
  "amo": "Márquez",
  "num_cos": 20,
  "id_sucursal": 2
}

```


* **Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "¡Datos del odontólogo actualizados!"
}

```



### `DELETE /odontologos/<int:cedula>`

Remueve un especialista del personal clínico activo.

* **Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "¡Odontólogo dado de baja!"
}

```



---

## 5. CRUD de Consultorios

### `GET /consultorios`

Muestra el catálogo completo de consultorios.

* **Respuesta Exitosa (200 OK):**
```json
[
  {
    "num_cos": 10,
    "id_sucursal": 1
  }
]

```



### `POST /consultorios`

Registra una celda física de consultorio asignándola a una sucursal existente.

* **Cuerpo de la Petición (JSON):**
```json
{
  "num_cos": 50,
  "id_sucursal": 1
}

```


* **Respuesta Exitosa (201 Created):**
```json
{
  "mensaje": "¡Consultorio creado con éxito!"
}

```



### `DELETE /consultorios/<int:id_sucursal>/<int:num_cos>`

Elimina el consultorio por su llave compuesta. Ej. `/consultorios/1/50`. No admite actualización (`PUT`) por restricciones de diseño relacional.

* **Respuesta Exitosa (200 OK):**
```json
{
  "mensaje": "¡Consultorio eliminado correctamente!"
}

```



---

## 6. Reportes Financieros Distribuidos

### `GET /reportes/pagos-mensuales`

Consolida el flujo acumulado de ingresos recaudados mensualmente indexados por cada número de asociado.

* **Respuesta Exitosa (200 OK):**
```json
[
  {
    "numero_asociado": 200001,
    "anio": 2024,
    "mes": 6,
    "monto_total": 350.00
  }
]

```



### `GET /reportes/monto-mensual-sucursal`

Consolida los ingresos brutos mensuales segregados de manera conjunta por sucursal y tipo de tratamiento.

* **Respuesta Exitosa (200 OK):**
```json
[
  {
    "tratamiento": "LIMPI",
    "sucursal": "Sucursal Norte",
    "mes": 6,
    "anio": 2024,
    "monto_mensual": 850.00
  }
]

```

