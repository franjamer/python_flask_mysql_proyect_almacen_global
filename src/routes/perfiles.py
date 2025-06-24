from flask import Blueprint, request, redirect, url_for
import database as db

perfiles_bp = Blueprint('perfiles_bp', __name__)


@perfiles_bp.route('/perfiles', methods=['POST'])
def añadir():
    username = request.form['username']
    password = request.form['password']
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))
    if username and password:
        conn = db.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO perfiles (perfil, password) VALUES  (%s, %s)"
        perfiles = (username, password)
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
    sql = "DELETE FROM perfiles WHERE idperfil= %s"
    perfiles = (id,)
    cursor.execute(sql, perfiles)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home_bp.perfiles'))


@perfiles_bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    password = request.form['password']
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))
    conn = db.get_connection()
    cursor = conn.cursor()
    sql = "UPDATE perfiles SET perfil = %s, password = %s WHERE idperfil = %s"
    cursor.execute(sql, (username, password, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home_bp.perfiles'))
