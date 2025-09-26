from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .configuracion_utils import VISTAS_CONFIG
from .configuracion_carga import cargar_configuracion, guardar_configuracion, listar_archivos_config

configuracion_bp = Blueprint('configuracion_bp', __name__)

@configuracion_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    if session.get('perfil') != 'Admin':
        flash('Acceso denegado: solo el perfil Admin puede acceder a configuración.', 'error')
        return redirect(url_for('home_bp.menu'))

    config = cargar_configuracion()
    vista = request.args.get('vista', 'inventario')
    campos = VISTAS_CONFIG.get(vista, [])
    archivos_config = listar_archivos_config()

    if request.method == 'POST':
        accion = request.form.get('accion')
        archivo = request.form.get('archivo_config')
        nombre_guardar = request.form.get('nombre_guardar', '').strip()

        # --- Lógica para aplicar estilos ---
        if accion == 'aplicar_local':
            vista_local = request.form.get('vista_local')
            if 'estilos_vistas' not in config:
                config['estilos_vistas'] = {}
            config['estilos_vistas'][vista_local] = {
                'color_texto_menu': request.form.get('color_texto_menu'),
                'color_fondo_menu': request.form.get('color_fondo_menu'),
                'tamano_texto_menu': request.form.get('tamano_texto_menu'),
                'estilo_texto_menu': request.form.get('estilo_texto_menu')
            }
            guardar_configuracion(config)
            flash(f'Estilo aplicado a la vista {vista_local}.', 'success')
            return redirect(url_for('configuracion_bp.configuracion', vista=vista_local))

        if accion == 'aplicar_global':
            parametro = request.form.get('parametro_global')
            if 'estilo_menu' not in config:
                config['estilo_menu'] = {}
            if parametro == 'todo':
                config['estilo_menu'] = {
                    'color_texto_menu': request.form.get('color_texto_menu'),
                    'color_fondo_menu': request.form.get('color_fondo_menu'),
                    'tamano_texto_menu': request.form.get('tamano_texto_menu'),
                    'estilo_texto_menu': request.form.get('estilo_texto_menu')
                }
            else:
                config['estilo_menu'][parametro] = request.form.get(parametro)
            guardar_configuracion(config)
            flash('Estilo global actualizado.', 'success')
            return redirect(url_for('configuracion_bp.configuracion', vista=vista))
        # --- Fin lógica estilos ---

        # ...aquí va la lógica de guardar_todo, cargar, eliminar, etc...
        # Puedes importar funciones auxiliares si lo prefieres

        # Ejemplo para guardar_todo:
        if accion == 'guardar_todo':
            # ...tu lógica...
            pass

        # El resto igual, o llama a funciones de otros módulos

    return render_template(
        'configuracion.html',
        config=config,
        vista=vista,
        campos=campos,
        vistas=VISTAS_CONFIG,
        archivos_config=archivos_config
    )

# Importa y registra el blueprint de estilos si lo necesitas
from .configuracion_estilos import estilos_bp