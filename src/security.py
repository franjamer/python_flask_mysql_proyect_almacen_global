"""
Configuración centralizada de seguridad para la aplicación Flask.
Incluye headers HTTP de seguridad, CORS y protección contra ataques comunes.
"""

from flask import request
from flask_cors import CORS
import os


def init_security(app):
    """
    Inicializa todas las configuraciones de seguridad en la aplicación Flask.
    
    Args:
        app: Instancia de Flask
    """
    
    # ============================================
    # 1. CONFIGURACIÓN DE CORS
    # ============================================
    
    # Configurar CORS - permitir solicitudes desde dominios específicos
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:4000').split(',')
    CORS(app, 
         resources={r"/api/*": {"origins": cors_origins}},
         supports_credentials=True,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         max_age=86400,  # 24 horas
         expose_headers=['Content-Type', 'X-Total-Count'])
    
    # ============================================
    # 2. SECURITY HEADERS - Ejecutar después de cada request
    # ============================================
    
    @app.after_request
    def set_security_headers(response):
        """
        Añade headers de seguridad HTTP a todas las respuestas.
        Previene ataques comunes como XSS, clickjacking, MIME-sniffing.
        """
        
        # Previene MIME-type sniffing (XSS)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Previene clickjacking - permite solo si se embebe en el mismo origen
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Protección XSS (older browsers)
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Content Security Policy - restrictivo por defecto
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "  # unsafe-inline necesario para templates Jinja2
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'self'"
        )
        
        # Referrer Policy - no enviar referrer a terceros
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Feature Policy - desabilitar features potencialmente peligrosas
        response.headers['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'payment=()'
        )
        
        # Habilitar HTTPS Strict Transport Security (en producción)
        if not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Prevenir caching de datos sensibles
        if request.path.startswith(('/login', '/logout', '/api/')):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        
        return response
    
    # ============================================
    # 3. PROTECCIÓN CONTRA ATAQUES
    # ============================================
    
    @app.before_request
    def security_checks():
        """
        Realizar verificaciones de seguridad antes de procesar cada solicitud.
        """
        
        # Limitar tamaño de payload (10MB máximo)
        if request.content_length and request.content_length > 10 * 1024 * 1024:
            return "Payload demasiado grande", 413
        
        # Verificar que el User-Agent no sea sospechoso (opcional)
        user_agent = request.headers.get('User-Agent', '')
        if not user_agent:
            # Puede ser un bot malicioso
            pass


def configure_session_security(app):
    """
    Configura opciones de seguridad para las sesiones.
    
    Args:
        app: Instancia de Flask
    """
    
    app.config['SESSION_COOKIE_SECURE'] = not app.debug  # Solo HTTPS en producción
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # No accesible desde JavaScript
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protección CSRF
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
