from flask import Blueprint, render_template, request, redirect, url_for, session
import database as db
from .vistas_config import VISTAS
from routes.configuracion_estilos import cargar_estilos_por_vista

perfiles_bp = Blueprint('perfiles_bp', __name__)

@perfiles_bp.route('/perfiles', methods=['GET'])
def mostrar_perfiles():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM perfiles")
    perfiles = cursor.fetchall()
    cursor.close()
    conn.close()
    columnas = VISTAS['perfiles']['columnas']
    nombres_columnas = VISTAS['perfiles']['nombres_columnas']
    vista='perfiles'
    estilos_por_vista = cargar_estilos_por_vista()
    return render_template(
        'perfiles.html',
        perfiles=perfiles,
        columnas=columnas,
        nombres_columnas=nombres_columnas,
        vista=vista,
        estilos_por_vista=estilos_por_vista
    )

@perfiles_bp.route('/perfiles', methods=['POST'])
def añadir():
    perfil = request.form['perfil']
    password = request.form['password']
    descripcion = request.form['descripcion']
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))
    if perfil and password and descripcion:
        conn = db.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO perfiles (perfil, password, descripcion) VALUES  (%s, %s, %s)"
        perfiles = (perfil, password, descripcion)
        cursor.execute(sql, perfiles)
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('perfiles_bp.mostrar_perfiles'))

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
    return redirect(url_for('perfiles_bp.mostrar_perfiles'))

@perfiles_bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    if session.get('rol') != 'admin':
        return redirect(url_for('home_bp.menu'))

    perfil = request.form['perfil']
    password = request.form['password']
    descripcion = request.form['descripcion']
    if perfil and password and descripcion:
        conn = db.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE perfiles SET perfil = %s, password = %s, descripcion = %s WHERE id_perfil = %s"
        cursor.execute(sql, (perfil, password, descripcion, id))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('perfiles_bp.mostrar_perfiles'))