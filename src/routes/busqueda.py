from flask import Blueprint, render_template, request
import database as db
from .vistas_config import VISTAS
from .configuracion_general import obtener_nombres_columnas

busqueda_bp = Blueprint('busqueda_bp', __name__)

campos_busqueda_permitidos = ['referencia', 'nombre', 'categoria', 'stock', 'id_situacion_tabla']

@busqueda_bp.route('/busqueda')
def busqueda():
    busqueda = request.args.get('busqueda', '').strip()
    campo = request.args.get('campo', 'referencia')
    orden = request.args.get('orden', 'asc')

    columnas = VISTAS['busqueda']['columnas']
    nombres_columnas = obtener_nombres_columnas('busqueda')
    datos = []

    # Quita 'ubicacion' de la consulta SQL porque se construye en Python
    columnas_sql = [col for col in columnas if col != 'ubicacion']
    # Añade los campos necesarios para construir 'ubicacion'
    for campo_extra in ['almacen', 'estanteria', 'lado', 'columna', 'altura']:
        if campo_extra not in columnas_sql:
            columnas_sql.append(campo_extra)

    if busqueda:
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        if campo not in campos_busqueda_permitidos:
            campo = 'referencia'
        query = f"""
            SELECT i.referencia, i.nombre, i.categoria, i.stock, i.id_situacion_tabla,
                   s.almacen, s.estanteria, s.lado, s.columna, s.altura
            FROM inventario_tabla i
            LEFT JOIN situacion_tabla s ON i.id_situacion_tabla = s.id_situacion_tabla
            WHERE i.{campo} LIKE %s
            ORDER BY i.{campo} {orden}
        """
        cursor.execute(query, (f"%{busqueda}%",))
        datos = cursor.fetchall()
        cursor.close()
        conn.close()

        # Construye la columna 'ubicacion' para cada fila
        for fila in datos:
            almacen = fila.get('almacen', '')
            estanteria = fila.get('estanteria', '')
            lado = fila.get('lado', '')
            columna_val = fila.get('columna', '')
            altura = fila.get('altura', '')
            fila['ubicacion'] = f"{almacen}-{estanteria}-{lado}-{columna_val}-{altura}"

    return render_template(
        'busqueda.html',
        columnas=columnas,
        nombres_columnas=nombres_columnas,
        datos=datos,
        busqueda=busqueda,
        campo=campo,
        orden=orden
    )