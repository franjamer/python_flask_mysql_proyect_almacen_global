import json
import os
from .vistas_config import VISTAS

def cargar_vistas_config():
    ruta = os.path.join(os.path.dirname(__file__), '..', 'vistas_config.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)