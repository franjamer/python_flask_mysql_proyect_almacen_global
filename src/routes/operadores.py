from flask import Blueprint, request, redirect, url_for, session
import database as db

operadores_bp = Blueprint('operadores_bp', __name__)

@operadores_bp.route('/añadir', methods=['POST'])
def añadir():
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))

    codigo_operador = request.form.get('codigo_operador')
    nombre_completo = request.form.get('nombre_completo')
    puesto = request.form.get('puesto')

    if codigo_operador and nombre_completo and puesto:
        conn = db.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO operadores (codigo_operador, nombre_completo, puesto) VALUES (%s, %s, %s)"
        cursor.execute(sql, (codigo_operador, nombre_completo, puesto))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('home_bp.operadores'))

@operadores_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))

    conn = db.get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM operadores WHERE id_operador = %s"
    cursor.execute(sql, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home_bp.operadores'))

@operadores_bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))

    codigo_operador = request.form.get('codigo_operador')
    nombre_completo = request.form.get('nombre_completo')
    puesto = request.form.get('puesto')

    if codigo_operador and nombre_completo and puesto:
        conn = db.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE operadores SET codigo_operador = %s, nombre_completo = %s, puesto = %s WHERE id_operador = %s"
        cursor.execute(sql, (codigo_operador, nombre_completo, puesto, id))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('home_bp.operadores'))

