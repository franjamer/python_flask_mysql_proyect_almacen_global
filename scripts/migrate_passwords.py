#!/usr/bin/env python
"""
Script de migración: Convierte contraseñas en texto plano a hashes seguros.

Uso:
    python migrate_passwords.py
    
Este script:
1. Conecta a la base de datos
2. Busca todos los perfiles con contraseñas en texto plano
3. Genera hashes seguros usando PBKDF2-SHA256
4. Actualiza la base de datos
5. Crea un backup antes de hacer cambios
"""

import sys
import os
from datetime import datetime

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
load_dotenv()

import database as db
from utils.password_utils import hash_password, is_password_hashed


def create_backup(conn):
    """Crear un backup de la tabla perfiles antes de hacer cambios."""
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_table = f'perfiles_backup_{timestamp}'
    
    try:
        cursor.execute(f'CREATE TABLE {backup_table} AS SELECT * FROM perfiles')
        conn.commit()
        print(f"✅ Backup creado: {backup_table}")
        cursor.close()
        return backup_table
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        cursor.close()
        return None


def migrate_passwords():
    """Migrar todas las contraseñas de texto plano a hashes."""
    
    print("=" * 60)
    print("MIGRACIÓN DE CONTRASEÑAS - De texto plano a PBKDF2-SHA256")
    print("=" * 60)
    
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        # Crear backup
        backup_table = create_backup(conn)
        if not backup_table:
            print("⚠️  No se pudo crear backup. Operación cancelada.")
            return False
        
        # Obtener todos los perfiles
        cursor.execute("SELECT id, perfil, password FROM perfiles")
        perfiles = cursor.fetchall()
        
        if not perfiles:
            print("❌ No se encontraron perfiles en la base de datos.")
            cursor.close()
            conn.close()
            return False
        
        print(f"\n📊 Encontrados {len(perfiles)} perfil(es)")
        
        # Contar contraseñas ya hasheadas vs texto plano
        plain_text_count = 0
        hashed_count = 0
        errors = 0
        
        for perfil_id, perfil_name, password_field in perfiles:
            if is_password_hashed(password_field):
                hashed_count += 1
                print(f"  ⏭️  {perfil_name}: Ya hasheada (saltando)")
            else:
                try:
                    # Generar hash de la contraseña en texto plano
                    new_hash = hash_password(password_field)
                    
                    # Actualizar en la base de datos
                    cursor.execute(
                        "UPDATE perfiles SET password = %s WHERE id = %s",
                        (new_hash, perfil_id)
                    )
                    conn.commit()
                    
                    plain_text_count += 1
                    print(f"  ✅ {perfil_name}: Contraseña hasheada exitosamente")
                
                except ValueError as ve:
                    errors += 1
                    print(f"  ⚠️  {perfil_name}: {str(ve)}")
                except Exception as e:
                    errors += 1
                    print(f"  ❌ {perfil_name}: Error - {str(e)}")
        
        cursor.close()
        conn.close()
        
        # Resumen
        print("\n" + "=" * 60)
        print("RESUMEN DE LA MIGRACIÓN")
        print("=" * 60)
        print(f"✅ Contraseñas hasheadas: {plain_text_count}")
        print(f"⏭️  Contraseñas ya hasheadas: {hashed_count}")
        print(f"❌ Errores: {errors}")
        print(f"📊 Total procesados: {plain_text_count + hashed_count + errors}")
        
        if errors == 0:
            print("\n✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print(f"\n💾 Backup guardado en tabla: {backup_table}")
            return True
        else:
            print(f"\n⚠️  Migración completada con {errors} error(es)")
            return False
    
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        if conn:
            conn.close()
        return False


def restore_from_backup(backup_table):
    """
    Restaurar desde un backup en caso de emergencia.
    
    Uso:
        restore_from_backup('perfiles_backup_20260817_120000')
    """
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        print(f"\n⚠️  Restaurando desde {backup_table}...")
        cursor.execute(f"DROP TABLE IF EXISTS perfiles")
        cursor.execute(f"ALTER TABLE {backup_table} RENAME TO perfiles")
        conn.commit()
        print("✅ Restauración completada")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error en restauración: {e}")
        cursor.close()
        conn.close()
        return False


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrar contraseñas a hashes seguros')
    parser.add_argument('--restore', type=str, help='Restaurar desde un backup (nombre de la tabla)')
    args = parser.parse_args()
    
    if args.restore:
        success = restore_from_backup(args.restore)
    else:
        success = migrate_passwords()
    
    sys.exit(0 if success else 1)
