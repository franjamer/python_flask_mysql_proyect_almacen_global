from flask import Blueprint, render_template, request
from routes.roles import puede_eliminar_movimientos
import database as db

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/')
def bienvenido():
    return render_template('bienvenido.html')


@home_bp.route('/menu')
def menu():
    return render_template('menu.html')


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
    return render_template('perfiles.html', perfiles=insertObjects)


@home_bp.route('/operadores')
def operadores():
    conn = db.get_connection()
    print("Conectando a la base de datos para obtener operadores desde home.py version aplicacion con IA")
    cursor = conn.cursor()
    consulta_select = """SELECT * FROM operadores"""
    cursor.execute(consulta_select)
    operadores = cursor.fetchall()
    insertObjets = []
    columnNames = [column[0] for column in cursor.description]
    for fila in operadores:
        operadores.append(dict(zip(columnNames, fila)))
    cursor.close()
    conn.close()
    return render_template('operadores.html', operadores=operadores)


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

    return render_template('busqueda.html', repuestos=repuestos, busqueda=busqueda, campo=campo, columnas=columnas, orden=orden)


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
    return render_template('repuestos.html', repuestos=insertObjects, columnas=columnNames)


@home_bp.route('/movimientos')
def movimientos():
    conn = db.get_connection()

    # 🎯 Añade esta verificación de seguridad
    if conn is None:
        # Si la conexión falla, devolvemos un error.
        # Esto evita que el programa falle con un AttributeError.
        # Puedes mostrar un mensaje de error en la plantilla o redirigir.
        print("¡Error: No se pudo conectar a la base de datos!")
        # Opcional: Redirigir a una página de error o al menú
        # return redirect(url_for('home_bp.menu'))
        # Opcional: Renderizar la plantilla con un mensaje de error
        return render_template('movimientos.html', movimientos=[], inventario=[], operadores=[], mensaje_error="No se pudo conectar a la base de datos. Por favor, verifica la conexión.")

    # Si la conexión es exitosa, continúa con el resto del código
    cursor = conn.cursor(dictionary=True)

    # Obtener piezas
    cursor.execute("SELECT nombre, stock FROM inventario_tabla")
    piezas = cursor.fetchall()
    # Obtener inventario para el select
    cursor.execute(
        "SELECT referencia, nombre FROM inventario_tabla ORDER BY nombre ASC")
    inventario = cursor.fetchall()
    # Obtener movimientos
    cursor.execute("SELECT * FROM movimientos_tabla")
    movimientos = cursor.fetchall()
    # Obtener perfiles
    cursor.execute("SELECT perfil FROM perfiles")
    perfiles = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        'movimientos.html',
        piezas=piezas,
        inventario=inventario,  # <-- Añade esto
        movimientos=movimientos,
        perfiles=perfiles,
        puede_eliminar_movimientos=puede_eliminar_movimientos
    )
