from flask import Blueprint, render_template, request
from routes.roles import puede_eliminar_movimientos
from routes.configuracion import cargar_configuracion
import database as db

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def bienvenido():
    config = cargar_configuracion()
    return render_template('bienvenido.html', config=config)

@home_bp.route('/menu')
def menu():
    config = cargar_configuracion()
    return render_template('menu.html', config=config)

@home_bp.route('/perfiles')
def perfiles():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM perfiles")
    perfiles = cursor.fetchall()
    insertObjects = []
    columnNames = [column[0] for column in cursor.description]
    for fila in perfiles:
        insertObjects.append(dict(zip(columnNames, fila)))
    cursor.close()
    config = cargar_configuracion()
    return render_template('perfiles.html', perfiles=insertObjects, config=config)

@home_bp.route('/busqueda')
def busqueda():
    busqueda = request.args.get('busqueda', '')
    campo = request.args.get('campo', 'referencia')
    orden = request.args.get('orden', 'asc').lower()

    repuestos = []
    columnas = []
    campos_validos = ['referencia', 'nombre', 'categoria', 'almacen']
    if campo not in campos_validos:
        campo = 'referencia'
    if orden not in ['asc', 'desc']:
        orden = 'asc'

    if busqueda == '*':
        query = f"SELECT * FROM inventario_tabla ORDER BY {campo} {orden.upper()}"
        params = ()
    elif busqueda:
        query = f"SELECT * FROM inventario_tabla WHERE {campo} LIKE %s ORDER BY {campo} {orden.upper()}"
        params = (f"%{busqueda}%",)
    else:
        query = None

    if query:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        columnas = [column[0] for column in cursor.description]
        if campo in columnas:
            columnas = [campo] + [col for col in columnas if col != campo]
        for fila in resultados:
            repuestos.append(
                dict(zip(columnas, [fila[columnas.index(col)] for col in columnas])))
        cursor.close()

    config = cargar_configuracion()
    return render_template('busqueda.html', repuestos=repuestos, busqueda=busqueda, campo=campo, columnas=columnas, orden=orden, config=config)

@home_bp.route('/repuestos')
def repuestos():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventario_tabla")
    repuestos = cursor.fetchall()
    columnNames = [column[0] for column in cursor.description]
    insertObjects = []
    for fila in repuestos:
        insertObjects.append(dict(zip(columnNames, fila)))
    cursor.close()
    config = cargar_configuracion()
    return render_template('repuestos.html', repuestos=insertObjects, columnas=columnNames, config=config)

@home_bp.route('/movimientos')
def movimientos():
    conn = db.get_connection()

    if conn is None:
        print("¡Error: No se pudo conectar a la base de datos!")
        return render_template('movimientos.html', movimientos=[], inventario=[], operadores=[], mensaje_error="No se pudo conectar a la base de datos. Por favor, verifica la conexión.")

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nombre, stock FROM inventario_tabla")
    piezas = cursor.fetchall()
    cursor.execute(
        "SELECT referencia, nombre FROM inventario_tabla ORDER BY nombre ASC")
    inventario = cursor.fetchall()
    cursor.execute("SELECT * FROM movimientos_tabla")
    movimientos = cursor.fetchall()
    cursor.execute("SELECT perfil FROM perfiles")
    perfiles = cursor.fetchall()
    cursor.close()
    conn.close()
    config = cargar_configuracion()
    return render_template(
        'movimientos.html',
        piezas=piezas,
        inventario=inventario,
        movimientos=movimientos,
        perfiles=perfiles,
        puede_eliminar_movimientos=puede_eliminar_movimientos,
        config=config
    )