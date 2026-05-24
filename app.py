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

if __name__ == '__main__':
    # Arranca el servidor en el puerto 5000
    app.run(debug=True, port=5000)