from flask import Blueprint, render_template, request, redirect, url_for, flash
from .vistas_config import VISTAS
from .configuracion_estilos import obtener_estilos_globales, actualizar_estilos_globales
from .configuracion_general import obtener_nombres_columnas, actualizar_nombres_columnas

configuracion_bp = Blueprint('configuracion_bp', __name__)

@configuracion_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    pestana = request.args.get('pestana') or request.form.get('pestana') or 'general'
    subpestana = request.args.get('subpestana') or request.form.get('subpestana')
    vista = request.args.get('vista') or request.form.get('vista') or 'inventario'

    if pestana == 'estilos' and not subpestana:
        subpestana = 'global'

    # Procesar cambios en estilos globales
    if request.method == 'POST' and pestana == 'estilos' and subpestana == 'global':
        parametro = request.form.get('parametro_global', 'todos')
        actualizar_estilos_globales(request.form, parametro)
        flash('Estilos globales actualizados.', 'success')
        return redirect(url_for('configuracion_bp.configuracion', pestana='estilos', subpestana='global', vista=vista))

    # Procesar cambios en nombres de columnas (General)
    if request.method == 'POST' and pestana == 'general':
        actualizar_nombres_columnas(vista, request.form)
        flash(f'Nombres de columnas actualizados para la vista {vista}.', 'success')
        return redirect(url_for('configuracion_bp.configuracion', pestana='general', vista=vista))

    estilos_globales = obtener_estilos_globales()
    config = {
        'nombres_columnas': obtener_nombres_columnas(vista)
    }

    return render_template(
        'configuracion.html',
        pestana=pestana,
        subpestana=subpestana,
        vista=vista,
        config=config,
        campos=VISTAS[vista]['columnas'],
        vistas=VISTAS,
        color_texto=estilos_globales.get('color_texto_menu', ''),
        color_fondo=estilos_globales.get('color_fondo_menu', ''),
        tamano_texto=estilos_globales.get('tamano_texto_menu', ''),
        estilo_texto=estilos_globales.get('estilo_texto_menu', '')
    )

def cargar_configuracion():
    pass


