def puede_ver_pedidos(rol):
    return rol in ['admin', 'pedidos']

def puede_crud_pedidos(rol):
    return rol in ['admin', 'pedidos']

def puede_eliminar_pedidos(rol):
    return rol in ['admin', 'pedidos']

def puede_ver_inventario(rol):
    return rol == 'admin'

def puede_ver_movimientos(rol):
    return True

def puede_eliminar_movimientos(rol):
    return rol == 'admin'

def puede_ver_busqueda(rol):
    return True