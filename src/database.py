import os
import mysql.connector
import time # 🎯 Añade esta importación

def get_connection():
    """
    Intenta establecer una conexión a la base de datos.
    Reintenta la conexión si el primer intento falla.
    """
    conn = None
    max_retries = 5 # Número máximo de intentos
    retry_delay = 2 # Retraso en segundos entre intentos
    
    for i in range(max_retries):
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                user=os.environ.get('DB_USER', 'usuario'),
                password=os.environ.get('DB_PASSWORD', 'clave'),
                database=os.environ.get('DB_NAME', 'almacen'),
                port=3306
            )
            # Si la conexión tiene éxito, salimos del bucle
            print("Conexión a la base de datos establecida con éxito.")
            return conn
            
        except mysql.connector.Error as err:
            print(f"Intento {i + 1}/{max_retries}: Error al conectar con la base de datos: {err}")
            if i < max_retries - 1:
                print(f"Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                print("Todos los intentos de conexión han fallado.")
                return None # Devuelve None si todos los intentos fallan