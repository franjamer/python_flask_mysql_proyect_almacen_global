def validar_pedido(datos):
    referencia_pedido = datos.get('referencia_pedido', '').strip()
    fecha_creacion = datos.get('fecha_creacion', '').strip()
    referencias = datos.getlist('referencia_articulo[]')
    cantidades_pedidas = datos.getlist('cantidad_pedida[]')
    cantidades_recibidas = datos.getlist('cantidad_recibida[]')

    if not referencia_pedido:
        return "El campo 'Referencia del pedido' es obligatorio."
    if not fecha_creacion:
        return "El campo 'Fecha creación' es obligatorio."
    if not referencias or all(ref.strip() == '' for ref in referencias):
        return "Debes añadir al menos un repuesto al pedido."
    for i in range(len(referencias)):
        if not referencias[i].strip():
            return f"Falta la referencia del repuesto en la línea {i+1}."
        if not cantidades_pedidas[i].strip():
            return f"Falta la cantidad pedida en la línea {i+1}."
        if not cantidades_recibidas[i].strip():
            return f"Falta la cantidad recibida en la línea {i+1}."
    return None

def obtener_nombre_articulo(cursor, referencia):
    cursor.execute("SELECT nombre FROM inventario_tabla WHERE referencia = %s", (referencia,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else ""