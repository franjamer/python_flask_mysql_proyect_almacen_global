from flask import Blueprint, render_template, request, redirect, url_for, session
import database as db
from routes.roles import puede_eliminar_movimientos

movimientos_bp = Blueprint('movimientos_bp', __name__)

@movimientos_bp.route('/movimientos', methods=['GET', 'POST'])
def movimientos():
    mensaje_error = None
    if request.method == 'POST':
        # Todos pueden crear movimientos
        nombre_pieza = request.form['nombre_pieza_repuesto']
        tipo = request.form['tipo_de_movimiento']
        cantidad = int(request.form.get('cantidad', 0))
        unidad = request.form.get('unidad_de_cantidad', '')
        codigo_usuario = request.form['codigo_usuario']
        fecha = request.form.get('fecha_movimiento', None)
        conn = db.get_connection()
        cursor = conn.cursor()
        # Obtener stock actual
        cursor.execute("SELECT stock FROM inventario_tabla WHERE nombre = %s", (nombre_pieza,))
        result = cursor.fetchone()
        if not result:
            mensaje_error = "Repuesto no encontrado."
        else:
            stock_actual = result[0]
            if tipo == 'salida':
                stock_nuevo = stock_actual - cantidad
            elif tipo == 'entrada':
                stock_nuevo = stock_actual + cantidad
            elif tipo == 'inventario':
                stock_nuevo = cantidad
            else:
                stock_nuevo = stock_actual
            # Actualizar stock
            cursor.execute("UPDATE inventario_tabla SET stock = %s WHERE nombre = %s", (stock_nuevo, nombre_pieza))
            # Insertar movimiento
            cursor.execute("""
                INSERT INTO movimientos_tabla (nombre_pieza_repuesto, tipo_de_movimiento, cantidad, unidad_de_cantidad, codigo_usuario, fecha_movimiento, stock_tras_movimiento)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre_pieza, tipo, cantidad, unidad, codigo_usuario, fecha, stock_nuevo))
            conn.commit()
        cursor.close()
        conn.close()
        if not mensaje_error:
            return redirect(url_for('movimientos_bp.movimientos'))
    # Mostrar movimientos
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre_pieza_repuesto, tipo_de_movimiento, cantidad, unidad_de_cantidad, codigo_usuario, fecha_movimiento, stock_tras_movimiento FROM movimientos_tabla ORDER BY fecha_movimiento DESC")
    movimientos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('movimientos.html', movimientos=movimientos, mensaje_error=mensaje_error, puede_eliminar_movimientos=puede_eliminar_movimientos)

@movimientos_bp.route('/movimientos/eliminar/<int:id>', methods=['POST'])
def eliminar_movimiento(id):
    if not puede_eliminar_movimientos(session.get('rol')):
        return redirect(url_for('movimientos_bp.movimientos'))
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movimientos_tabla WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('movimientos_bp.movimientos'))