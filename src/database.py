import os
import mysql.connector
import time

def get_connection():
    """
    Intenta establecer una conexión a la base de datos.
    Reintenta la conexión si el primer intento falla.
    """
    max_retries = 5  # Número máximo de intentos
    retry_delay = 2  # Retraso en segundos entre intentos

    for i in range(max_retries):
        try:
            conn = mysql.connector.connect(
                host='localhost',           # Cambia 'db' por 'localhost'
                user='root',    # Tu usuario de MySQL local
                password='root', # Tu contraseña de MySQL local
                database='almacenRepuestos',     # El nombre de tu base de datos local
                port=3306
            )
            print("Conexión a la base de datos establecida con éxito.")
            return conn
        except mysql.connector.Error as err:
            print(f"Intento {i + 1}/{max_retries}: Error al conectar con la base de datos: {err}")
            if i < max_retries - 1:
                print(f"Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                print("Todos los intentos de conexión han fallado.")
                return None  # Devuelve None si todos los intentos fallan

