from flask import Blueprint
import json
import os

estilos_bp = Blueprint('estilos_bp', __name__)

ESTILOS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'estilos_config.json'))

def cargar_estilos_por_vista():
    if os.path.exists(ESTILOS_PATH):
        with open(ESTILOS_PATH, encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_estilos_por_vista(estilos_por_vista):
    with open(ESTILOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(estilos_por_vista, f, indent=2, ensure_ascii=False)