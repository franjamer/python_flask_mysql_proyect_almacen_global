from flask import Blueprint, render_template, request, redirect, url_for, session
import database as db

situacion_bp = Blueprint('situacion_bp', __name__)

@situacion_bp.route('/situacion', methods=['GET'])
def situacion():
    puede_editar = session.get('rol') == 'admin'
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT almacen FROM situacion_tabla ORDER BY almacen")
    almacenes = cursor.fetchall()
    cursor.execute("SELECT * FROM situacion_tabla ORDER BY estanteria, columna, altura")
    posiciones = cursor.fetchall()
    # Consulta de repuestos para el select
    cursor.execute("SHOW TABLES LIKE 'inventario'")
    if cursor.fetchone():
        cursor.execute("SELECT referencia, nombre FROM inventario ORDER BY referencia")
        repuestos = cursor.fetchall()
    else:
        repuestos = []
    cursor.close()
    conn.close()
    return render_template(
        'situación.html',
        almacenes=almacenes,
        posiciones=posiciones,
        puede_editar=puede_editar,
        repuestos=repuestos
    )

@situacion_bp.route('/situacion/añadir', methods=['POST'])
def añadir():
    if session.get('rol') != 'admin':
        return redirect(url_for('situacion_bp.situacion'))
    referencia_repuesto = request.form.get('referencia_repuesto') or None
    datos = (
        request.form['almacen'],
        request.form['estanteria'],
        request.form['altura'],
        request.form['columna'],
        request.form['lado'],
        request.form['linea_produccion'],
        referencia_repuesto
    )
    conn = db.get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO situacion_tabla
        (almacen, estanteria, altura, columna, lado, linea_produccion, referencia_repuesto)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('situacion_bp.situacion'))

@situacion_bp.route('/situacion/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('situacion_bp.situacion'))
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM situacion_tabla WHERE id_situacion_tabla = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('situacion_bp.situacion'))

@situacion_bp.route('/situacion/crear_ajax', methods=['POST'])
def crear_situacion_ajax():
    data = request.json
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """INSERT INTO situacion_tabla
        (almacen, estanteria, altura, columna, lado, linea_produccion)
        VALUES (%s, %s, %s, %s, %s, %s)"""
    valores = (
        data.get('almacen'),
        data.get('estanteria'),
        data.get('altura'),
        data.get('columna'),
        data.get('lado'),
        data.get('linea_produccion')
    )
    cursor.execute(sql, valores)
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM situacion_tabla WHERE id_situacion_tabla = %s", (new_id,))
    nueva = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(nueva)