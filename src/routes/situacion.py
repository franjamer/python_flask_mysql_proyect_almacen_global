from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import database as db
from routes.configuracion import cargar_configuracion
from .vistas_config import VISTAS  # <-- Añade esto

situacion_bp = Blueprint('situacion_bp', __name__)

def puede_crear_actualizar():
    return session.get('rol') in ['admin']

def puede_eliminar():
    return session.get('rol') == 'admin'

@situacion_bp.route('/situacion', methods=['GET', 'POST'])
def situacion():
    mensaje_error = None
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST' and puede_crear_actualizar():
        almacen = request.form.get('almacen', '').strip()
        estanteria = request.form.get('estanteria', '').strip()
        lado = request.form.get('lado', '').strip()
        columna = request.form.get('columna', '').strip()
        altura = request.form.get('altura', '').strip()

        if not all([almacen, estanteria, lado, columna, altura]):
            mensaje_error = "Todos los campos son obligatorios."
        else:
            try:
                cursor.execute(
                    "INSERT INTO situacion_tabla (almacen, estanteria, lado, columna, altura) VALUES (%s, %s, %s, %s, %s)",
                    (almacen, estanteria, lado, columna, altura)
                )
                conn.commit()
            except Exception as e:
                mensaje_error = "Error al añadir la situación: " + str(e)

            if not mensaje_error:
                cursor.close()
                conn.close()
                return redirect(url_for('situacion_bp.situacion'))

    cursor.execute("SELECT DISTINCT almacen FROM situacion_tabla ORDER BY almacen")
    almacenes = cursor.fetchall()

    cursor.execute("SELECT * FROM situacion_tabla ORDER BY almacen, estanteria, columna, altura")
    posiciones = cursor.fetchall()

    cursor.close()
    conn.close()

    # Cargar configuración personalizada
    config = cargar_configuracion()
    columnas = VISTAS['situacion']['columnas']
    nombres_columnas = VISTAS['situacion']['nombres_columnas']

    return render_template(
        'situacion.html',
        almacenes=almacenes,
        posiciones=posiciones,
        mensaje_error=mensaje_error,
        puede_crear_actualizar=puede_crear_actualizar,
        puede_eliminar=puede_eliminar,
        columnas=columnas,
        nombres_columnas=nombres_columnas,
        config=config
    )

@situacion_bp.route('/situacion/eliminar/<id_situacion_tabla>', methods=['POST'])
def eliminar_situacion(id_situacion_tabla):
    if not puede_eliminar():
        return redirect(url_for('situacion_bp.situacion'))

    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM situacion_tabla WHERE id_situacion_tabla=%s", (id_situacion_tabla,))
        conn.commit()
    except Exception as e:
        flash(f"Error al eliminar la situación: {e}", 'error')

    cursor.close()
    conn.close()
    return redirect(url_for('situacion_bp.situacion'))

@situacion_bp.route('/nueva_situacion', methods=['POST'])
def nueva_situacion():
    if not puede_crear_actualizar():
        return redirect(url_for('inventario_bp.inventario'))

    conn = db.get_connection()
    cursor = conn.cursor()

    almacen = request.form.get('almacen', '').strip()
    estanteria = request.form.get('estanteria', '').strip()
    lado = request.form.get('lado', '').strip()
    columna = request.form.get('columna', '').strip()
    altura = request.form.get('altura', '').strip()

    try:
        cursor.execute(
            "INSERT INTO situacion_tabla (almacen, estanteria, lado, columna, altura) VALUES (%s, %s, %s, %s, %s)",
            (almacen, estanteria, lado, columna, altura)
        )
        conn.commit()
    except Exception as e:
        flash(f"Error al añadir la situación: {e}", 'error')

    cursor.close()
    conn.close()
    return redirect(url_for('inventario_bp.inventario'))