import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../configuracion.json')
PERSONAL_CONFIG_DIR = os.path.join(os.path.dirname(__file__), '../../personal_config')
if not os.path.exists(PERSONAL_CONFIG_DIR):
    os.makedirs(PERSONAL_CONFIG_DIR)

from .configuracion_utils import VISTAS_CONFIG

def cargar_configuracion():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {}
    if 'nombres_columnas' not in config:
        config['nombres_columnas'] = {}
    for campos in VISTAS_CONFIG.values():
        for campo in campos:
            if campo not in config['nombres_columnas']:
                config['nombres_columnas'][campo] = campo.replace('_', ' ').capitalize()
    if 'textos_menu' not in config:
        config['textos_menu'] = {
            "central": "Bienvenido al sistema de gestión",
            "titulo_principal": "Bienvenido al sistema de gestión",
            "titulo_secundario": "Menú Principal"
        }
    if 'nombres_vistas' not in config:
        config['nombres_vistas'] = {
            'Busqueda': 'Busqueda de Repuestos',
            'inventario': 'Inventario',
            'movimientos': 'Movimientos',
            'pedidos': 'Pedidos',
            'operadores': 'Operadores',
            'perfiles': 'Perfiles',
            'situacion': 'Situación',
            'mapa_interactivo': 'Mapa Interactivo',
            'menu': 'Menú Principal'
        }
    return config

def guardar_configuracion(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def listar_archivos_config():
    return [f for f in os.listdir(PERSONAL_CONFIG_DIR) if f.endswith('.json')]