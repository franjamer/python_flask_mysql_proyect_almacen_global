from flask import Blueprint, render_template, request, jsonify
import database as db

tablas_bp = Blueprint('tablas_bp', __name__)

@tablas_bp.route('/tablas', methods=['GET'])
def mostrar_tablas():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tablas = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    conn.close()
    return render_template('tablas.html', tablas=tablas)

@tablas_bp.route('/columnas_tabla', methods=['POST'])
def columnas_tabla():
    nombre_tabla = request.json.get('tabla')
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DESCRIBE {nombre_tabla}")
    columnas = [fila[0] for fila in cursor.fetchall()]
    cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT 20")
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({
        "columnas": columnas,
        "filas": filas
    })