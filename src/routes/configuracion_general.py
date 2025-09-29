from .vistas_config import VISTAS

def obtener_nombres_columnas(vista):
    nombres_defecto = {campo: campo.replace('_', ' ').capitalize() for campo in VISTAS[vista]['columnas']}
    nombres_personalizados = VISTAS[vista].get('nombres_columnas', {})
    return {campo: nombres_personalizados.get(campo, nombres_defecto[campo]) for campo in VISTAS[vista]['columnas']}

def actualizar_nombres_columnas(vista, form):
    if 'nombres_columnas' not in VISTAS[vista]:
        VISTAS[vista]['nombres_columnas'] = {}
    for campo in VISTAS[vista]['columnas']:
        nuevo_valor = form.get(f'nombre_columna_{campo}')
        if nuevo_valor:
            VISTAS[vista]['nombres_columnas'][campo] = nuevo_valor