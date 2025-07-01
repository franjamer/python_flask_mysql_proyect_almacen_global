from flask import Blueprint, render_template, session, redirect, url_for
import database as db
from routes.roles import puede_eliminar_movimientos
import time
# Crea el Blueprint para la tabla y las acciones relacionadas.
movimientos_table_bp = Blueprint('movimientos_table_bp', __name__)

@movimientos_table_bp.route('/')
def movimientos_tabla():
    """
    Ruta principal para la vista de movimientos.
    Carga los datos de inventario, operadores y movimientos
    y renderiza la plantilla principal.
    """
    conn = None
    cursor = None
    movimientos = []
    inventario = []
    operadores = []
    mensaje_error = None
    
    try:
        # 1. Obtener la conexión a la base de datos.
        conn = db.get_connection()
        if conn is None:
            # Si la conexión es None, lanza una excepción para ir al bloque `except`.
            raise Exception("No se pudo conectar a la base de datos. Por favor, verifica la configuración.")
             # 🎯 PASO DE DIAGNÓSTICO: AÑADIR UN PEQUEÑO RETRASO.
            # Si esto funciona, confirma que es una condición de carrera.
            time.sleep(0.5) 
        # 2. Ejecutar una consulta de prueba para "calentar" la conexión.
        # Esto evita el problema del "movimiento fantasma".
        with conn.cursor() as test_cursor:
            test_cursor.execute("SELECT 1")
            test_cursor.fetchone()
        
        # 3. Crear el cursor para las consultas reales de la vista.
        # Usamos `dictionary=True` para obtener resultados como diccionarios.
        # Usamos `buffered=True` para manejar múltiples consultas sin errores.
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        # 4. Cargar datos para los formularios.
        cursor.execute("SELECT referencia, nombre FROM inventario_tabla ORDER BY nombre ASC")
        inventario = cursor.fetchall()
        
        cursor.execute("SELECT id_operador, codigo_operador, nombre_completo FROM operadores ORDER BY codigo_operador ASC")
        operadores = cursor.fetchall()

        # 5. Cargar datos para la tabla de movimientos.
        cursor.execute("""
            SELECT idmovimientos, referencia_pieza_repuesto, nombre_pieza_repuesto, tipo_de_movimiento,
                   cantidad, unidad_de_cantidad, codigo_operador, fecha_movimiento, stock_tras_movimiento
            FROM movimientos_tabla
            ORDER BY fecha_movimiento DESC
        """)
        movimientos = cursor.fetchall()
        
    except Exception as e:
        # 6. Capturar cualquier error (conexión, consulta, etc.) y manejarlo.
        print(f"Error en la vista movimientos_tabla: {e}")
        # Aseguramos que las variables de la plantilla son listas vacías si hay un error.
        movimientos = []
        inventario = []
        operadores = []
        mensaje_error = f"Error al cargar los datos: {e}"
        
    finally:
        # 7. Asegurar que la conexión se cierra en cualquier caso.
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    # 8. Renderizar la plantilla con todas las variables definidas.
    # El valor de `puede_eliminar_movimientos` se calcula aquí para pasarlo a la plantilla.
    puede_eliminar = puede_eliminar_movimientos(session.get('rol'))
    
    return render_template(
        'movimientos.html',
        movimientos=movimientos,
        inventario=inventario,
        operadores=operadores,
        puede_eliminar_movimientos=puede_eliminar,
        mensaje_error=mensaje_error
    )


@movimientos_table_bp.route('/eliminar/<int:idmovimientos>', methods=['POST'])
def eliminar_movimiento(idmovimientos):
    """
    Ruta para eliminar un movimiento.
    Solo accesible para usuarios con el rol adecuado.
    """
    # 1. Verificar los permisos del usuario.
    if not puede_eliminar_movimientos(session.get('rol')):
        return redirect(url_for('movimientos_bp.movimientos_table_bp.movimientos_tabla'))

    conn = None
    cursor = None
    try:
        # 2. Obtener la conexión y el cursor.
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 3. Ejecutar la consulta DELETE.
        cursor.execute("DELETE FROM movimientos_tabla WHERE idmovimientos = %s", (idmovimientos,))
        
        # 4. Confirmar los cambios en la base de datos.
        conn.commit()
        
    except Exception as e:
        print(f"Error al eliminar el movimiento {idmovimientos}: {e}")
        if conn:
            conn.rollback() # Deshacer si hay un error.
            
    finally:
        # 5. Cerrar la conexión y el cursor de forma segura.
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
    # 6. Redirigir de vuelta a la vista de la tabla.
    return redirect(url_for('movimientos_bp.movimientos_table_bp.movimientos_tabla'))