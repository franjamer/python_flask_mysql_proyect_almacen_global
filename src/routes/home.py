from flask import Blueprint, render_template, request
import database as db

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def bienvenido():
    return render_template('bienvenido.html')

@home_bp.route('/menu')
def menu():
    return render_template('menu.html')

@home_bp.route('/usuarios')
def usuarios():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    insertObjects = []
    columnNames = [column[0] for column in cursor.description]
    for fila in usuarios:
        insertObjects.append(dict(zip(columnNames, fila)))
    cursor.close()
    return render_template('usuarios.html', users=insertObjects)

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
            repuestos.append(dict(zip(columnas, [fila[columnas.index(col)] for col in columnas])))
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
    cursor = conn.cursor()
    # Obtener piezas
    cursor.execute("SELECT nombre, stock FROM inventario_tabla")
    piezas = cursor.fetchall()
    piezas = [dict(zip([column[0] for column in cursor.description], fila)) for fila in piezas]
    # Obtener movimientos
    cursor.execute("SELECT * FROM movimientos_tabla")
    movimientos_data = cursor.fetchall()
    movimientos_cols = [column[0] for column in cursor.description]
    movimientos = [dict(zip(movimientos_cols, fila)) for fila in movimientos_data]
    # Obtener usuarios
    cursor.execute("SELECT codigo_operador FROM usuarios")
    usuarios_data = cursor.fetchall()
    usuarios = [dict(zip([column[0] for column in cursor.description], fila)) for fila in usuarios_data]
    cursor.close()
    conn.close()
    return render_template('movimientos.html', piezas=piezas, movimientos=movimientos, usuarios=usuarios)

