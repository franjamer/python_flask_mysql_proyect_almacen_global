# Inportación de las dependencias y variables necesarias
from flask import Blueprint, render_template, request, redirect, url_for, session
from .pedidos_detalle import validar_pedido, obtener_nombre_articulo
from .pedidos_db import (
    obtener_inventario, obtener_pedidos, obtener_lineas_pedido,
    insertar_pedido, actualizar_linea_pedido, eliminar_pedido,
    eliminar_linea, modificar_pedido, obtener_pedido_cabecera  
)
from routes.roles import puede_crud_pedidos, puede_eliminar_pedidos
from .vistas_config import VISTAS
from .configuracion_general import obtener_nombres_columnas

pedidos_bp = Blueprint('pedidos_bp', __name__)

@pedidos_bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    mensaje_error = None
    columnas = VISTAS['pedidos']['columnas']
    nombres_columnas = VISTAS['pedidos']['nombres_columnas']
    nombre_vista = "Pedidos"  # Puedes parametrizarlo si lo tienes en config

    if request.method == 'POST':
        if not puede_crud_pedidos(session.get('rol')):
            return redirect(url_for('pedidos_bp.pedidos'))
        mensaje_error = validar_pedido(request.form)
        if not mensaje_error:
            referencia_pedido = request.form['referencia_pedido']
            fecha_creacion = request.form['fecha_creacion']
            referencias = request.form.getlist('referencia_articulo[]')
            cantidades_pedidas = request.form.getlist('cantidad_pedida[]')
            cantidades_recibidas = request.form.getlist('cantidad_recibida[]')
            fechas_recibido = request.form.getlist('fecha_recibido[]')
            lineas = zip(referencias, cantidades_pedidas, cantidades_recibidas, fechas_recibido)
            insertar_pedido(referencia_pedido, fecha_creacion, lineas, obtener_nombre_articulo)

    inventario = obtener_inventario()
    pedidos = obtener_pedidos(columnas)
    pedido_id = request.args.get('pedido_id')
    lineas = []
    if pedido_id:
        lineas = obtener_lineas_pedido(pedido_id)

    nombres_columnas_lineas = VISTAS['lineas_pedido']['nombres_columnas']

    return render_template(
        'pedidos.html',
        pedidos=pedidos,
        inventario=inventario,
        lineas=lineas,
        mensaje_error=mensaje_error,
        puede_crud_pedidos=puede_crud_pedidos,
        puede_eliminar_pedidos=puede_eliminar_pedidos,
        columnas=columnas,
        nombres_columnas=nombres_columnas,
        nombre_vista=nombre_vista,
        nombres_columnas_lineas=nombres_columnas_lineas
    )

@pedidos_bp.route('/actualizar_linea/<int:linea_id>', methods=['POST'])
def actualizar_linea(linea_id):
    if not puede_crud_pedidos(session.get('rol')):
        return redirect(url_for('pedidos_bp.pedidos'))
    cantidad_pedida = int(request.form['cantidad_pedida'])
    cantidad_recibida = int(request.form['cantidad_recibida'])
    fecha_recibido = request.form.get('fecha_recibido')
    pedido_id_db = actualizar_linea_pedido(linea_id, cantidad_pedida, cantidad_recibida, fecha_recibido)
    return redirect(url_for('pedidos_bp.pedidos', pedido_id=pedido_id_db))

@pedidos_bp.route('/eliminar_pedido/<int:pedido_id>', methods=['POST'])
def eliminar_pedido_route(pedido_id):
    if not puede_eliminar_pedidos(session.get('rol')):
        return redirect(url_for('pedidos_bp.pedidos'))
    eliminar_pedido(pedido_id)
    return redirect(url_for('pedidos_bp.pedidos'))

@pedidos_bp.route('/eliminar_linea/<int:linea_id>', methods=['POST'])
def eliminar_linea_route(linea_id):
    if not puede_eliminar_pedidos(session.get('rol')):
        return redirect(url_for('pedidos_bp.pedidos'))
    pedido_id_db = eliminar_linea(linea_id)
    return redirect(url_for('pedidos_bp.pedidos', pedido_id=pedido_id_db) if pedido_id_db else url_for('pedidos_bp.pedidos'))

@pedidos_bp.route('/modificar_pedido/<int:pedido_id>', methods=['GET', 'POST'])
def modificar_pedido_route(pedido_id):
    if not puede_crud_pedidos(session.get('rol')):
        return redirect(url_for('pedidos_bp.pedidos'))
    mensaje_error = None
    if request.method == 'POST':
        mensaje_error = validar_pedido(request.form)
        if not mensaje_error:
            referencia_pedido = request.form['referencia_pedido']
            fecha_creacion = request.form['fecha_creacion']
            referencias = request.form.getlist('referencia_articulo[]')
            cantidades_pedidas = request.form.getlist('cantidad_pedida[]')
            cantidades_recibidas = request.form.getlist('cantidad_recibida[]')
            fechas_recibido = request.form.getlist('fecha_recibido[]')
            lineas = zip(referencias, cantidades_pedidas, cantidades_recibidas, fechas_recibido)
            modificar_pedido(pedido_id, referencia_pedido, fecha_creacion, lineas, obtener_nombre_articulo)
            return redirect(url_for('pedidos_bp.pedidos', pedido_id=pedido_id))

    pedido = obtener_pedido_cabecera(pedido_id)
    lineas = obtener_lineas_pedido(pedido_id)
    inventario = obtener_inventario()
    nombres_columnas_lineas = VISTAS['lineas_pedido']['nombres_columnas']
    return render_template(
        'pedidos/modificar_pedido.html',
        pedido_id=pedido_id,
        pedido=pedido,
        lineas=lineas,
        inventario=inventario,
        mensaje_error=mensaje_error,
        nombres_columnas=obtener_nombres_columnas('pedidos'),
        nombres_columnas_lineas=nombres_columnas_lineas 
    )
