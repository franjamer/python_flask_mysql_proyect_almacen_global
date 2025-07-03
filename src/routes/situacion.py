from flask import Blueprint, render_template, request, redirect, url_for, session
import database as db

situacion_bp = Blueprint('situacion_bp', __name__)

@situacion_bp.route('/situacion', methods=['GET', 'POST'])
def situacion():
    puede_editar = session.get('rol') == 'admin'
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT almacen FROM situacion_tabla ORDER BY almacen")
    almacenes = cursor.fetchall()
    cursor.execute("SELECT * FROM situacion_tabla ORDER BY estanteria, columna, altura")
    posiciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('situación.html', almacenes=almacenes, posiciones=posiciones, puede_editar=puede_editar)

# Añadir nueva posición
@situacion_bp.route('/situacion/añadir', methods=['POST'])
def añadir():
    if session.get('rol') != 'admin':
        return redirect(url_for('situacion_bp.situacion'))
    datos = (
        request.form['almacen'],
        request.form['estanteria'],
        request.form['altura'],
        request.form['columna'],
        request.form['lado'],
        request.form['linea_produccion'],
        request.form.get('referencia_repuesto', ''),
        request.form.get('descripcion', '')
    )
    conn = db.get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO situacion_tabla
        (almacen, estanteria, altura, columna, lado, linea_produccion, referencia_repuesto, descripcion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('situacion_bp.situacion'))

# Eliminar posición
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

# Editar posición (simple, sin modal)
@situacion_bp.route('/situacion/editar/<int:id>', methods=['POST'])
def editar(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('situacion_bp.situacion'))
    datos = (
        request.form['almacen'],
        request.form['estanteria'],
        request.form['altura'],
        request.form['columna'],
        request.form['lado'],
        request.form['linea_produccion'],
        request.form.get('referencia_repuesto', ''),
        request.form.get('descripcion', ''),
        id
    )
    conn = db.get_connection()
    cursor = conn.cursor()
    sql = """UPDATE situacion_tabla SET
        almacen=%s, estanteria=%s, altura=%s, columna=%s, lado=%s, linea_produccion=%s, referencia_repuesto=%s, descripcion=%s
        WHERE id_situacion_tabla=%s"""
    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('situacion_bp.situacion'))