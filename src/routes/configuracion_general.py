from .vistas_config import VISTAS, guardar_vistas
# vistas es un diccionario global que contiene la configuración de todas las vistas
# guardar vistas es una función para manejar el archivo JSON
def obtener_nombres_columnas(vista):
    nombres_defecto = {campo: campo.replace('_', ' ').capitalize() for campo in VISTAS[vista]['columnas']}
    nombres_personalizados = VISTAS[vista].get('nombres_columnas', {})
    return {campo: nombres_personalizados.get(campo, nombres_defecto[campo]) for campo in VISTAS[vista]['columnas']}
# actualiza los nombres de columnas en el archivo JSON
def actualizar_nombres_columnas(vista, form):
    if 'nombres_columnas' not in VISTAS[vista]:
        VISTAS[vista]['nombres_columnas'] = {}
    for campo in VISTAS[vista]['columnas']:
        nuevo_valor = form.get(f'nombre_columna_{campo}')
        if nuevo_valor:
            VISTAS[vista]['nombres_columnas'][campo] = nuevo_valor
    guardar_vistas(VISTAS)