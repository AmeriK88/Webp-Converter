# WebP Converter - Refactored Structure

Proyecto refactorizado con una estructura modular y escalable para Flask.

## 📁 Estructura del Proyecto

```
project/
├─ run.py                    # Punto de entrada de la aplicación
├─ config.py                # Configuración centralizada
├─ requirements.txt         # Dependencias del proyecto
├─ app/
│  ├─ __init__.py          # App factory (create_app)
│  ├─ extensions.py        # Extensiones (db, login_manager, etc.)
│  ├─ web/
│  │  ├─ __init__.py       # Blueprint definition
│  │  ├─ routes.py         # Rutas web (endpoints)
│  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ image_service.py  # Lógica de conversión WebP
│  ├─ utils/
│  │  ├─ __init__.py
│  │  ├─ files.py          # Validaciones y utilidades de archivos
│  ├─ templates/
│  │  └─ index.html        # Template principal
│  ├─ static/
│  │  ├─ script.js         # JS del cliente
│  │  ├─ styles.css        # Estilos CSS
│  └─ uploads/             # Carpeta de descargas de imágenes
└─ README.md               # Este archivo
```

## 🚀 Cómo Ejecutar

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🔧 Configuración

### Variables de entorno

Puedes configurar la aplicación mediante variables de entorno:

```bash
# Cambiar el entorno (development/production)
set FLASK_ENV=development

# Cambiar la carpeta de uploads
set UPLOAD_FOLDER=C:/mi/carpeta/uploads

# Cambiar la clave secreta
set FLASK_SECRET_KEY=mi_clave_secreta_aquí
```

### En `config.py`

- `SECRET_KEY`: Clave secreta para sesiones (por defecto: "change_me")
- `UPLOAD_FOLDER`: Carpeta donde se guardan las imágenes convertidas
- `ALLOWED_EXTENSIONS`: Extensiones permitidas para subir
- `MAX_CONTENT_LENGTH`: Tamaño máximo de archivo (50MB por defecto)

## 📚 Estructura de Carpetas - Propósito de Cada Módulo

### `app/__init__.py` (App Factory)
Define la función `create_app()` que:
- Crea la instancia de Flask
- Carga la configuración
- Registra blueprints
- Asegura que exista la carpeta de uploads

### `config.py`
Centraliza toda la configuración:
- Rutas de carpetas
- Extensiones permitidas
- Configuración de seguridad

### `app/utils/files.py`
Funciones auxiliares para:
- Validar extensiones de archivo
- Sanitizar nombres de archivo

### `app/services/image_service.py`
Lógica de negocio para:
- Convertir imágenes a WebP
- Validar archivos
- Gestionar la carpeta de uploads

### `app/web/routes.py`
Endpoints HTTP:
- GET `/` - Mostrar formulario
- POST `/convert` - Convertir imágenes
- GET `/uploads/<filename>` - Servir imágenes convertidas

### `app/web/__init__.py`
Define y exporta el blueprint `web_bp`

## 🔀 Migración desde la versión antigua

Si tenías el código en `app.py`, la refactorización ha:

1. ✅ Extraído la configuración a `config.py`
2. ✅ Separado las rutas a `app/web/routes.py`
3. ✅ Movido la lógica de conversión a `app/services/image_service.py`
4. ✅ Creado utilidades en `app/utils/files.py`
5. ✅ Centralizado la creación de la app en `app/__init__.py`

**Los archivos antiguos (`app.py`, `static/`, `templates/`) pueden ser eliminados si la nueva estructura funciona correctamente.**

## 🎯 Ventajas de esta estructura

- ✅ **Escalable**: Fácil de agregar nuevas características
- ✅ **Mantenible**: Código organizado por responsabilidad
- ✅ **Testeable**: Módulos independientes y reutilizables
- ✅ **Profesional**: Sigue convenciones de proyectos Flask grandes
- ✅ **Configurable**: Soporta múltiples entornos

## 📝 Notas

- Si necesitas agregar una base de datos, usa `app/extensions.py` para inicializar SQLAlchemy
- Para agregar autenticación, crea un nuevo blueprint en `app/auth/`
- Los servicios adicionales pueden ir en `app/services/`
- Los modelos pueden ir en `app/models/` si es necesario

## ⚙️ Desarrollo futuro

Para expandir el proyecto:

1. **Agregar DB**: Crear `app/models/` y usar `app/extensions.py`
2. **Agregar autenticación**: Crear `app/auth/routes.py` y `app/auth/__init__.py`
3. **Agregar API**: Crear `app/api/routes.py` en un blueprint separado
4. **Agregar tests**: Crear carpeta `tests/` con tests unitarios

---

**Versión refactorizada**: Feb 2026
