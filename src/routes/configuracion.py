from flask import Blueprint, render_template, request, redirect, url_for, flash
import json
import os

configuracion_bp = Blueprint('configuracion_bp', __name__)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../configuracion.json')
# Define las vistas y los campos configurables de cada una
VISTAS_CONFIG = {
    "inventario": [
        "referencia", "nombre", "categoria", "subcategoria",
        "caracteristicas_medidas", "fotos_planos", "empaquetado",
        "stock", "stock_minimo", "stock_maximo", "id_situacion_tabla"
    ],
    "busqueda": [
        "referencia", "nombre", "categoria", "almacen", "stock"
    ],
    "pedidos": [
        "id_pedido", "fecha", "referencia", "cantidad", "estado", "proveedor"
    ],
    "movimientos": [
        "id_movimiento", "fecha", "referencia", "cantidad", "tipo", "operador"
    ],
    "operadores": [
        "id_operador", "nombre", "perfil", "activo"
    ],
    "perfiles": [
        "id_perfil", "perfil", "descripcion"
    ],
    "situacion": [
        "id_situacion_tabla", "almacen", "estanteria", "lado", "columna", "altura"
    ],
    "mapa_interactivo": [
        "almacen", "estanteria", "lado", "columna", "altura"
    ],
    "menu": ["titulo_principal", "titulo_secundario", "central"]
}

def cargar_configuracion():
    import os, json
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../configuracion.json')
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {}
    if 'textos_menu' not in config:
        config['textos_menu'] = {}
    for campo in ["titulo_principal", "titulo_secundario", "central"]:
        if campo not in config['textos_menu']:
            if campo == "titulo_principal":
                config['textos_menu'][campo] = "Bienvenido al sistema"
            elif campo == "titulo_secundario":
                config['textos_menu'][campo] = "Gestión de almacén"
            else:
                config['textos_menu'][campo] = "Bienvenido al sistema de gestión"
    if 'nombres_columnas' not in config:
        config['nombres_columnas'] = {}
    # Añade todos los campos de todas las vistas si faltan
    for campos in VISTAS_CONFIG.values():
        for campo in campos:
            if campo not in config['nombres_columnas']:
                config['nombres_columnas'][campo] = campo.replace('_', ' ').capitalize()
    if 'nombres_vistas' not in config:
        config['nombres_vistas'] = {k: k.replace('_', ' ').capitalize() for k in VISTAS_CONFIG.keys()}
    return config

def guardar_configuracion(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

@configuracion_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    config = cargar_configuracion()
    vista = request.args.get('vista', 'inventario')
    campos = VISTAS_CONFIG.get(vista, [])
    if request.method == 'POST':
        # Actualiza la configuración con los datos del formulario
        config['nombres_columnas'] = request.form.get('nombres_columnas', type=dict) or config.get('nombres_columnas', {})
        config['nombres_vistas'] = request.form.get('nombres_vistas', type=dict) or config.get('nombres_vistas', {})
        config['textos_menu'] = request.form.get('textos_menu', type=dict) or config.get('textos_menu', {})
        # Alternativamente, puedes procesar cada campo individualmente si no usas JS para enviar el dict
        for campo in campos:
            config['nombres_columnas'][campo] = request.form.get(f'nombre_columna_{campo}', campo)
        for vista_nombre in ['inventario', 'busqueda', 'mapa_interactivo']:
            config['nombres_vistas'][vista_nombre] = request.form.get(f'nombre_vista_{vista_nombre}', vista_nombre)
        if 'central' in VISTAS_CONFIG.get(vista, []):
            config['textos_menu']['central'] = request.form.get('texto_menu_central', config['textos_menu'].get('central', ''))
        if vista == "menu":
            for campo in ["titulo_principal", "titulo_secundario", "central"]:
                config['textos_menu'][campo] = request.form.get(f'texto_menu_{campo}', config['textos_menu'].get(campo, ''))
        guardar_configuracion(config)
        flash('Configuración guardada correctamente.', 'success')
        return redirect(url_for('configuracion_bp.configuracion', vista=vista))
    return render_template('configuracion.html', config=config, vista=vista, campos=campos, vistas=VISTAS_CONFIG)