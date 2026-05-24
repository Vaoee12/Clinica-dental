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

---

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