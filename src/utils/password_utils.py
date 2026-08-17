"""
Módulo de utilidades para manejo seguro de contraseñas.
Usa werkzeug.security para hashing de contraseñas con PBKDF2.
"""

from werkzeug.security import generate_password_hash, check_password_hash
import os

PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', '8'))
HASH_METHOD = 'pbkdf2:sha256'  # Método de hashing seguro


def hash_password(password: str) -> str:
    """
    Genera un hash seguro de la contraseña usando PBKDF2-SHA256.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash seguro de la contraseña
        
    Raises:
        ValueError: Si la contraseña es demasiado corta
    """
    if not password or len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"La contraseña debe tener al menos {PASSWORD_MIN_LENGTH} caracteres")
    
    # generate_password_hash usa 250,000 iteraciones por defecto
    return generate_password_hash(password, method=HASH_METHOD)


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash.
    
    Args:
        password: Contraseña en texto plano a verificar
        password_hash: Hash de contraseña almacenado en la BD
        
    Returns:
        True si la contraseña es correcta, False en caso contrario
    """
    try:
        return check_password_hash(password_hash, password)
    except Exception as e:
        print(f"Error al verificar contraseña: {e}")
        return False


def is_password_hashed(password_str: str) -> bool:
    """
    Verifica si una cadena ya es un hash PBKDF2 (para detectar migraciones).
    
    Args:
        password_str: Cadena a verificar
        
    Returns:
        True si parece ser un hash, False si es texto plano
    """
    # Los hashes PBKDF2 comienzan con "pbkdf2:sha256$"
    return password_str.startswith('pbkdf2:')
