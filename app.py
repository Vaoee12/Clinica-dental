from flask import Flask, jsonify
from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS


app = Flask(__name__)
# Conectense a esta API compadres 
CORS(app) 

# Credenciales de tu Docker
DB_HOST = "localhost"
DB_NAME = "clinicadental"
DB_USER = "admin"
DB_PASS = "admin123"
DB_PORT = "5432"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

# Endpoint de prueba para ver si el servidor está vivo
@app.route('/', methods=['GET'])
def index():
    return jsonify({"mensaje": "¡API del Sistema SGO jalando al 100!"})

# Tu endpoint del CRUD
@app.route('/sucursales', methods=['GET'])
def obtener_sucursales():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consultamos la tabla SUCURSAL
        cursor.execute('SELECT ID_SUCURSAL, NOMBRE_S, CALLE, NUMERO, CIUDAD FROM SUCURSAL;')
        sucursales = cursor.fetchall()
        
        # Formateamos a JSON
        lista_sucursales = []
        for sucursal in sucursales:
            lista_sucursales.append({
                "id_sucursal": sucursal[0],
                "nombre_s": sucursal[1],
                "calle": sucursal[2],
                "numero": sucursal[3],
                "ciudad": sucursal[4]
            })
            
        cursor.close()
        conn.close()
        return jsonify(lista_sucursales), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para CREAR una nueva sucursal (POST)
