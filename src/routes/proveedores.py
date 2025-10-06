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
        nombre = request.form['nombre_prov']
        email = request.form['email_prov']
        telefono = request.form['telefono_prov']
        contacto = request.form['contacto_prov']
        web = request.form['web_prov']
        cursor.execute(
            "INSERT INTO proveedores (nombre_prov, email_prov, telefono_prov, contacto_prov, web_prov) VALUES (%s, %s, %s, %s, %s)",
            (nombre, email, telefono, contacto, web)
        )
        conn.commit()
        flash('Proveedor añadido correctamente.', 'success')

    cursor.execute("SELECT * FROM proveedores ORDER BY id_prov ASC")
    proveedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', proveedores=proveedores)