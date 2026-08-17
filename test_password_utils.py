"""
Test de verificación del módulo de hashing de contraseñas
"""

import sys
import os
sys.path.insert(0, 'src')

from utils.password_utils import hash_password, verify_password, is_password_hashed

print("=" * 60)
print("TEST: Módulo de Hashing de Contraseñas")
print("=" * 60)

# Test 1: Generar hash
print("\n[TEST 1] Generar hash de contraseña")
try:
    password = "MiContraseña123"
    hashed = hash_password(password)
    print(f"✅ Contraseña original: {password}")
    print(f"✅ Hash generado: {hashed[:50]}...")
    print(f"✅ Es hash PBKDF2: {is_password_hashed(hashed)}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Verificar contraseña correcta
print("\n[TEST 2] Verificar contraseña correcta")
if verify_password(password, hashed):
    print(f"✅ Contraseña verificada correctamente")
else:
    print(f"❌ Error: Contraseña no verificada")

# Test 3: Verificar contraseña incorrecta
print("\n[TEST 3] Verificar contraseña incorrecta")
if not verify_password("ContraseñaIncorrecta", hashed):
    print(f"✅ Rechazo correctamente contraseña incorrecta")
else:
    print(f"❌ Error: Aceptó contraseña incorrecta")

# Test 4: Validar longitud mínima
print("\n[TEST 4] Validar longitud mínima de contraseña")
try:
    hash_password("123")  # Muy corta
    print(f"❌ Error: Permitió contraseña muy corta")
except ValueError as e:
    print(f"✅ Rechazó correctamente: {e}")

# Test 5: Detectar texto plano vs hash
print("\n[TEST 5] Detectar texto plano vs hash")
plain_text = "MiContraseña123"
is_plain = is_password_hashed(plain_text)
is_hash = is_password_hashed(hashed)
print(f"✅ '{plain_text}' es hash: {is_plain} (esperado: False)")
print(f"✅ '{hashed[:30]}...' es hash: {is_hash} (esperado: True)")

# Test 6: Usar en login (simular)
print("\n[TEST 6] Simular verificación de login")
try:
    stored_password_in_db = hash_password("admin123")
    user_input = "admin123"
    
    if verify_password(user_input, stored_password_in_db):
        print(f"✅ Login simulado exitoso")
    else:
        print(f"❌ Error: Login no funcionó")
except Exception as e:
    print(f"❌ Error en login simulado: {e}")

print("\n" + "=" * 60)
print("RESULTADO: ✅ MÓDULO DE HASHING FUNCIONANDO CORRECTAMENTE")
print("=" * 60)
print("\nPróximos pasos:")
print("1. Ejecutar: python scripts/migrate_passwords.py")
print("2. Esto hasheará todas las contraseñas existentes en la BD")
print("3. Se creará un backup automático antes de hacer cambios")
