# 🔒 Guía de Implementación: Headers de Seguridad y CORS

## ✅ ¿Qué se Implementó?

Se ha añadido una **capa de seguridad integral** a tu aplicación Flask que incluye:

### 1. **Security Headers HTTP**
Protección contra ataques comunes automáticamente añadida a cada respuesta:

| Header | Propósito | Valor |
|--------|-----------|-------|
| `X-Content-Type-Options` | Previene MIME-sniffing | `nosniff` |
| `X-Frame-Options` | Previene clickjacking | `SAMEORIGIN` |
| `X-XSS-Protection` | Protección XSS (navegadores antiguos) | `1; mode=block` |
| `Content-Security-Policy` | Controla qué recursos se pueden cargar | Restrictivo por defecto |
| `Referrer-Policy` | Controla información de referrer | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Deshabilita features peligrosas | Geolocalización, cámara, micrófono |
| `Strict-Transport-Security` | Fuerza HTTPS | Solo en producción |

### 2. **CORS Configuration**
Control flexible de solicitudes desde otros dominios:
- ✅ Configuración por entorno (.env)
- ✅ Métodos permitidos: GET, POST, PUT, DELETE, PATCH, OPTIONS
- ✅ Headers personalizables
- ✅ Credenciales habilitadas para solicitudes autenticadas
- ✅ Cache de 24 horas

### 3. **Session Security**
Protección de cookies de sesión:
- ✅ `HTTPONLY`: No accesible desde JavaScript (previene robo XSS)
- ✅ `SAMESITE=Lax`: Protección contra CSRF
- ✅ `SECURE`: Solo HTTPS en producción
- ✅ Expiración: 1 hora
- ✅ Refresh automático en cada request

### 4. **Protecciones Adicionales**
- ✅ Validación de tamaño de payload (máx 10MB)
- ✅ Caching deshabilitado para rutas sensibles (/login, /logout, /api/)
- ✅ Checks de seguridad before_request

---

## 📝 Cómo Usar

### Paso 1: Copiar archivo .env
```bash
cp .env.example .env
```

### Paso 2: Configurar CORS Origins
Edita `.env` y ajusta según tu entorno:

**Para desarrollo local:**
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:4000
```

**Para producción:**
```env
CORS_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
```

### Paso 3: Verificar que funcione

Reinicia tu aplicación:
```bash
python src/app.py
```

Verifica los headers en tu navegador:
1. Abre DevTools (F12)
2. Ve a Network
3. Haz un request
4. Revisa la pestaña "Response Headers"

Deberías ver todos los security headers listados arriba.

---

## 🔍 Verificación de Security Headers

**Test local con curl:**
```bash
curl -I http://localhost:4000/
```

Deberías ver:
```
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'; ...
```

**Test online (recomendado):**
- Sube a producción y testa en https://securityheaders.com
- Score esperado: A+ (con HTTPS y HSTS en producción)

---

## ⚙️ Configuración Avanzada

### Modificar Content Security Policy

Edita `src/security.py` si necesitas permitir recursos externos:

```python
response.headers['Content-Security-Policy'] = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://cdn.example.com; "  # Agregar CDN
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data: https:; "  # Permitir imágenes HTTPS
    ...
)
```

### Agregar Dominios CORS Dinámicamente

En `.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:4000,https://tu-dominio.com,https://api.tu-dominio.com
```

### Cambiar Duración de Session

En `src/security.py`:
```python
app.config['PERMANENT_SESSION_LIFETIME'] = 7200  # 2 horas en lugar de 1
```

---

## 🚨 Notas Importantes

1. **CSP puede romper cosas:**
   - Si usas `eval()` o `onclick="..."` inline, CSP lo bloqueará
   - Solución: Mover a ficheros `.js` separados

2. **CORS_ORIGINS debe ser específico:**
   - ❌ NO: `*` (acepta cualquier origen)
   - ✅ SÍ: `https://tu-dominio.com`

3. **En producción:**
   - Activa `HTTPS` (HSTS se activará automáticamente)
   - Usa dominios específicos en CORS
   - Prueba en https://securityheaders.com

4. **Para APIs con Frontend separado:**
   - El frontend debe estar en la lista de `CORS_ORIGINS`
   - Ejemplo:
     ```env
     CORS_ORIGINS=https://frontend.tu-dominio.com,https://api.tu-dominio.com
     ```

---

## 📊 Checklist Post-Implementación

- [ ] ✅ Instalar Flask-CORS y python-dotenv
- [ ] ✅ Crear archivo `.env` desde `.env.example`
- [ ] ✅ Configurar `CORS_ORIGINS` según entorno
- [ ] ✅ Reiniciar aplicación
- [ ] ✅ Verificar headers con curl o DevTools
- [ ] ✅ Probar CORS desde frontend (si existe)
- [ ] ⬜ Implementar HTTPS (FASE 6: Deployment)
- [ ] ⬜ Cambiar secret key desde .env (FASE 1: Seguridad)

---

## 🔗 Próximos Pasos

Continuaremos con **FASE 1: Seguridad Crítica**:
1. Secret key desde variables de entorno
2. Hashing de contraseñas (werkzeug.security)
3. Validación de entrada mejorada

**¿Quieres continuar con la FASE 1?**
