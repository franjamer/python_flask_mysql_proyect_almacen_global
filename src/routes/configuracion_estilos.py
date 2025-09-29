from flask import Blueprint, request, session, redirect, url_for, flash
from .configuracion_carga import cargar_configuracion, guardar_configuracion
from .vistas_config import VISTAS

estilos_bp = Blueprint('estilos_bp', __name__)

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

def obtener_estilos_globales():
    # Devuelve los estilos de la primera vista con 'estilos'
    for datos in VISTAS.values():
        if 'estilos' in datos:
            return datos['estilos']
    return {}

def actualizar_estilos_globales(form, parametro):
    for vista, datos in VISTAS.items():
        if 'estilos' in datos:
            estilos = datos['estilos']
            if parametro == 'todos':
                for clave in estilos.keys():
                    nuevo_valor = form.get(f'global_{clave}')
                    if nuevo_valor:
                        estilos[clave] = nuevo_valor
            else:
                nuevo_valor = form.get(f'global_{parametro}')
                if nuevo_valor:
                    estilos[parametro] = nuevo_valor

def actualizar_estilo_vista(vista, form):
    if 'estilos' in VISTAS[vista]:
        for clave in VISTAS[vista]['estilos'].keys():
            nuevo_valor = form.get(f'local_{clave}')
            if nuevo_valor:
                VISTAS[vista]['estilos'][clave] = nuevo_valor

from flask import render_template

@estilos_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    pestana = request.args.get('pestana', '')
    subpestana = request.args.get('subpestana', '')

    if request.method == 'POST' and pestana == 'estilos' and subpestana == 'global':
        parametro = request.form.get('parametro_global', 'todos')
        actualizar_estilos_globales(request.form, parametro)
        estilos_globales = obtener_estilos_globales(request.form, parametro)
        flash('Estilos globales actualizados.', 'success')
        return render_template(
            'configuracion.html',
            color_texto=estilos_globales['color_texto_menu'],
            color_fondo=estilos_globales['color_fondo_menu'],
            tamano_texto=estilos_globales['tamano_texto_menu'],
            estilo_texto=estilos_globales['estilo_texto_menu'],
        )

    return render_template('configuracion.html', color_texto='', color_fondo='', tamano_texto='', estilo_texto='')