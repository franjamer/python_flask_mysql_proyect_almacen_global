from flask import Blueprint, render_template, request, redirect, url_for, session
from .utilidades import asegurar_fila_minima_auto
import database as db

inventario_bp = Blueprint('inventario_bp', __name__)

CAMPOS = [
    'referencia',
    'nombre',
    'categoria',
    'subcategoria',
    'almacen',
    'caracteristicas_medidas',
    'fotos_planos',
    'empaquetado',
    'stock',
    'stock_minimo',
    'stock_maximo',
    'id_situacion_tabla'
]


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
        LEFT JOIN situacion_tabla s ON i.id_situacion_tabla = s.id
        ORDER BY i.id
    """)
    repuestos = cursor.fetchall()
    cursor.close()
    conn.close()
    columnas = ['id'] + CAMPOS
    return render_template(
        'inventario.html',
        repuestos=repuestos,
        columnas=columnas,
        mensaje_error=mensaje_error,
        puede_crear_actualizar=puede_crear_actualizar,
        puede_eliminar=puede_eliminar,
        posiciones=posiciones
    )


@inventario_bp.route('/inventario/modificar/<referencia>', methods=['POST'])
def modificar_repuesto(referencia):
    if not puede_crear_actualizar():
        return redirect(url_for('inventario_bp.inventario'))
    CAMPOS_EDIT = [c for c in CAMPOS if c not in ['referencia', 'nombre']]
    datos = {campo: request.form.get(campo, '').strip()
             for campo in CAMPOS_EDIT}
    conn = db.get_connection()
    cursor = conn.cursor()
    set_clause = ', '.join([f"{campo}=%s" for campo in CAMPOS_EDIT])
    valores = [datos[campo] if campo != 'stock' else (
        datos[campo] if datos[campo] != '' else 0) for campo in CAMPOS_EDIT]
    valores.append(referencia)
    cursor.execute(
        f"UPDATE inventario_tabla SET {set_clause} WHERE referencia=%s",
        tuple(valores)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('inventario_bp.inventario'))


@inventario_bp.route('/inventario/eliminar/<referencia>', methods=['POST'])
def eliminar_repuesto(referencia):
    if not puede_eliminar():
        return redirect(url_for('inventario_bp.inventario'))
    conn = db.get_connection()
    cursor = conn.cursor()
    asegurar_fila_minima_auto('inventario_tabla')
    cursor.execute(
        "DELETE FROM inventario_tabla WHERE referencia=%s", (referencia,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('inventario_bp.inventario'))
