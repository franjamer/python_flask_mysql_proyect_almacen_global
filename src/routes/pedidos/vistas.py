from flask import Blueprint, render_template, request, redirect, url_for, session
from .utils import validar_pedido, obtener_nombre_articulo
from routes.roles import puede_crud_pedidos, puede_eliminar_pedidos
import database as db

pedidos_bp = Blueprint('pedidos_bp', __name__)

@pedidos_bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    conn = db.get_connection()
    cursor = conn.cursor()
    mensaje_error = None

    if request.method == 'POST':
        if not puede_crud_pedidos(session.get('rol')):
            return redirect(url_for('pedidos_bp.pedidos'))
        mensaje_error = validar_pedido(request.form)
        if not mensaje_error:
            referencia_pedido = request.form['referencia_pedido']
            fecha_creacion = request.form['fecha_creacion']
            referencias = request.form.getlist('referencia_articulo[]')
            cantidades_pedidas = request.form.getlist('cantidad_pedida[]')
            cantidades_recibidas = request.form.getlist('cantidad_recibida[]')
            fechas_recibido = request.form.getlist('fecha_recibido[]')

            completo = False
            cursor.execute("""
                INSERT INTO pedidos_global_tabla (referencia_pedido, fecha_creacion, completo)
                VALUES (%s, %s, %s)
            """, (referencia_pedido, fecha_creacion, completo))
            pedido_id = cursor.lastrowid

            for i in range(len(referencias)):
                cantidad_pedida = int(cantidades_pedidas[i])
                cantidad_recibida = int(cantidades_recibidas[i]) if cantidades_recibidas[i] else 0
                fecha_recibido = fechas_recibido[i] if fechas_recibido[i] else None
                completo_linea = cantidad_pedida == cantidad_recibida

                nombre_articulo = obtener_nombre_articulo(cursor, referencias[i])

                cursor.execute("""
                    INSERT INTO lineas_pedido_tabla
                    (pedido_id, referencia_articulo, nombre_articulo, cantidad_pedida, cantidad_recibida, fecha_recibido, completo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (pedido_id, referencias[i], nombre_articulo, cantidad_pedida, cantidad_recibida, fecha_recibido, completo_linea))

            cursor.execute("""
                SELECT COUNT(*) FROM lineas_pedido_tabla WHERE pedido_id = %s AND completo = 0
            """, (pedido_id,))
            incompletas = cursor.fetchone()[0]
            if incompletas == 0:
                cursor.execute("UPDATE pedidos_global_tabla SET completo = 1 WHERE id = %s", (pedido_id,))

            conn.commit()

    cursor.execute("SELECT referencia, nombre FROM inventario_tabla")
    inventario = cursor.fetchall()
    cursor.execute("SELECT * FROM pedidos_global_tabla ORDER BY id DESC LIMIT 50")
    pedidos = cursor.fetchall()
    pedido_id = request.args.get('pedido_id')
    lineas = []
    if pedido_id:
        cursor.execute("SELECT * FROM lineas_pedido_tabla WHERE pedido_id = %s", (pedido_id,))
        lineas = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template(
        'pedidos.html',
        pedidos=pedidos,
        inventario=inventario,
        lineas=lineas,
        mensaje_error=mensaje_error,
        puede_crud_pedidos=puede_crud_pedidos,
        puede_eliminar_pedidos=puede_eliminar_pedidos
    )

@pedidos_bp.route('/actualizar_linea/<int:linea_id>', methods=['POST'])
def actualizar_linea(linea_id):
    if not puede_crud_pedidos(session.get('rol')):
        return redirect(url_for('pedidos_bp.pedidos'))
    cantidad_pedida = int(request.form['cantidad_pedida'])
    cantidad_recibida = int(request.form['cantidad_recibida'])
    fecha_recibido = request.form.get('fecha_recibido')

    conn = db.get_connection()
    cursor = conn.cursor()
    if not fecha_recibido:
        cursor.execute("SELECT fecha_recibido FROM lineas_pedido_tabla WHERE id = %s", (linea_id,))
        result = cursor.fetchone()
        fecha_recibido = result[0] if result else None

    completo = cantidad_recibida >= cantidad_pedida

    cursor.execute("""
        UPDATE lineas_pedido_tabla
        SET cantidad_pedida = %s,
            cantidad_recibida = %s,
            fecha_recibido = %s,
            completo = %s
        WHERE id = %s
    """, (cantidad_pedida, cantidad_recibida, fecha_recibido, completo, linea_id))

    cursor.execute("SELECT pedido_id FROM lineas_pedido_tabla WHERE id = %s", (linea_id,))
    pedido_id_db = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM lineas_pedido_tabla WHERE pedido_id = %s AND completo = 0", (pedido_id_db,))
    incompletas = cursor.fetchone()[0]
    cursor.execute("UPDATE pedidos_global_tabla SET completo = %s WHERE id = %s", (incompletas == 0, pedido_id_db))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('pedidos_bp.pedidos', pedido_id=pedido_id_db))

@pedidos_bp.route('/eliminar_pedido/<int:pedido_id>', methods=['POST'])
def eliminar_pedido(pedido_id):
    if not puede_eliminar_pedidos(session.get('rol')):
        return redirect(url_for('pedidos_bp.pedidos'))
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lineas_pedido_tabla WHERE pedido_id = %s", (pedido_id,))
    cursor.execute("DELETE FROM pedidos_global_tabla WHERE id = %s", (pedido_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('pedidos_bp.pedidos'))

@pedidos_bp.route('/eliminar_linea/<int:linea_id>', methods=['POST'])
def eliminar_linea(linea_id):
    if not puede_eliminar_pedidos(session.get('rol')):
        return redirect(url_for('pedidos_bp.pedidos'))
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pedido_id FROM lineas_pedido_tabla WHERE id = %s", (linea_id,))
    result = cursor.fetchone()
    if not result:
        cursor.close()
        conn.close()
        return redirect(url_for('pedidos_bp.pedidos'))
    pedido_id_db = result[0]
    cursor.execute("SELECT COUNT(*) FROM lineas_pedido_tabla WHERE pedido_id = %s", (pedido_id_db,))
    num_lineas = cursor.fetchone()[0]
    if num_lineas > 1:
        cursor.execute("DELETE FROM lineas_pedido_tabla WHERE id = %s", (linea_id,))
        conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('pedidos_bp.pedidos', pedido_id=pedido_id_db))

@pedidos_bp.route('/modificar_pedido/<int:pedido_id>', methods=['GET', 'POST'])
def modificar_pedido(pedido_id):
    if not puede_crud_pedidos(session.get('rol')):
        return redirect(url_for('pedidos_bp.pedidos'))
    conn = db.get_connection()
    cursor = conn.cursor()
    mensaje_error = None

    if request.method == 'POST':
        mensaje_error = validar_pedido(request.form)
        if not mensaje_error:
            referencia_pedido = request.form['referencia_pedido']
            fecha_creacion = request.form['fecha_creacion']
            referencias = request.form.getlist('referencia_articulo[]')
            cantidades_pedidas = request.form.getlist('cantidad_pedida[]')
            cantidades_recibidas = request.form.getlist('cantidad_recibida[]')
            fechas_recibido = request.form.getlist('fecha_recibido[]')

            cursor.execute("""
                UPDATE pedidos_global_tabla
                SET referencia_pedido = %s, fecha_creacion = %s
                WHERE id = %s
            """, (referencia_pedido, fecha_creacion, pedido_id))

            cursor.execute("DELETE FROM lineas_pedido_tabla WHERE pedido_id = %s", (pedido_id,))

            for i in range(len(referencias)):
                cantidad_pedida = int(cantidades_pedidas[i])
                cantidad_recibida = int(cantidades_recibidas[i]) if cantidades_recibidas[i] else 0
                fecha_recibido = fechas_recibido[i] if fechas_recibido[i] else None
                completo_linea = cantidad_pedida == cantidad_recibida

                nombre_articulo = obtener_nombre_articulo(cursor, referencias[i])

                cursor.execute("""
                    INSERT INTO lineas_pedido_tabla
                    (pedido_id, referencia_articulo, nombre_articulo, cantidad_pedida, cantidad_recibida, fecha_recibido, completo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (pedido_id, referencias[i], nombre_articulo, cantidad_pedida, cantidad_recibida, fecha_recibido, completo_linea))

            cursor.execute("SELECT COUNT(*) FROM lineas_pedido_tabla WHERE pedido_id = %s AND completo = 0", (pedido_id,))
            incompletas = cursor.fetchone()[0]
            cursor.execute("UPDATE pedidos_global_tabla SET completo = %s WHERE id = %s", (incompletas == 0, pedido_id))

            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('pedidos_bp.pedidos', pedido_id=pedido_id))

    cursor.execute("SELECT referencia_pedido, fecha_creacion FROM pedidos_global_tabla WHERE id = %s", (pedido_id,))
    pedido = cursor.fetchone()
    cursor.execute("SELECT * FROM lineas_pedido_tabla WHERE pedido_id = %s", (pedido_id,))
    lineas = cursor.fetchall()
    cursor.execute("SELECT referencia, nombre FROM inventario_tabla")
    inventario = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        'modificar_pedido.html',
        pedido_id=pedido_id,
        pedido=pedido,
        lineas=lineas,
        inventario=inventario,
        mensaje_error=mensaje_error
    )