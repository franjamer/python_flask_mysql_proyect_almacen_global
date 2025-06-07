from flask import Blueprint, request, redirect, url_for
import database as db

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/usuarios', methods=['POST'])
def addUser():
    username = request.form['username']
    password = request.form['password']
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))
    if username and password:
        conn = db.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (codigo_operador, password) VALUES  (%s, %s)"
        users = (username, password)
        cursor.execute(sql, users)
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('home_bp.usuarios'))

@users_bp.route('/usuarios/<int:id>', methods=['POST'])
def delete(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))
    conn = db.get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM usuarios WHERE idusuario= %s"
    users = (id,)
    cursor.execute(sql, users)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home_bp.usuarios'))

@users_bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    password = request.form['password']
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))
    conn = db.get_connection()
    cursor = conn.cursor()
    sql = "UPDATE usuarios SET codigo_operador = %s, password = %s WHERE idusuario = %s"
    cursor.execute(sql, (username, password, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home_bp.usuarios'))