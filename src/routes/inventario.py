from flask import Blueprint, render_template, request, redirect, url_for
import database as db

inventario_bp = Blueprint('inventario_bp', __name__)

# Campos de la tabla (excepto id)
CAMPOS = [
    'referencia',
    'nombre',
    'categoria',
    'subcategoria',
    'almacen',
    'caracteristicas_medidas',
    'fotos_planos',
    'empaquetado',
    'stock'
]

@inventario_bp.route('/inventario', methods=['GET', 'POST'])
def inventario():
    mensaje_error = None
    if request.method == 'POST':
        datos = {campo: request.form.get(campo, '').strip() for campo in CAMPOS}
        # Validar obligatorios
        obligatorios = ['referencia', 'categoria']
        if any(datos[campo] == '' for campo in obligatorios):
            mensaje_error = "Referencia y Categoría son obligatorios."
        else:
            conn = db.get_connection()
            cursor = conn.cursor()
            try:
                placeholders = ','.join(['%s'] * len(CAMPOS))
                campos_str = ','.join(CAMPOS)
                valores = [datos[campo] if campo != 'stock' else (datos[campo] if datos[campo] != '' else 0) for campo in CAMPOS]
                cursor.execute(
                    f"INSERT INTO inventario_tabla ({campos_str}) VALUES ({placeholders})",
                    tuple(valores)
                )
                conn.commit()
            except Exception as e:
                mensaje_error = "Error al añadir el repuesto: " + str(e)
            cursor.close()
            conn.close()
            if not mensaje_error:
                return redirect(url_for('inventario_bp.inventario'))

    # Mostrar todos los repuestos
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, {', '.join(CAMPOS)} FROM inventario_tabla")
    repuestos = cursor.fetchall()
    cursor.close()
    conn.close()
    columnas = ['id'] + CAMPOS
    return render_template('inventario.html', repuestos=repuestos, columnas=columnas, mensaje_error=mensaje_error)

@inventario_bp.route('/inventario/modificar/<referencia>', methods=['POST'])
def modificar_repuesto(referencia):
    datos = {campo: request.form.get(campo, '').strip() for campo in CAMPOS}
    conn = db.get_connection()
    cursor = conn.cursor()
    set_clause = ', '.join([f"{campo}=%s" for campo in CAMPOS if campo != 'referencia'])
    valores = [datos[campo] if campo != 'stock' else (datos[campo] if datos[campo] != '' else 0) for campo in CAMPOS if campo != 'referencia']
    valores.append(referencia)
    cursor.execute(
        f"UPDATE inventario_tabla SET {set_clause} WHERE referencia=%s",
        tuple(valores)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('inventario_bp.inventario'))

@inventario_bp.route('/inventario/eliminar/<referencia>', methods=['POST'])
def eliminar_repuesto(referencia):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventario_tabla WHERE referencia=%s", (referencia,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('inventario_bp.inventario'))