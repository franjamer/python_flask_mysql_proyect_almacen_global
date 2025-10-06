from flask import Blueprint, render_template, request, redirect, url_for, flash
from .vistas_config import VISTAS
from .configuracion_estilos import cargar_estilos_por_vista, guardar_estilos_por_vista
from .configuracion_general import obtener_nombres_columnas, actualizar_nombres_columnas
import json
import os

configuracion_bp = Blueprint('configuracion_bp', __name__)

@configuracion_bp.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    # 
    pestana = request.args.get('pestana') or request.form.get('pestana') or 'general'
    vista = request.args.get('vista') or request.form.get('vista') or 'inventario'

    # Procesar cambios en estilos por vista
    if request.method == 'POST' and pestana == 'estilos':
        estilos_por_vista = cargar_estilos_por_vista()
        for key, value in request.form.items():
            if '-' in key:
                vista_key, param = key.split('-', 1)
                if vista_key not in estilos_por_vista:
                    estilos_por_vista[vista_key] = {}
                estilos_por_vista[vista_key][param] = value
        guardar_estilos_por_vista(estilos_por_vista)
        flash('Estilos guardados correctamente.', 'success')
        return redirect(url_for('configuracion_bp.configuracion', pestana='estilos'))
    # Procesar cambios en nombres de columnas
    config = {
        'nombres_columnas': obtener_nombres_columnas(vista)
    }
    # Actualizar nombres de columnas si se envió el formulario
    estilos_por_vista = cargar_estilos_por_vista()
    # Procesar cambios en nombres de columnas
    return render_template(
        'configuracion.html',
        pestana=pestana,
        vista=vista,
        estilos_por_vista=estilos_por_vista,
        config=config,
        campos=VISTAS[vista]['columnas'],
        vistas=VISTAS
    )

def cargar_configuracion():
    pass


