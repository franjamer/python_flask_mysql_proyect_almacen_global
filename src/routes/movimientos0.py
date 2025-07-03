from flask import Blueprint, render_template, request, redirect, url_for, session
import database as db
from routes.roles import puede_eliminar_movimientos

# Crea el Blueprint para los movimientos
movimientos_bp = Blueprint('movimientos_bp', __name__)

# Maneja las peticiones GET y POST para la gestión de movimientos.


@movimientos_bp.route('/movimientos', methods=['GET', 'POST'])
def movimientos():
    mensaje_error = None
    conn = None
    cursor = None
    inventario = []
    operadores = []
    movimientos_lista = []

    try:
        # 1. Conexión a la base de datos
        conn = db.get_connection()
        if conn is None:
            raise Exception(
                "No se pudo conectar a la base de datos. Verifica tu archivo database.py y el servidor MySQL.")

        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            # Obtener datos del formulario
            referencia_pieza = request.form.get('referencia_pieza_repuesto')
            tipo = request.form.get('tipo_de_movimiento')
            cantidad = int(request.form.get('cantidad', 0))
            unidad = request.form.get('unidad_de_cantidad', 'Unidad')
            codigo_operador = request.form.get('codigo_operador_form', None)
            fecha = request.form.get('fecha_movimiento', None)

            # Validar que se seleccionó un operador
            if not codigo_operador:
                mensaje_error = "Debes seleccionar un operador."
            else:
                # Obtener nombre del repuesto y stock para actualizar (con bloqueo de fila)
                cursor.execute(
                    "SELECT nombre, stock FROM inventario_tabla WHERE referencia = %s FOR UPDATE", (referencia_pieza,))
                result = cursor.fetchone()

                if not result:
                    mensaje_error = "Repuesto no encontrado."
                else:
                    nombre_pieza = result['nombre']
                    stock_actual = result['stock']

                    # Calcular nuevo stock
                    if tipo == 'salida':
                        stock_nuevo = stock_actual - cantidad
                    elif tipo == 'entrada':
                        stock_nuevo = stock_actual + cantidad
                    elif tipo == 'inventario':
                        stock_nuevo = cantidad
                    else:
                        stock_nuevo = stock_actual

                    # Insertar movimiento
                    cursor.execute("""
                        INSERT INTO movimientos_tabla (referencia_pieza_repuesto, nombre_pieza_repuesto, tipo_de_movimiento, cantidad, unidad_de_cantidad, codigo_operador, fecha_movimiento, stock_tras_movimiento)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (referencia_pieza, nombre_pieza, tipo, cantidad, unidad, codigo_operador, fecha, stock_nuevo))

                    # Actualizar stock del inventario
                    cursor.execute(
                        "UPDATE inventario_tabla SET stock = %s WHERE referencia = %s", (stock_nuevo, referencia_pieza))

                    # Confirmar la transacción
                    conn.commit()

                    # Redirigir para evitar reenvíos de formulario
                    return redirect(url_for('movimientos_bp.movimientos'))

        # Cargar SIEMPRE los datos para los selects y la tabla, tanto en GET como en POST (con o sin error)
        cursor.execute(
            "SELECT referencia, nombre FROM inventario_tabla ORDER BY nombre ASC")
        inventario = cursor.fetchall()
        cursor.execute(
            "SELECT id_operador, codigo_operador, nombre_completo FROM operadores ORDER BY id_operador ASC")
        operadores = cursor.fetchall()
        cursor.execute("""
            SELECT idmovimientos, referencia_pieza_repuesto, nombre_pieza_repuesto, tipo_de_movimiento, cantidad, unidad_de_cantidad, codigo_operador, fecha_movimiento, stock_tras_movimiento
            FROM movimientos_tabla
            ORDER BY fecha_movimiento DESC
        """)
        movimientos_lista = cursor.fetchall()

    except Exception as e:
        # En caso de cualquier error, hacemos rollback
        if conn:
            conn.rollback()
        mensaje_error = f"Error al cargar o procesar los datos: {e}. Inténtalo de nuevo."
        print(f"--- ERROR CAPTURADO en la vista movimientos() ---")
        print(f"Detalle del error: {e}")
        inventario = []
        operadores = []
        movimientos_lista = []

    finally:
        # Asegurarse de que el cursor y la conexión se cierran siempre
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Renderizar la plantilla
    print("OPERADORES ENVIADOS A LA PLANTILLA:", operadores)
    return render_template(
        'movimientos.html',
        movimientos=movimientos_lista,
        inventario=inventario,
        operadores=operadores,
        mensaje_error=mensaje_error,
        puede_eliminar_movimientos=puede_eliminar_movimientos
    )

# Ruta para eliminar movimientos


@movimientos_bp.route('/movimientos/eliminar/<int:idmovimientos>', methods=['POST'])
def eliminar_movimiento(idmovimientos):
    if not puede_eliminar_movimientos(session.get('rol')):
        return redirect(url_for('movimientos_bp.movimientos'))

    conn = None
    cursor = None
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM movimientos_tabla WHERE idmovimientos = %s", (idmovimientos,))
        conn.commit()
    except Exception as e:
        print(f"Error al eliminar movimiento: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return redirect(url_for('movimientos_bp.movimientos'))
