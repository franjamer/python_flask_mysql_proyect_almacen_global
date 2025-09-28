VISTAS = {
    "inventario": {
        "columnas": [
            "referencia", "nombre", "categoria", "subcategoria",
            "caracteristicas_medidas", "fotos_planos", "empaquetado",
            "stock", "stock_minimo", "stock_maximo", "id_situacion_tabla"
        ],
        "estilos": {
            "color_texto_menu": "#bfbfbf",
            "color_fondo_menu": "#b3cef9",
            "tamano_texto_menu": "16",
            "estilo_texto_menu": "normal"
        }
    },
    "busqueda": {
        "columnas": [
            "referencia", "nombre", "categoria", "almacen", "stock", "ubicacion", "id_situacion_tabla"
        ],
        "estilos": {
            "color_texto_menu": "#000000",
            "color_fondo_menu": "#ffffff",
            "tamano_texto_menu": "16",
            "estilo_texto_menu": "normal"
        }
    },
    "menu": {
        "columnas": ["central", "titulo_principal", "titulo_secundario"],
        "estilos": {
            "color_texto_menu": "#000000",
            "color_fondo_menu": "#f17e7e",
            "tamano_texto_menu": "16",
            "estilo_texto_menu": "normal"
        }
    },
    "operadores": {
        "columnas": [
            "codigo_operador", "nombre_completo", "telefono", "email",
            "direccion", "id_situacion_tabla"
        ],
        "estilos": {
            "color_texto_menu": "#000000",
            "color_fondo_menu": "#ffffff",
            "tamano_texto_menu": "16",
            "estilo_texto_menu": "normal"
        }
    },
    "movimientos": {
        "columnas": [
            "referencia_pieza_repuesto", "nombre_pieza_repuesto", "tipo_de_movimiento",
            "cantidad", "unidad_de_cantidad", "codigo_operador", "fecha_movimiento",
            "stock_tras_movimiento"
        ],
        "estilos": {
            "color_texto_menu": "#000000",
            "color_fondo_menu": "#ffffff",
            "tamano_texto_menu": "16",
            "estilo_texto_menu": "normal"
        }
    },
    "pedidos": {
        "columnas": [
            "id_pedido", "fecha", "referencia", "cantidad", "estado", "proveedor"
        ],
        "estilos": {
            "color_texto_menu": "#000000",
            "color_fondo_menu": "#ffffff",
            "tamano_texto_menu": "16",
            "estilo_texto_menu": "normal"
        }
    },
    "perfiles": {
        "columnas": [
            "id_perfil", "perfil", "descripcion"
        ],
        "estilos": {
            "color_texto_menu": "#000000",
            "color_fondo_menu": "#ffffff",
            "tamano_texto_menu": "16",
            "estilo_texto_menu": "normal"
        }
    },
    "situacion": {
        "columnas": [
            "id_situacion_tabla", "almacen", "estanteria", "lado", "columna", "altura"
        ],
        "estilos": {
            "color_texto_menu": "#000000",
            "color_fondo_menu": "#ffffff",
            "tamano_texto_menu": "16",
            "estilo_texto_menu": "normal"
        }
    },
    "mapa_interactivo": {
        "columnas": [
            "almacen", "estanteria", "lado", "columna", "altura"
        ],
        "estilos": {
            "color_texto_menu": "#000000",
            "color_fondo_menu": "#ffffff",
            "tamano_texto_menu": "16",
            "estilo_texto_menu": "normal"
        }
    }
}