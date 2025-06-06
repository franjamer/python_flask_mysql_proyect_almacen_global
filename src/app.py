from flask import Flask
import os
from routes.home import home_bp
from routes.users import users_bp
from routes.movimientos import movimientos_bp
from routes.pedidos import pedidos_bp
from routes.tablas import tablas_bp
from routes.inventario import inventario_bp

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder=template_dir)

# Registrar Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(users_bp)
app.register_blueprint(inventario_bp)
app.register_blueprint(movimientos_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(tablas_bp)

# Configuración de la base de datos
if __name__ == '__main__':
    app.run(debug=True, port=4000)
