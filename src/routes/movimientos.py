from flask import Blueprint, request, redirect, url_for
import database as db

movimientos_bp = Blueprint('movimientos_bp', __name__)

@movimientos_bp.route('/movimientos/add', methods=['POST'])
def add_movimiento():
    nombre_pieza = request.form['nombre_pieza_repuesto']
    tipo = request.form['tipo_de_movimiento']
    cantidad = int(request.form.get('cantidad', 0))
    unidad = request.form.get('unidad_de_cantidad', '')
    codigo_usuario = request.form['codigo_usuario']
    fecha = request.form.get('fecha_movimiento', None)
    stock_nuevo = None

    # Usar una nueva conexión para cada petición
    conn = db.get_connection()
    cursor = conn.cursor()

    # Obtener stock actual
    cursor.execute("SELECT stock FROM inventario_tabla WHERE nombre = %s", (nombre_pieza,))
    stock_actual = cursor.fetchone()[0]

    if tipo == 'salida':
        stock_nuevo = stock_actual - cantidad
    elif tipo == 'entrada':
        stock_nuevo = stock_actual + cantidad
    elif tipo == 'inventario':
        stock_nuevo = cantidad  # Aquí 'cantidad' es el nuevo stock

    # Actualizar stock en inventario_tabla
    cursor.execute("UPDATE inventario_tabla SET stock = %s WHERE nombre = %s", (stock_nuevo, nombre_pieza))
    # Insertar movimiento
    cursor.execute("""
        INSERT INTO movimientos_tabla (nombre_pieza_repuesto, tipo_de_movimiento, cantidad, unidad_de_cantidad, codigo_usuario, fecha_movimiento, stock_tras_movimiento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nombre_pieza, tipo, cantidad, unidad, codigo_usuario, fecha, stock_nuevo))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home_bp.movimientos'))