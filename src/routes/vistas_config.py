import json
import os

RUTA_JSON = os.path.join(os.path.dirname(__file__), '..', 'vistas_config.json')

def cargar_vistas():
    with open(RUTA_JSON, encoding='utf-8') as f:
        return json.load(f)

def guardar_vistas(VISTAS):
    with open(RUTA_JSON, 'w', encoding='utf-8') as f:
        json.dump(VISTAS, f, ensure_ascii=False, indent=2)

VISTAS = cargar_vistas()

