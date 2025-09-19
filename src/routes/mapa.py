from flask import Blueprint, render_template, request, jsonify
import database as db
mapa_bp = Blueprint('mapa_bp', __name__)

@mapa_bp.route('/mapa')
def mapa_interactivo():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT DISTINCT almacen FROM situacion_tabla ORDER BY almacen")
    almacenes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('mapa_interactivo.html', almacenes=almacenes)

@mapa_bp.route('/mapa/estanterias')
def obtener_estanterias():
    almacen = request.args.get('almacen')
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT DISTINCT estanteria FROM situacion_tabla WHERE almacen = %s ORDER BY estanteria", (almacen,))
    estanterias = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(estanterias)

@mapa_bp.route('/mapa/lados')
def obtener_lados():
    almacen = request.args.get('almacen')
    estanteria = request.args.get('estanteria')
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT DISTINCT lado FROM situacion_tabla WHERE almacen = %s AND estanteria = %s", (almacen, estanteria))
    lados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(lados)

@mapa_bp.route('/mapa/posiciones')
def obtener_posiciones():
    almacen = request.args.get('almacen')
    estanteria = request.args.get('estanteria')
    lado = request.args.get('lado')
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT columna, altura
        FROM situacion_tabla
        WHERE almacen = %s AND estanteria = %s AND lado = %s
        ORDER BY columna, altura
    """, (almacen, estanteria, lado))
    posiciones = cursor.fetchall()

    # Para cada posición, busca los repuestos en inventario_tabla usando la columna compuesta
    for p in posiciones:
        ubicacion = f"{almacen}-{estanteria}-{lado}-{p['columna']}-{p['altura']}"
        cursor2 = conn.cursor(dictionary=True)
        cursor2.execute("""
            SELECT referencia, nombre
            FROM inventario_tabla
            WHERE id_situacion_tabla = %s
        """, (p['id_situacion_tabla'],))
        repuestos = cursor2.fetchall()
        p['repuestos'] = repuestos
        cursor2.close()
    conn.close()
    return jsonify(posiciones)

@mapa_bp.route('/mapa/repuestos')
def obtener_repuestos():
    almacen = request.args.get('almacen')
    estanteria = request.args.get('estanteria')
    lado = request.args.get('lado')
    columna = request.args.get('columna')
    altura = request.args.get('altura')
    ubicacion = f"{almacen}-{estanteria}-{lado}-{columna}-{altura}"
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT referencia, nombre
        FROM inventario_tabla
        WHERE ubicacion = %s
    """, (ubicacion,))
    repuestos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(repuestos)
@mapa_bp.route('/mapa/columnas')
def obtener_columnas():
    almacen = request.args.get('almacen')
    estanteria = request.args.get('estanteria')
    lado = request.args.get('lado')
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT columna
        FROM situacion_tabla
        WHERE almacen = %s AND estanteria = %s AND lado = %s
        ORDER BY columna
    """, (almacen, estanteria, lado))
    columnas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(columnas)

@mapa_bp.route('/mapa/alturas')
def obtener_alturas():
    almacen = request.args.get('almacen')
    estanteria = request.args.get('estanteria')
    lado = request.args.get('lado')
    columna = request.args.get('columna')
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT altura, id_situacion_tabla
        FROM situacion_tabla
        WHERE almacen = %s AND estanteria = %s AND lado = %s AND columna = %s
        ORDER BY altura
    """, (almacen, estanteria, lado, columna))
    alturas = cursor.fetchall()
    for a in alturas:
        cursor2 = conn.cursor(dictionary=True)
        cursor2.execute("""
            SELECT referencia, nombre
            FROM inventario_tabla
            WHERE id_situacion_tabla = %s
        """, (a['id_situacion_tabla'],))
        a['repuestos'] = cursor2.fetchall()
        cursor2.close()
    cursor.close()
    conn.close()
    return jsonify(alturas)