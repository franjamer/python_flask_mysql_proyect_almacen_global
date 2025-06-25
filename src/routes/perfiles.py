from flask import Blueprint, request, redirect, url_for, session
import database as db

perfiles_bp = Blueprint('perfiles_bp', __name__)


@perfiles_bp.route('/perfiles', methods=['POST'])
def añadir():
    perfil = request.form['perfil']
    password = request.form['password']
    rol = request.form['rol']
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))
    if perfil and password and rol:
        conn = db.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO perfiles (perfil, password,rol) VALUES  (%s, %s, %s)"
        perfiles = (perfil, password, rol)
        cursor.execute(sql, perfiles)
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('home_bp.perfiles'))


@perfiles_bp.route('/perfiles/<int:id>', methods=['POST'])
def delete(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))
    conn = db.get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM perfiles WHERE id_perfil= %s"
    perfiles = (id,)
    cursor.execute(sql, perfiles)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home_bp.perfiles'))


@perfiles_bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))

    perfil = request.form['perfil']
    password = request.form['password']
    rol = request.form['rol']
    if perfil and password and rol:
        conn = db.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE perfiles SET perfil = %s, password = %s, rol = %s WHERE id_perfil = %s"
        cursor.execute(sql, (perfil, password, rol, id))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('home_bp.perfiles'))
