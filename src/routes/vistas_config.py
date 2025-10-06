import json
import os

RUTA_JSON = os.path.join(os.path.dirname(__file__), '..', 'vistas_config.json')
# lee los datos del archivo JSON
def cargar_vistas():
    with open(RUTA_JSON, encoding='utf-8') as f:
        return json.load(f)
# Guarda los datos en el archivo JSON
def guardar_vistas(VISTAS):
    with open(RUTA_JSON, 'w', encoding='utf-8') as f:
        json.dump(VISTAS, f, ensure_ascii=False, indent=2)
# vistas es un diccionario global que contiene la configuración de todas las vistas
VISTAS = cargar_vistas()

