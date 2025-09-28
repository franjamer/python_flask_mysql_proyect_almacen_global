from flask import Blueprint, request, session, redirect, url_for, flash
from .configuracion_carga import cargar_configuracion, guardar_configuracion
from .vistas_config import VISTAS

estilos_bp = Blueprint('estilos_bp', __name__)

def actualizar_estilo_vista(vista, clave_estilo, nuevo_valor):
    if clave_estilo in VISTAS[vista]["estilos"]:
        VISTAS[vista]["estilos"][clave_estilo] = nuevo_valor
        # Aquí puedes guardar el cambio en un archivo si lo deseas

@estilos_bp.route('/aplicar_estilo', methods=['POST'])
def aplicar_estilo():
    if session.get('perfil') != 'Admin':
        flash('Acceso denegado: solo el perfil Admin puede acceder a configuración.', 'error')
        return redirect(url_for('home_bp.menu'))

    config = cargar_configuracion()
    accion = request.form.get('accion')

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
        return redirect(url_for('configuracion_bp.configuracion'))

    return redirect(url_for('configuracion_bp.configuracion'))