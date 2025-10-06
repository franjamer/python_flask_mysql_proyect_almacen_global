from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .utilidades import asegurar_fila_minima_auto
import database as db
from routes.configuracion import cargar_configuracion
from .configuracion_general import obtener_nombres_columnas
from .vistas_config import VISTAS
from .configuracion_estilos import cargar_estilos_por_vista

inventario_bp = Blueprint('inventario_bp', __name__)

CAMPOS = VISTAS['inventario']['columnas']


def puede_crear_actualizar():
    return session.get('rol') in ['admin', 'pedidos']


def puede_eliminar():
    return session.get('rol') == 'admin'


def puede_ver():
    return session.get('rol') in ['admin', 'pedidos', 'perfil']


@inventario_bp.route('/inventario', methods=['GET', 'POST'])
def inventario():
    mensaje_error = None
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    # Cargar posiciones para el modal
    cursor.execute(
        "SELECT * FROM situacion_tabla ORDER BY almacen, estanteria, columna, altura")
    posiciones = cursor.fetchall()

    if request.method == 'POST' and puede_crear_actualizar():
        datos = {campo: request.form.get(campo, '').strip()
                 for campo in CAMPOS}
        # Validar obligatorios
        obligatorios = ['referencia', 'categoria']
        if any(datos[campo] == '' for campo in obligatorios):
            mensaje_error = "Referencia y Categoría son obligatorios."
        else:
            try:
                placeholders = ','.join(['%s'] * len(CAMPOS))
                campos_str = ','.join(CAMPOS)
                valores = [datos[campo] if campo != 'stock' else (
                    datos[campo] if datos[campo] != '' else 0) for campo in CAMPOS]
                # Si no se seleccionó situación, poner None
                if not datos['id_situacion_tabla']:
                    valores[-1] = None
                cursor.execute(
                    f"INSERT INTO inventario_tabla ({campos_str}) VALUES ({placeholders})",
                    tuple(valores)
                )
                conn.commit()
            except Exception as e:
                mensaje_error = "Error al añadir el repuesto: " + str(e)
            if not mensaje_error:
                cursor.close()
                conn.close()
                return redirect(url_for('inventario_bp.inventario'))

    # Mostrar todos los repuestos con JOIN a situación
    cursor.execute("""
        SELECT i.*, 
            s.almacen AS almacen_situacion, s.estanteria, s.columna, s.altura, s.lado,
            CONCAT(s.almacen, '-', s.estanteria, '-', s.lado, '-', s.columna, '-', s.altura) AS ubicacion
        FROM inventario_tabla i
        LEFT JOIN situacion_tabla s ON i.id_situacion_tabla = s.id_situacion_tabla
        ORDER BY i.id
    """)

    repuestos = cursor.fetchall()
    cursor.close()
    conn.close()
    columnas = ['id'] + CAMPOS

    # Cargar configuración personalizada
    config = cargar_configuracion()
    nombres_columnas = obtener_nombres_columnas('inventario')

    estilos_por_vista = cargar_estilos_por_vista()

    return render_template(
        'inventario.html',
        repuestos=repuestos,
        columnas=columnas,
        mensaje_error=mensaje_error,
        puede_crear_actualizar=puede_crear_actualizar,
        puede_eliminar=puede_eliminar,
        posiciones=posiciones,
        config=config,
        nombres_columnas=nombres_columnas,
        vista='inventario',
        estilos_por_vista=estilos_por_vista
    )


@inventario_bp.route('/inventario/modificar/<int:id>', methods=['POST'])
def modificar_repuesto(id):
    if not puede_crear_actualizar():
        return redirect(url_for('inventario_bp.inventario'))
    CAMPOS_EDIT = [c for c in CAMPOS]
    datos = {campo: request.form.get(campo, '').strip() for campo in CAMPOS_EDIT}
    conn = db.get_connection()
    cursor = conn.cursor()

    # Verificar si el registro existe
    cursor.execute("SELECT referencia FROM inventario_tabla WHERE id=%s", (id,))
    repuesto = cursor.fetchone()
    if not repuesto:
        flash("El repuesto no existe.", "error")
        cursor.close()
        conn.close()
        return redirect(url_for('inventario_bp.inventario'))

    set_clause = ', '.join([f"{campo}=%s" for campo in CAMPOS_EDIT])
    valores = [datos[campo] if campo != 'stock' else (datos[campo] if datos[campo] != '' else 0) for campo in CAMPOS_EDIT]
    valores.append(id)
    cursor.execute(
        f"UPDATE inventario_tabla SET {set_clause} WHERE id=%s",
        tuple(valores)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('inventario_bp.inventario'))


@inventario_bp.route('/inventario/eliminar/<int:id>', methods=['POST'])
def eliminar_repuesto(id):
    if not puede_eliminar():
        return redirect(url_for('inventario_bp.inventario'))
    conn = db.get_connection()
    cursor = conn.cursor()

    # Obtener referencia para borrar movimientos
    cursor.execute("SELECT referencia FROM inventario_tabla WHERE id=%s", (id,))
    repuesto = cursor.fetchone()
    referencia = repuesto[0] if repuesto else None

    try:
        if referencia:
            cursor.execute(
                "DELETE FROM movimientos_tabla WHERE referencia_pieza_repuesto=%s", (referencia,)
            )
            conn.commit()
        asegurar_fila_minima_auto('inventario_tabla')
        cursor.execute(
            "DELETE FROM inventario_tabla WHERE id=%s", (id,)
        )
        conn.commit()
    except Exception as e:
        flash(f"Error al eliminar el repuesto: {e}", 'error')

    cursor.close()
    conn.close()
    return redirect(url_for('inventario_bp.inventario'))
