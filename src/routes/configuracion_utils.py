VISTAS_CONFIG = {
    "inventario": [
        "Referencia", "Nombre", "Categoria", "Subcategoria",
        "Caracteristicas_Medidas", "Fotos_Planos", "Empaquetado",
        "Stock", "Stock_Minimo", "Stock_Maximo", "id_Situacion_Tabla"
    ],
    "operadores": [
        "Codigo_Operador", "Nombre_Completo", "Telefono", "Email",
        "Direccion", "id_Situacion_Tabla"
    ],
    "movimientos": [
        "Referencia_Pieza_Repuesto", "Nombre_Pieza_Repuesto", "Tipo_De_Movimiento",
        "Cantidad", "Unidad_De_Cantidad", "Codigo_Operador", "Fecha_Movimiento",
        "Stock_Tras_Movimiento"
    ],
    "operadores": [
        "Codigo_Operador", "Nombre_Completo", "Telefono", "Email",
        "Direccion", "id_Situacion_Tabla"
    ],
    "movimientos": [
        "Referencia_Pieza_Repuesto", "Nombre_Pieza_Repuesto", "Tipo_De_Movimiento",
        "Cantidad", "Unidad_De_Cantidad", "Codigo_Operador", "Fecha_Movimiento",
        "Stock_Tras_Movimiento"
    ],
    
    
}

def inicializar_config(config, vistas_config):
    if config is None:
        config = {}
    if 'nombres_columnas' not in config or not config['nombres_columnas']:
        config['nombres_columnas'] = {}
    for campos_vista in vistas_config.values():
        for campo in campos_vista:
            if campo not in config['nombres_columnas']:
                config['nombres_columnas'][campo] = campo.replace('_', ' ').capitalize()
    if 'estilo_menu' not in config:
        config['estilo_menu'] = {
            'color_texto_menu': '#000000',
            'color_fondo_menu': '#ffffff',
            'tamano_texto_menu': '16px',
            'estilo_texto_menu': 'normal'
        }
    if 'textos_menu' not in config or not config['textos_menu']:
        config['textos_menu'] = {
            "central": "Bienvenido al sistema de gestión",
            "titulo_principal": "Bienvenido al sistema de gestión",
            "titulo_secundario": "Menú Principal"
        }
    if 'estilos_vistas' not in config:
        config['estilos_vistas'] = {}
    return config