@app.route('/sucursales', methods=['POST'])
def crear_sucursal():
    try:
        # Obtenemos los datos en formato JSON que nos mandará el Frontend
        datos = request.json
        
        id_sucursal = datos.get('id_sucursal')
        nombre_s = datos.get('nombre_s')
        calle = datos.get('calle')
        numero = datos.get('numero')
        ciudad = datos.get('ciudad')
        
        # Validación súper básica para que no nos manden datos vacíos
        if not all([id_sucursal, nombre_s, calle, numero, ciudad]):
            return jsonify({"error": "Faltan datos requeridos (id_sucursal, nombre_s, calle, numero, ciudad)"}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Armamos el query de inserción de SQL
        query = """
            INSERT INTO SUCURSAL (ID_SUCURSAL, NOMBRE_S, CALLE, NUMERO, CIUDAD) 
            VALUES (%s, %s, %s, %s, %s);
        """
        # Ejecutamos el query pasando los valores de forma segura
        cursor.execute(query, (id_sucursal, nombre_s, calle, numero, ciudad))
        
        # IMPORTANTE: Confirmamos los cambios en la base de datos
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Sucursal creada exitosamente!"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para ACTUALIZAR una sucursal (PUT)
@app.route('/sucursales/<int:id_sucursal>', methods=['PUT'])
def actualizar_sucursal(id_sucursal):
    try:
        datos = request.json
        nombre_s = datos.get('nombre_s')
        calle = datos.get('calle')
        numero = datos.get('numero')
        ciudad = datos.get('ciudad')
        
        if not all([nombre_s, calle, numero, ciudad]):
            return jsonify({"error": "Faltan datos para actualizar"}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # El query UPDATE de SQL
        query = """
            UPDATE SUCURSAL 
            SET NOMBRE_S = %s, CALLE = %s, NUMERO = %s, CIUDAD = %s
            WHERE ID_SUCURSAL = %s;
        """
        cursor.execute(query, (nombre_s, calle, numero, ciudad, id_sucursal))
        
        # Validamos si realmente se actualizó algo (por si pasan un ID que no existe)
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Sucursal no encontrada"}), 404
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Sucursal actualizada con éxito!"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint para ELIMINAR una sucursal (DELETE)
@app.route('/sucursales/<int:id_sucursal>', methods=['DELETE'])
def eliminar_sucursal(id_sucursal):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM SUCURSAL WHERE ID_SUCURSAL = %s;"
        cursor.execute(query, (id_sucursal,))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Sucursal no encontrada"}), 404
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Sucursal eliminada, mi rey!"}), 200
        
    except Exception as e:
        return jsonify({
            "error": "No se pudo eliminar. ¿Tiene consultorios asignados?", 
            "detalle": str(e)
        }), 500

# ==========================================
# CRUD DE PACIENTES
# ==========================================

# Endpoint para CREAR un paciente (POST) usando Procedimiento Almacenado
@app.route('/pacientes', methods=['POST'])
def crear_paciente():
    try:
        datos = request.json
        
        # Extraemos los datos que necesita el procedimiento almacenado
        num_a = datos.get('num_a')
        tipoafiliado = datos.get('tipoafiliado')
        costo_m = datos.get('costo_m')
        
        id_cedula = datos.get('id_cedula')
        nomp = datos.get('nomp')
        app = datos.get('app')
        amp = datos.get('amp') # Apellido materno 
        monto_mensual = datos.get('monto_mensual')
        
        telefono = datos.get('telefono')
        
        # Validación básica para que no falten los datos clave
        if not all([num_a, tipoafiliado, costo_m, id_cedula, nomp, app, monto_mensual, telefono]):
            return jsonify({"error": "Faltan datos requeridos para registrar al paciente y su afiliación"}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Llamamos al procedimiento almacenado de PostgreSQL usando CALL
        query = "CALL registrar_paciente(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(query, (
            num_a, tipoafiliado, costo_m, 
            id_cedula, nomp, app, amp, monto_mensual, 
            telefono
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Paciente, afiliación y teléfono registrados con éxito en un solo movimiento!"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para OBTENER todos los pacientes (GET)
@app.route('/pacientes', methods=['GET'])
def obtener_pacientes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consultamos la tabla PACIENTE
        cursor.execute('SELECT ID_CEDULA, NOMP, APP, AMP, MONTO_MENSUAL, NUM_A FROM PACIENTE;')
        pacientes = cursor.fetchall()
        
        lista_pacientes = []
        for pac in pacientes:
            lista_pacientes.append({
                "id_cedula": pac[0],
                "nomp": pac[1],
                "app": pac[2],
                "amp": pac[3],
                "monto_mensual": float(pac[4]), # Lo pasamos a float porque en BD es NUMERIC
                "num_a": pac[5]
            })
            
        cursor.close()
        conn.close()
        return jsonify(lista_pacientes), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint para ACTUALIZAR un paciente (PUT)
@app.route('/pacientes/<int:id_cedula>', methods=['PUT'])
def actualizar_paciente(id_cedula):
    try:
        datos = request.json
        nomp = datos.get('nomp')
        app = datos.get('app')
        amp = datos.get('amp')
        monto_mensual = datos.get('monto_mensual')
        
        if not all([nomp, app, monto_mensual]):
            return jsonify({"error": "Faltan datos básicos (nombre, apellido paterno, monto) para actualizar"}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE PACIENTE 
            SET NOMP = %s, APP = %s, AMP = %s, MONTO_MENSUAL = %s
            WHERE ID_CEDULA = %s;
        """
        cursor.execute(query, (nomp, app, amp, monto_mensual, id_cedula))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Paciente no encontrado"}), 404
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Paciente actualizado con éxito!"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint para ELIMINAR un paciente (DELETE)
@app.route('/pacientes/<int:id_cedula>', methods=['DELETE'])
def eliminar_paciente(id_cedula):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Como la tabla TELEFONO_P depende del paciente, tenemos que borrar su teléfono primero
        cursor.execute("DELETE FROM TELEFONO_P WHERE ID_CEDULA = %s;", (id_cedula,))
        
        # Ahora sí borramos al paciente
        cursor.execute("DELETE FROM PACIENTE WHERE ID_CEDULA = %s;", (id_cedula,))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Paciente no encontrado"}), 404
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Paciente eliminado del sistema!"}), 200
        
    except Exception as e:
        return jsonify({
            "error": "No se pudo eliminar. ¿Este paciente ya tiene consultas registradas?", 
            "detalle": str(e)
        }), 500

# ==========================================
# CRUD DE ODONTÓLOGOS
# ==========================================

# Endpoint para OBTENER todos los odontólogos (GET)
@app.route('/odontologos', methods=['GET'])
def obtener_odontologos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT CEDULA, HORARIO_CON, HORARIO_SUC, ESPECIALIDAD, NOMO, APO, AMO, NUM_COS, ID_SUCURSAL FROM ODONTOLOGO;')
        odontologos = cursor.fetchall()
        
        lista_odontologos = []
        for odon in odontologos:
            lista_odontologos.append({
                "cedula": odon[0],
                "horario_con": str(odon[1]), # Convertimos la fecha a texto para que el JSON no truene
                "horario_suc": str(odon[2]),
                "especialidad": odon[3],
                "nomo": odon[4],
                "apo": odon[5],
                "amo": odon[6],
                "num_cos": odon[7],
                "id_sucursal": odon[8]
            })
            
        cursor.close()
        conn.close()
        return jsonify(lista_odontologos), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint para CREAR un odontólogo (POST)
@app.route('/odontologos', methods=['POST'])
def crear_odontologo():
    try:
        datos = request.json
        
        cedula = datos.get('cedula')
        horario_con = datos.get('horario_con')
        horario_suc = datos.get('horario_suc')
        especialidad = datos.get('especialidad')
        nomo = datos.get('nomo')
        apo = datos.get('apo')
        amo = datos.get('amo') # El apellido materno es opcional
        num_cos = datos.get('num_cos')
        id_sucursal = datos.get('id_sucursal')
        
        # Validamos que vengan los datos obligatorios
        if not all([cedula, horario_con, horario_suc, especialidad, nomo, apo, num_cos, id_sucursal]):
            return jsonify({"error": "Faltan datos requeridos. Revisa que no falte la cédula, horarios, especialidad, nombre, apellido o ubicación."}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO ODONTOLOGO (CEDULA, HORARIO_CON, HORARIO_SUC, ESPECIALIDAD, NOMO, APO, AMO, NUM_COS, ID_SUCURSAL)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (cedula, horario_con, horario_suc, especialidad, nomo, apo, amo, num_cos, id_sucursal))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Odontólogo registrado con éxito!"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint para ACTUALIZAR un odontólogo (PUT)
@app.route('/odontologos/<int:cedula>', methods=['PUT'])
def actualizar_odontologo(cedula):
    try:
        datos = request.json
        
        horario_con = datos.get('horario_con')
        horario_suc = datos.get('horario_suc')
        especialidad = datos.get('especialidad')
        nomo = datos.get('nomo')
        apo = datos.get('apo')
        amo = datos.get('amo')
        num_cos = datos.get('num_cos')
        id_sucursal = datos.get('id_sucursal')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE ODONTOLOGO 
            SET HORARIO_CON = %s, HORARIO_SUC = %s, ESPECIALIDAD = %s, NOMO = %s, APO = %s, AMO = %s, NUM_COS = %s, ID_SUCURSAL = %s
            WHERE CEDULA = %s;
        """
        cursor.execute(query, (horario_con, horario_suc, especialidad, nomo, apo, amo, num_cos, id_sucursal, cedula))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Odontólogo no encontrado"}), 404
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Datos del odontólogo actualizados!"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint para ELIMINAR un odontólogo (DELETE)
@app.route('/odontologos/<int:cedula>', methods=['DELETE'])
def eliminar_odontologo(cedula):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM ODONTOLOGO WHERE CEDULA = %s;", (cedula,))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Odontólogo no encontrado"}), 404
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Odontólogo dado de baja!"}), 200
        
    except Exception as e:
        return jsonify({
            "error": "No se pudo eliminar. Verifica si el odontólogo ya realizó tratamientos o tiene historial.", 
            "detalle": str(e)
        }), 500

# ==========================================
# CRUD DE CONSULTORIOS
# ==========================================

# Endpoint para OBTENER todos los consultorios (GET)
@app.route('/consultorios', methods=['GET'])
def obtener_consultorios():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT NUM_COS, ID_SUCURSAL FROM CONSULTORIO;')
        consultorios = cursor.fetchall()
        
        lista_consultorios = []
        for cons in consultorios:
            lista_consultorios.append({
                "num_cos": cons[0],
                "id_sucursal": cons[1]
            })
            
        cursor.close()
        conn.close()
        return jsonify(lista_consultorios), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint para CREAR un consultorio (POST)
@app.route('/consultorios', methods=['POST'])
def crear_consultorio():
    try:
        datos = request.json
        num_cos = datos.get('num_cos')
        id_sucursal = datos.get('id_sucursal')
        
        if not num_cos or not id_sucursal:
            return jsonify({"error": "Faltan datos. Se requiere num_cos e id_sucursal"}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "INSERT INTO CONSULTORIO (NUM_COS, ID_SUCURSAL) VALUES (%s, %s);"
        cursor.execute(query, (num_cos, id_sucursal))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Consultorio creado con éxito!"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint para ELIMINAR un consultorio (DELETE)
# Como la llave primaria es compuesta, pedimos ambos IDs en la URL
@app.route('/consultorios/<int:id_sucursal>/<int:num_cos>', methods=['DELETE'])
def eliminar_consultorio(id_sucursal, num_cos):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM CONSULTORIO WHERE ID_SUCURSAL = %s AND NUM_COS = %s;"
        cursor.execute(query, (id_sucursal, num_cos))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Consultorio no encontrado en esa sucursal"}), 404
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Consultorio eliminado correctamente!"}), 200
        
    except Exception as e:
        return jsonify({
            "error": "No se pudo eliminar. Revisa si hay odontólogos u operaciones asignadas a este consultorio.", 
            "detalle": str(e)
        }), 500


if __name__ == '__main__':
    # Arranca el servidor en el puerto 5000
    app.run(debug=True, port=5000)