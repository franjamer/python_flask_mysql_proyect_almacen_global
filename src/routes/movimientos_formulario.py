# En src/routes/movimientos_formulario.py

from flask import Blueprint, request, redirect, url_for, session
import database as db
# Asegúrate de importar la función de roles si la usas
from routes.roles import puede_eliminar_movimientos

# Creamos el Blueprint para el formulario
movimientos_form_bp = Blueprint('movimientos_form_bp', __name__)

@movimientos_form_bp.route('/add_movimiento', methods=['POST'])
def add_movimiento():
    # 🎯 Vamos a añadir un print para confirmar que la función se está ejecutando.
    print("Función add_movimiento ejecutada. Procesando formulario...")
    
    # Abrimos la conexión a la base de datos al inicio de la función.
    conn = None
    cursor = None
    try:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 1. Obtener datos del formulario
        referencia_pieza = request.form.get('referencia_pieza_repuesto')
        tipo = request.form.get('tipo_de_movimiento')
        cantidad = int(request.form.get('cantidad', 0))
        unidad = request.form.get('unidad_de_cantidad')
        codigo_operador = request.form.get('codigo_operador')
        fecha = request.form.get('fecha_movimiento')

        # 2. Validación básica
        if not all([referencia_pieza, tipo, cantidad > 0, codigo_operador, fecha]):
            print("Validación fallida: Faltan datos o la cantidad no es válida.")
            # 💡 Si la validación falla, redirigimos con un mensaje de error.
            # Necesitarás modificar tu plantilla para mostrar `mensaje_error` al redirigir.
            # Por ahora, simplemente redirigiremos para no bloquear.
            return redirect(url_for('movimientos_bp.movimientos_table_bp.movimientos_tabla', mensaje_error="Faltan datos obligatorios."))

        # 3. Obtener stock y nombre actuales del inventario
        cursor.execute("SELECT nombre, stock FROM inventario_tabla WHERE referencia = %s", (referencia_pieza,))
        result = cursor.fetchone()

        if not result:
            print("Validación fallida: Repuesto no encontrado en el inventario.")
            return redirect(url_for('movimientos_bp.movimientos_table_bp.movimientos_tabla', mensaje_error="Repuesto no encontrado."))

        nombre_pieza = result['nombre']
        stock_actual = result['stock']
        
        # 4. Calcular el nuevo stock
        stock_nuevo = stock_actual
        if tipo == 'salida':
            stock_nuevo = stock_actual - cantidad
        elif tipo == 'entrada':
            stock_nuevo = stock_actual + cantidad
        elif tipo == 'inventario':
            stock_nuevo = cantidad
        
        # 5. Actualizar stock en la tabla de inventario
        print(f"Actualizando stock para {referencia_pieza}: {stock_actual} -> {stock_nuevo}")
        cursor.execute("UPDATE inventario_tabla SET stock = %s WHERE referencia = %s", (stock_nuevo, referencia_pieza))
        
        # 6. Insertar el nuevo movimiento en la tabla de movimientos
        print(f"Insertando nuevo movimiento: {referencia_pieza}, tipo: {tipo}, cantidad: {cantidad}, operador: {codigo_operador}")
        cursor.execute("""
            INSERT INTO movimientos_tabla (referencia_pieza_repuesto, nombre_pieza_repuesto, tipo_de_movimiento, cantidad, unidad_de_cantidad, codigo_operador, fecha_movimiento, stock_tras_movimiento)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (referencia_pieza, nombre_pieza, tipo, cantidad, unidad, codigo_operador, fecha, stock_nuevo))
        
        # 7. Confirmar los cambios en la base de datos
        conn.commit()
        print("Movimiento añadido y stock actualizado. Commit realizado.")
        
    except Exception as e:
        # Si ocurre un error, deshacemos los cambios para evitar datos inconsistentes.
        if conn:
            conn.rollback()
        print(f"Ocurrió un error al añadir el movimiento: {e}")
        # Aquí también podrías redirigir con un mensaje de error.
        return redirect(url_for('movimientos_bp.movimientos_table_bp.movimientos_tabla', mensaje_error=f"Error al guardar: {e}"))
        
    finally:
        # Aseguramos que la conexión y el cursor se cierran siempre.
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # 8. Redirigir al usuario de vuelta a la página de movimientos (para ver la tabla actualizada)
    print("Redirigiendo a la vista de tabla.")
    return redirect(url_for('movimientos_bp.movimientos_table_bp.movimientos_tabla'))