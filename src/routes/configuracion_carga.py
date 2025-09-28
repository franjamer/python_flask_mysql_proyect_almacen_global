import json
import os
from .vistas_config import VISTAS
CONFIG_PATH = 'ruta/donde/guardas/las/configs'

# Asegura que la carpeta existe antes de guardar/cargar
if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)

def guardar_configuracion(config, nombre_archivo='config.json'):
    ruta = os.path.join(CONFIG_PATH, nombre_archivo)
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error al guardar la configuración: {e}")

def cargar_configuracion(nombre_archivo='config.json'):
    ruta = os.path.join(CONFIG_PATH, nombre_archivo)
    if not os.path.exists(ruta):
        print(f"Archivo de configuración no encontrado: {ruta}")
        return None
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar la configuración: {e}")
        return None

def listar_archivos_config():
    """Devuelve una lista de archivos de configuración disponibles."""
    if not os.path.exists(CONFIG_PATH):
        return []
    return [f for f in os.listdir(CONFIG_PATH) if f.endswith('.json')]