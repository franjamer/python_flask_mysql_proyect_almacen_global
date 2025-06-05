from flask import Blueprint, render_template, request, redirect, url_for
import database as db

pedidos_bp = Blueprint('pedidos_bp', __name__)

@pedidos_bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    conn = db.get_connection()
    cursor = conn.cursor()

    mensaje_error = None

    if request.method == 'POST':
        referencia_pedido = request.form.get('referencia_pedido', '').strip()
        fecha_creacion = request.form.get('fecha_creacion', '').strip()
        referencias = request.form.getlist('referencia_articulo[]')
        cantidades_pedidas = request.form.getlist('cantidad_pedida[]')
        cantidades_recibidas = request.form.getlist('cantidad_recibida[]')
        fechas_recibido = request.form.getlist('fecha_recibido[]')

        # Validar campos de cabecera
        if not referencia_pedido:
            mensaje_error = "El campo 'Referencia del pedido' es obligatorio."
        elif not fecha_creacion:
            mensaje_error = "El campo 'Fecha creación' es obligatorio."
        # Validar que haya al menos una línea de repuesto
        elif not referencias or all(ref.strip() == '' for ref in referencias):
            mensaje_error = "Debes añadir al menos un repuesto al pedido."
        else:
            # Validar que todas las líneas tengan datos obligatorios
            for i in range(len(referencias)):
                if not referencias[i].strip():
                    mensaje_error = f"Falta la referencia del repuesto en la línea {i+1}."
                    break
                if not cantidades_pedidas[i].strip():
                    mensaje_error = f"Falta la cantidad pedida en la línea {i+1}."
                    break
                if not cantidades_recibidas[i].strip():
                    mensaje_error = f"Falta la cantidad recibida en la línea {i+1}."
                    break

        if not mensaje_error:
            completo = False  # Se actualizará después

            # Insertar cabecera del pedido
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

                # Obtener el nombre del artículo desde inventario
                cursor.execute("SELECT nombre FROM inventario_tabla WHERE referencia = %s", (referencias[i],))
                resultado = cursor.fetchone()
                nombre_articulo = resultado[0] if resultado else ""

                cursor.execute("""
                    INSERT INTO lineas_pedido_tabla
                    (pedido_id, referencia_articulo, nombre_articulo, cantidad_pedida, cantidad_recibida, fecha_recibido, completo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (pedido_id, referencias[i], nombre_articulo, cantidad_pedida, cantidad_recibida, fecha_recibido, completo_linea))

            # Actualizar campo completo en cabecera si todas las líneas están completas
            cursor.execute("""
                SELECT COUNT(*) FROM lineas_pedido_tabla WHERE pedido_id = %s AND completo = 0
            """, (pedido_id,))
            incompletas = cursor.fetchone()[0]
            if incompletas == 0:
                cursor.execute("UPDATE pedidos_global_tabla SET completo = 1 WHERE id = %s", (pedido_id,))

            conn.commit()

    # Obtener referencias y nombres del inventario
    cursor.execute("SELECT referencia, nombre FROM inventario_tabla")
    inventario = cursor.fetchall()

    # Obtener pedidos globales
    cursor.execute("SELECT * FROM pedidos_global_tabla ORDER BY id DESC LIMIT 50")
    pedidos = cursor.fetchall()

    # Obtener líneas si se ha seleccionado un pedido
    pedido_id = request.args.get('pedido_id')
    lineas = []
    if pedido_id:
        cursor.execute("SELECT * FROM lineas_pedido_tabla WHERE pedido_id = %s", (pedido_id,))
        lineas = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('pedidos.html', pedidos=pedidos, inventario=inventario, lineas=lineas, mensaje_error=mensaje_error)

@pedidos_bp.route('/actualizar_linea/<int:linea_id>', methods=['POST'])
def actualizar_linea(linea_id):
    cantidad_pedida = int(request.form['cantidad_pedida'])
    cantidad_recibida = int(request.form['cantidad_recibida'])
    fecha_recibido = request.form.get('fecha_recibido') or None
    completo = cantidad_pedida == cantidad_recibida

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE lineas_pedido_tabla
        SET cantidad_pedida = %s,
            cantidad_recibida = %s,
            fecha_recibido = %s,
            completo = %s
        WHERE id = %s
    """, (cantidad_pedida, cantidad_recibida, fecha_recibido, completo, linea_id))

    # Actualizar el campo completo del pedido si corresponde
    cursor.execute("""
        SELECT pedido_id FROM lineas_pedido_tabla WHERE id = %s
    """, (linea_id,))
    pedido_id_db = cursor.fetchone()[0]
    cursor.execute("""
        SELECT COUNT(*) FROM lineas_pedido_tabla WHERE pedido_id = %s AND completo = 0
    """, (pedido_id_db,))
    incompletas = cursor.fetchone()[0]
    cursor.execute("""
        UPDATE pedidos_global_tabla SET completo = %s WHERE id = %s
    """, (incompletas == 0, pedido_id_db))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('pedidos_bp.pedidos', pedido_id=pedido_id_db))

    @pedidos_bp.route('/modificar_pedido/<int:pedido_id>', methods=['GET', 'POST'])
    def modificar_pedido(pedido_id):
    # Aquí va la lógica para modificar el pedido
    # Por ahora solo redirige de vuelta
    return redirect(url_for('pedidos_bp.pedidos', pedido_id=pedido_id))