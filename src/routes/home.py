from flask import Blueprint, render_template, request
from routes.configuracion import cargar_configuracion
import database as db
from .vistas_config import VISTAS
from .configuracion_general import obtener_nombres_columnas
from .configuracion_estilos import cargar_estilos_por_vista

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
# Página de bienvenida
def bienvenido():
    config = cargar_configuracion()
    return render_template('bienvenido.html', config=config)

@home_bp.route('/menu')
# Página del menú principal
def menu():
    config = cargar_configuracion()
    estilos_por_vista = cargar_estilos_por_vista()
    return render_template('menu.html', 
    config=config,
    vista='inventario',
    estilos_por_vista=estilos_por_vista)



