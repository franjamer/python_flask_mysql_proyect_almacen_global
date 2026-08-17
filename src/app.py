# Importación de dependencias y variables necesarias
from flask import Flask, session, redirect, url_for, request, render_template
import os
import sys
from dotenv import load_dotenv
import database as db
from security import init_security, configure_session_security

# Cargar variables de entorno desde .env
# Buscar .env en el directorio raíz del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(project_root, '.env')
load_dotenv(env_file)
# Cargar variables de entorno desde .env
# Buscar .env en el directorio raíz del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(project_root, '.env')
load_dotenv(env_file)

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
from routes.configuracion import configuracion_bp, cargar_configuracion
from routes.proveedores import proveedores_bp
from routes.busqueda import busqueda_bp
from utils.password_utils import verify_password, is_password_hashed
# from src import create_app
# configuración de carpetas y path de la aplicación.
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
# app= create_app()
# Inicialización de la aplicación Flask
app = Flask(__name__, template_folder=template_dir)

# ============================================
# CONFIGURAR DESDE VARIABLES DE ENTORNO
# ============================================
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-cambiar-en-produccion')
app.debug = os.getenv('DEBUG', 'False').lower() == 'true'

if app.debug:
    print("⚠️  ADVERTENCIA: Modo DEBUG activo. Cambiar a False en producción.")
else:
    print("✅ Modo producción: DEBUG=False")

# ============================================
# INICIALIZAR SEGURIDAD
# ============================================
init_security(app)
configure_session_security(app)

# RUTA DE LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        perfil = request.form.get('perfil', '').strip()
        password = request.form.get('password', '')
        
        if not perfil or not password:
            error = 'Usuario y contraseña son requeridos'
        else:
            conn = db.get_connection()
            cursor = conn.cursor()
            try:
                # Obtener el hash de contraseña del perfil
                cursor.execute(
                    "SELECT id, rol, password FROM perfiles WHERE perfil = %s", 
                    (perfil,)
                )
                user_record = cursor.fetchone()
                
                if user_record:
                    user_id, rol, stored_password = user_record
                    
                    # Verificar contraseña con hash
                    if verify_password(password, stored_password):
                        session['perfil'] = perfil
                        session['rol'] = rol
                        session['user_id'] = user_id
                        app.logger.info(f"Login exitoso para usuario: {perfil}")
                        return redirect(url_for('home_bp.menu'))
                    else:
                        app.logger.warning(f"Intento de login fallido para usuario: {perfil}")
                        error = 'Perfil o contraseña incorrectos'
                else:
                    app.logger.warning(f"Usuario no encontrado: {perfil}")
                    error = 'Perfil o contraseña incorrectos'
            except Exception as e:
                app.logger.error(f"Error en login: {str(e)}")
                error = 'Error en la autenticación. Por favor, intenta de nuevo.'
            finally:
                cursor.close()
                conn.close()
    
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
app.register_blueprint(configuracion_bp)
app.register_blueprint(proveedores_bp)
app.register_blueprint(busqueda_bp)

# Deshabilita el caché de plantillas SOLO en desarrollo
if app.debug:
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
else:
    app.config['TEMPLATES_AUTO_RELOAD'] = False

# Configuración de la base de datos
if __name__ == '__main__':
    app.run(debug=app.debug, port=4000)


