from flask import Blueprint, render_template, request,session, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import json
import os
import time
from utils.data_admin import export_tables, save_export_to_file, import_data, delete_tables_data, TABLAS_PERMITIDAS

configuracion_bp = Blueprint('configuracion_bp', __name__)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../configuracion.json')
# Cambia aquí el nombre de la carpeta si quieres 'personal_config'
PERSONAL_CONFIG_DIR = os.path.join(os.path.dirname(__file__), '../../personal_config')
if not os.path.exists(PERSONAL_CONFIG_DIR):
    os.makedirs(PERSONAL_CONFIG_DIR)

# Define las vistas y los campos configurables de cada una
VISTAS_CONFIG = {
    "inventario": [
        "referencia", "nombre", "categoria", "subcategoria",
        "caracteristicas_medidas", "fotos_planos", "empaquetado",
        "stock", "stock_minimo", "stock_maximo", "id_situacion_tabla"
    ],
    "busqueda": [
        "referencia", "nombre", "categoria", "almacen", "stock","ubicacion","id_situacion_tabla"
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
    "menu": ["central", "titulo_principal", "titulo_secundario"]
}

def cargar_configuracion():
    import os, json
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../configuracion.json')
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {}
    if 'nombres_columnas' not in config:
        config['nombres_columnas'] = {}
    # Añade todos los campos de todas las vistas si faltan
    for campos in VISTAS_CONFIG.values():
        for campo in campos:
            if campo not in config['nombres_columnas']:
                config['nombres_columnas'][campo] = campo.replace('_', ' ').capitalize()
    if 'textos_menu' not in config:
        config['textos_menu'] = {"central": "Bienvenido al sistema de gestión","titulo_principal": "Bienvenido al sistema de gestión","titulo_secundario": "Menú Principal"}

    if 'nombres_vistas' not in config:
        config['nombres_vistas'] = {
            'busqueda': 'Búsqueda de repuestos',
            'inventario': 'Inventario',
            'movimientos': 'Movimientos',
            # ... otras vistas
        }
    return config

def guardar_configuracion(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def listar_archivos_config():
    return [f for f in os.listdir(PERSONAL_CONFIG_DIR) if f.endswith('.json')]

@configuracion_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    # Permitir acceso si perfil == 'Admin' o rol == 'admin'
    if not (session.get('perfil') == 'Admin' or session.get('rol') == 'admin'):
        flash('Acceso denegado: solo el perfil Admin puede acceder a configuración.', 'error')
        return redirect(url_for('home_bp.menu'))

    config = cargar_configuracion()
    # read 'vista' from POST or GET (request.values covers both)
    vista = request.values.get('vista', 'inventario')
    campos = VISTAS_CONFIG.get(vista, [])
    archivos_config = listar_archivos_config()

    if request.method == 'POST':
        accion = request.form.get('accion')
        archivo = request.form.get('archivo_config')
        nombre_guardar = request.form.get('nombre_guardar', '').strip()

        # Normalize and save estilo_menu fields when present so both forms update the same config
        if accion in ('guardar_estilo', 'guardar_ui', 'guardar_todo'):
            if 'estilo_menu' not in config:
                config['estilo_menu'] = {}
            # support per-text styling for titulo_principal, central, titulo_secundario
            for key in ('titulo_principal', 'central', 'titulo_secundario'):
                prefix = key
                # gather fields if present
                color = request.form.get(f'{prefix}_color')
                bg = request.form.get(f'{prefix}_bg')
                size = request.form.get(f'{prefix}_size')
                valign = request.form.get(f'{prefix}_valign')
                halign = request.form.get(f'{prefix}_halign')
                # only set sub-dict if any of these present
                if any((color, bg, size, valign, halign)):
                    if key not in config['estilo_menu'] or not isinstance(config['estilo_menu'][key], dict):
                        config['estilo_menu'][key] = {}
                    if color is not None:
                        config['estilo_menu'][key]['color'] = color
                    if bg is not None:
                        config['estilo_menu'][key]['bg'] = bg
                    if size is not None and size != '':
                        config['estilo_menu'][key]['size'] = size
                    if valign is not None:
                        config['estilo_menu'][key]['valign'] = valign
                    if halign is not None:
                        config['estilo_menu'][key]['halign'] = halign
            # marca_agua handling: save uploaded file to static/marca_agua
            archivo_marca = None
            if 'marca_agua_menu' in request.files:
                archivo_m = request.files.get('marca_agua_menu')
                if archivo_m and archivo_m.filename:
                    # ensure dir exists
                    marca_dir = os.path.join(os.path.dirname(__file__), '../../static/marca_agua')
                    if not os.path.exists(marca_dir):
                        os.makedirs(marca_dir)
                    fname = secure_filename(archivo_m.filename)
                    # prefix with timestamp to avoid collisions
                    fname_final = f"{int(time.time())}_{fname}"
                    ruta_m = os.path.join(marca_dir, fname_final)
                    try:
                        archivo_m.save(ruta_m)
                        config['estilo_menu']['marca_agua_menu'] = fname_final
                    except Exception:
                        flash('Error guardando la imagen de marca de agua.', 'error')
            archivo_marca = config['estilo_menu'].get('marca_agua_menu')
            # If the action is guardar_estilo we save immediately and return
            if accion == 'guardar_estilo':
                guardar_configuracion(config)
                flash('Estilo del menú guardado correctamente.', 'success')
                return redirect(url_for('configuracion_bp.configuracion', vista=vista))

        # Setup / Reset: exportar, importar y eliminar registros (usa helpers)
        if accion in ('export_registros', 'import_registros', 'eliminar_registros'):
            # Exportar
            if accion == 'export_registros':
                tablas = request.form.getlist('tables') or request.form.getlist('tables[]')
                if not tablas:
                    flash('No se seleccionaron tablas para exportar.', 'error')
                    return redirect(url_for('configuracion_bp.configuracion', vista=vista))
                # conectar y exportar
                import database as db
                conn = db.get_connection()
                if conn is None:
                    flash('No se pudo conectar a la base de datos para exportar.', 'error')
                    return redirect(url_for('configuracion_bp.configuracion', vista=vista))
                resultado = export_tables(conn, tablas)
                conn.close()
                # allow custom filename from form
                custom_name = request.form.get('export_filename', '').strip()
                nombre, ruta = save_export_to_file(resultado, PERSONAL_CONFIG_DIR, filename=custom_name or None, suffix='registros')
                flash(f'Exportación guardada: {nombre}', 'success')
                return redirect(url_for('configuracion_bp.configuracion', vista=vista))

            # Importar
            if accion == 'import_registros':
                import_file = request.files.get('import_file')
                replace = request.form.get('replace') in ('1', 'on', 'true')
                if not import_file:
                    flash('No se ha subido ningún fichero para importar.', 'error')
                    return redirect(url_for('configuracion_bp.configuracion', vista=vista))
                try:
                    data = json.load(import_file)
                except Exception as e:
                    flash(f'Error leyendo JSON: {e}', 'error')
                    return redirect(url_for('configuracion_bp.configuracion', vista=vista))
                import database as db
                conn = db.get_connection()
                if conn is None:
                    flash('No se pudo conectar a la base de datos para importar.', 'error')
                    return redirect(url_for('configuracion_bp.configuracion', vista=vista))
                try:
                    import_data(conn, data, replace=replace)
                    flash('Importación completada.', 'success')
                except Exception as e:
                    flash(f'Error durante la importación: {e}', 'error')
                finally:
                    conn.close()
                return redirect(url_for('configuracion_bp.configuracion', vista=vista))

            # Eliminar registros
            if accion == 'eliminar_registros':
                tablas = request.form.getlist('tables') or request.form.getlist('tables[]')
                if not tablas:
                    flash('No se seleccionaron tablas para eliminar.', 'error')
                    return redirect(url_for('configuracion_bp.configuracion', vista=vista))
                import database as db
                conn = db.get_connection()
                if conn is None:
                    flash('No se pudo conectar a la base de datos para eliminar registros.', 'error')
                    return redirect(url_for('configuracion_bp.configuracion', vista=vista))
                try:
                    # automatic backup before delete
                    backup = export_tables(conn, tablas)
                    nombre_backup, _ = save_export_to_file(backup, PERSONAL_CONFIG_DIR, prefix='backup_before_delete', suffix='registros')
                    delete_tables_data(conn, tablas)
                    flash(f'Registros eliminados correctamente. Backup: {nombre_backup}', 'success')
                except Exception as e:
                    flash(f'Error al eliminar registros: {e}', 'error')
                finally:
                    conn.close()
                return redirect(url_for('configuracion_bp.configuracion', vista=vista))

        # download exported file
        if request.form.get('accion_descargar'):
            filename = request.form.get('file_name')
            # security: ensure file in personal dir
            if not filename or '..' in filename:
                flash('Nombre de archivo no válido.', 'error')
                return redirect(url_for('configuracion_bp.configuracion', vista=vista))
            return redirect(url_for('configuracion_bp.download_export', filename=filename))

        # Guardar toda la configuración en un archivo nuevo
        if accion == 'guardar_todo':
            # --- AÑADE AQUÍ LA LECTURA DE LOS CAMPOS DE ESTILO ANTES DE GUARDAR ---
            if 'estilo_menu' not in config:
                config['estilo_menu'] = {}
            config['estilo_menu']['color_texto_menu'] = request.form.get('color_texto_menu', config['estilo_menu'].get('color_texto_menu', '#fb0000'))
            config['estilo_menu']['color_fondo_menu'] = request.form.get('color_fondo_menu', config['estilo_menu'].get('color_fondo_menu', '#eeb6bb'))
            config['estilo_menu']['tamano_texto_menu'] = request.form.get('tamano_texto_menu', config['estilo_menu'].get('tamano_texto_menu', '48'))
            # Si tienes imagen de marca de agua, añade aquí la lógica para guardarla

            # determine suffix based on vista
            if vista == 'menu':
                suf = 'main-menu'
            else:
                suf = 'campos'
            # use save_export_to_file to get consistent filename behavior
            nombre, ruta = save_export_to_file(config, PERSONAL_CONFIG_DIR, prefix='config', filename=nombre_guardar or None, suffix=suf)
            flash(f'Configuración guardada como {nombre}.', 'success')
            return redirect(url_for('configuracion_bp.configuracion', vista=vista))
        # Cargar configuración desde archivo
        elif accion == 'cargar' and archivo:
            ruta = os.path.join(PERSONAL_CONFIG_DIR, archivo)
            with open(ruta, 'r', encoding='utf-8') as f:
                nueva_config = json.load(f)
            guardar_configuracion(nueva_config)
            flash('Configuración cargada correctamente.', 'success')
            return redirect(url_for('configuracion_bp.configuracion', vista=vista))
        # Eliminar archivo de configuración
        elif accion == 'eliminar' and archivo:
            ruta = os.path.join(PERSONAL_CONFIG_DIR, archivo)
            if os.path.exists(ruta):
                os.remove(ruta)
                flash('Archivo eliminado.', 'success')
            return redirect(url_for('configuracion_bp.configuracion', vista=vista))
        # Actualiza la configuración con los datos del formulario
        config['nombres_columnas'] = request.form.get('nombres_columnas', type=dict) or config.get('nombres_columnas', {})
        config['nombres_vistas'] = request.form.get('nombres_vistas', type=dict) or config.get('nombres_vistas', {})
        config['textos_menu'] = request.form.get('textos_menu', type=dict) or config.get('textos_menu', {})
        # Procesar campos individuales cuando no se envía un dict
        for campo in campos:
            config['nombres_columnas'][campo] = request.form.get(f'nombre_columna_{campo}', campo)
        for vista_nombre in ['inventario', 'busqueda', 'mapa_interactivo']:
            config['nombres_vistas'][vista_nombre] = request.form.get(f'nombre_vista_{vista_nombre}', vista_nombre)
        # Campos de texto del menú principal
        config['textos_menu']['titulo_principal'] = request.form.get('texto_menu_titulo_principal', config['textos_menu'].get('titulo_principal', ''))
        config['textos_menu']['titulo_secundario'] = request.form.get('texto_menu_titulo_secundario', config['textos_menu'].get('titulo_secundario', ''))
        if 'central' in VISTAS_CONFIG.get(vista, []):
            config['textos_menu']['central'] = request.form.get('texto_menu_central', config['textos_menu'].get('central', ''))
        guardar_configuracion(config)
        flash('Configuración guardada correctamente.', 'success')
        return redirect(url_for('configuracion_bp.configuracion', vista=vista))
    return render_template(
        'configuracion.html',
        config=config,
        vista=vista,
        campos=campos,
        vistas=VISTAS_CONFIG,
        archivos_config=archivos_config
    )


@configuracion_bp.route('/configuracion/download/<path:filename>')
def download_export(filename):
    if not (session.get('perfil') == 'Admin' or session.get('rol') == 'admin'):
        flash('Acceso denegado.', 'error')
        return redirect(url_for('home_bp.menu'))
    # security: ensure filename safe
    if not filename or '..' in filename:
        flash('Nombre de archivo no válido.', 'error')
        return redirect(url_for('configuracion_bp.configuracion'))
    return send_from_directory(PERSONAL_CONFIG_DIR, filename, as_attachment=True)