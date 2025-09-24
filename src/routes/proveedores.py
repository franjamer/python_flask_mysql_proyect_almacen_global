from flask import Blueprint, render_template, session, redirect, url_for, flash, request
import database as db

proveedores_bp = Blueprint('proveedores_bp', __name__)

@proveedores_bp.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    if session.get('perfil') != 'Admin':
        flash('Acceso denegado: solo el perfil Admin puede acceder a proveedores.', 'error')
        return redirect(url_for('home_bp.menu'))

    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)

    # Alta de proveedor
    if request.method == 'POST':
        nombre = request.form['nombre_proveedor']
        contacto = request.form['persona_contacto_proveedor']
        telefono = request.form['telefono_proveedor']
        email = request.form['direccion_proveedor']
        ciudad = request.form['ciudad_proveedor']
        cursor.execute(
            "INSERT INTO proveedor_tabla (nombre, contacto, telefono, email, ciudad) VALUES (%s, %s, %s, %s, %s)",
            (nombre, contacto, telefono, email, ciudad)
        )
        conn.commit()
        flash('Proveedor añadido correctamente.', 'success')

    cursor.execute("SELECT * FROM proveedor_tabla ORDER BY id_proveedor ASC")
    proveedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', proveedores=proveedores)