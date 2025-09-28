# Importa y registra el blueprint de estilos si lo necesitas
from .configuracion_estilos import estilos_bp
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .configuracion_utils import VISTAS_CONFIG, inicializar_config
from .configuracion_carga import cargar_configuracion, guardar_configuracion, listar_archivos_config
from .vistas_config_loader import cargar_vistas_config

configuracion_bp = Blueprint('configuracion_bp', __name__)

VISTAS_CONFIG = cargar_vistas_config()

@configuracion_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    if session.get('perfil') != 'Admin':
        flash('Acceso denegado: solo el perfil Admin puede acceder a configuración.', 'error')
        return redirect(url_for('home_bp.menu'))

    config = cargar_configuracion()
    config = inicializar_config(config, VISTAS_CONFIG)
    
    vista = request.args.get('vista', 'inventario')
    campos = VISTAS_CONFIG.get(vista, [])
    archivos_config = listar_archivos_config()

    if request.method == 'POST':
        # Actualiza los textos del menú si están en el formulario
        for campo in ['central', 'titulo_principal', 'titulo_secundario']:
            nuevo_valor = request.form.get(f'texto_menu_{campo}')
            if nuevo_valor:
                config['textos_menu'][campo] = nuevo_valor

        # Actualiza nombres de columnas si están en el formulario
        for campo in config['nombres_columnas']:
            nuevo_valor = request.form.get(f'nombre_columna_{campo}')
            if nuevo_valor:
                config['nombres_columnas'][campo] = nuevo_valor

        # Actualiza estilos por vista si corresponde
        for vista in config.get('estilos_vistas', {}):
            for clave in ['color_texto_menu', 'color_fondo_menu', 'tamano_texto_menu', 'estilo_texto_menu']:
                nuevo_valor = request.form.get(f'estilo_{clave}_{vista}')
                if nuevo_valor:
                    config['estilos_vistas'][vista][clave] = nuevo_valor

        # Guarda la configuración actualizada
        guardar_configuracion(config)
        flash('Configuración guardada correctamente.', 'success')
        return redirect(url_for('configuracion_bp.configuracion'))

    return render_template(
        'configuracion.html',
        config=config,
        vista=vista,
        campos=campos,
        vistas=VISTAS_CONFIG,
        archivos_config=archivos_config
    )