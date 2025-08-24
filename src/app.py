# Importación de dependencias y variables necesarias
from flask import Flask, session, redirect, url_for, request, render_template
import os
import database as db
from routes.home import home_bp
from routes.perfiles import perfiles_bp
from routes.movimientos import movimientos_bp
from routes.pedidos import pedidos_bp
from routes.tablas import tablas_bp
from routes.inventario import inventario_bp
from routes.operadores import operadores_bp
from routes.roles import puede_eliminar_movimientos
from routes.situacion import situacion_bp
from routes.mapa import mapa_bp
# configuración de carpetas y path de la aplicación.
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'FJMR_ADMIN'

# RUTA DE LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        perfil = request.form['perfil']
        password = request.form['password']
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT rol FROM perfiles WHERE perfil = %s AND password = %s", (perfil, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['perfil'] = perfil
            session['rol'] = user[0]
            return redirect(url_for('home_bp.menu'))
        else:
            error = 'perfil o contraseña incorrectos'
    return render_template('login.html', error=error)

# RUTA DE LOGOUT
@app.route('/logout')
def logout():
    session.pop('perfil', None)
    return redirect(url_for('login'))

# PROTECCIÓN DE RUTAS
@app.before_request
def require_login():
    rutas_libres = ['login', 'static']
    if request.endpoint not in rutas_libres and not session.get('perfil'):
        print(f'Acceso denegado a la ruta: {request.url}')
        return redirect(url_for('login'))

# Registrar Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(perfiles_bp)
app.register_blueprint(inventario_bp)
app.register_blueprint(movimientos_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(tablas_bp)
app.register_blueprint(operadores_bp)
app.register_blueprint(situacion_bp )
app.register_blueprint(mapa_bp)
# Deshabilita el caché de plantillas para desarrollo
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

# Configuración de la base de datos
if __name__ == '__main__':
    app.run(debug=True, port=4000)


