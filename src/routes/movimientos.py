from flask import Blueprint, render_template, request, redirect, url_for, session
import database as db
from routes.roles import puede_eliminar_movimientos

movimientos_bp = Blueprint('movimientos_bp', __name__)


@movimientos_bp.route('/movimientos', methods=['GET', 'POST'])
def movimientos():
    mensaje_error = None
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener inventario para el select
    cursor.execute(
        "SELECT referencia, nombre FROM inventario_tabla ORDER BY nombre ASC")
    inventario = cursor.fetchall()

    # Obtener perfiles para el select (de la tabla 'perfiles')
    cursor.execute(
        "SELECT idperfil,codigo_operador FROM perfiles ORDER BY idperfil ASC")
    perfiles = cursor.fetchall()

    if request.method == 'POST':
        referencia_pieza = request.form['referencia_pieza_repuesto']
        tipo = request.form['tipo_de_movimiento']
        cantidad = int(request.form.get('cantidad', 0))
        unidad = request.form.get('unidad_de_cantidad', '')
        codigo_perfil = request.form['codigo_perfil']
        fecha = request.form.get('fecha_movimiento', None)

        # Obtener nombre del repuesto a partir de la referencia
        cursor.execute(
            "SELECT nombre, stock FROM inventario_tabla WHERE referencia = %s", (referencia_pieza,))
        result = cursor.fetchone()
        if not result:
            mensaje_error = "Repuesto no encontrado."
        else:
            nombre_pieza = result['nombre']
            stock_actual = result['stock']
            if tipo == 'salida':
                stock_nuevo = stock_actual - cantidad
            elif tipo == 'entrada':
                stock_nuevo = stock_actual + cantidad
            elif tipo == 'inventario':
                stock_nuevo = cantidad
            else:
                stock_nuevo = stock_actual
            # Actualizar stock
            cursor.execute(
                "UPDATE inventario_tabla SET stock = %s WHERE referencia = %s", (stock_nuevo, referencia_pieza))
            # Insertar movimiento (guardando referencia y nombre)
            cursor.execute("""
                INSERT INTO movimientos_tabla (referencia_pieza_repuesto, nombre_pieza_repuesto, tipo_de_movimiento, cantidad, unidad_de_cantidad, codigo_perfil, fecha_movimiento, stock_tras_movimiento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (referencia_pieza, nombre_pieza, tipo, cantidad, unidad, codigo_perfil, fecha, stock_nuevo))
            conn.commit()
        if not mensaje_error:
            cursor.close()
            conn.close()
            return redirect(url_for('movimientos_bp.movimientos'))

    # Mostrar movimientos (incluyendo referencia)
    cursor.execute("""
        SELECT idmovimientos, referencia_pieza_repuesto, nombre_pieza_repuesto, tipo_de_movimiento, cantidad, unidad_de_cantidad, codigo_perfil, fecha_movimiento, stock_tras_movimiento
        FROM movimientos_tabla
        ORDER BY fecha_movimiento DESC
    """)
    movimientos = cursor.fetchall()
    cursor.close()
    conn.close()
    print("Movimientos obtenidos:", movimientos)
    return render_template(
        'movimientos.html',
        movimientos=movimientos,
        inventario=inventario,
        perfiles=perfiles,
        mensaje_error=mensaje_error,
        puede_eliminar_movimientos=puede_eliminar_movimientos
    )


@movimientos_bp.route('/movimientos/eliminar/<int:idmovimientos>', methods=['POST'])
def eliminar_movimiento(idmovimientos):
    if not puede_eliminar_movimientos(session.get('rol')):
        return redirect(url_for('movimientos_bp.movimientos'))
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM movimientos_tabla WHERE idmovimientos = %s", (idmovimientos,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('movimientos_bp.movimientos'))
