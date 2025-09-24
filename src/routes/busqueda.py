from flask import Blueprint, render_template, request
from routes.configuracion import cargar_configuracion
import database as db

busqueda_bp = Blueprint('busqueda_bp', __name__)

campos_busqueda_permitidos = ['referencia', 'nombre', 'categoria', 'stock', 'id_situacion_tabla']

@busqueda_bp.route('/busqueda')
def busqueda():
    busqueda = request.args.get('busqueda', '').strip()
    campo = request.args.get('campo', 'referencia')
    orden = request.args.get('orden', 'asc')
    config = cargar_configuracion()

    columnas = config.get('columnas_busqueda', ['referencia', 'nombre', 'categoria', 'stock', 'ubicacion'])
    datos = []

    # Quita 'ubicacion' de la consulta SQL porque se construye en Python
    columnas_sql = [col for col in columnas if col != 'ubicacion']
    # Añade los campos necesarios para construir 'ubicacion'
    for campo in ['almacen', 'estanteria', 'lado', 'columna', 'altura']:
        if campo not in columnas_sql:
            columnas_sql.append(campo)

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
        datos=datos,
        config=config
    )