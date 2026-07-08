# GETTING STARTED - LEVANTAR EL PROYECTO

Esta guía es para desarrolladores que necesitan levantar el proyecto existente en su entorno local.

## Requisitos previos
- Python 3.14.2 o superior
- PostgreSQL instalado y corriendo
- Git

## 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd yakuwise_backend
```

## 2. Crear y activar entorno virtual
```bash
python -m venv entorno_yakuwise
.\entorno_yakuwise\Scripts\activate
```

## 3. Instalar dependencias
```bash
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

## 4. Configurar variables de entorno
- Copiar el archivo de ejemplo: `cp .env_example .env`
- Editar `.env` con tus credenciales de base de datos:
  ```
  DB_NAME=nombre_db
  DB_USER=usuario
  DB_PASSWORD=password
  DB_HOST=localhost
  DB_PORT=5432
  DEBUG=True
  SECRET_KEY=tu_secret_key
  ALLOWED_HOSTS=localhost,127.0.0.1
  ```

## 5. Crear base de datos en PostgreSQL
```sql
CREATE DATABASE nombre_db;
```

## 6. Ejecutar migraciones
```bash
cd bk_yakuwise
python manage.py makemigrations
python manage.py migrate
```

## 7. Cargar fixtures (datos iniciales)
```bash
python manage.py loaddata fixtures/rol.json
python manage.py loaddata fixtures/tipo_documento.json
```

## 8. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

## 9. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## 10. Formatear código (opcional)
```bash
isort .
black .
flake8 .
```

## Estructura del proyecto
```
yakuwise_backend/
├── bk_yakuwise/           # Proyecto Django principal
│   ├── apps/              # Aplicaciones internas
│   │   ├── security/
│   │   ├── cliente/
│   │   └── monitoreoparametro/
│   ├── fixtures/          # Datos iniciales
│   ├── manage.py
│   └── yakuwise/          # Configuración
├── entorno_yakuwise/      # Entorno virtual (gitignore)
├── requirements.txt       # Dependencias de producción
├── requirements_dev.txt   # Dependencias de desarrollo
├── .env                   # Variables de entorno (gitignore)
└── .env_example           # Ejemplo de variables de entorno
```

## Troubleshooting

### Error de conexión a PostgreSQL
- Verifica que PostgreSQL esté corriendo
- Verifica las credenciales en `.env`
- Asegúrate de que la base de datos exista

### Error de migraciones
- Elimina la carpeta `migrations/` de cada app (excepto `__init__.py`)
- Ejecuta `python manage.py makemigrations` nuevamente
- Ejecuta `python manage.py migrate`

### Error de codificación de caracteres
- Verifica que la configuración de PostgreSQL use UTF-8
- El proyecto ya incluye `client_encoding=UTF8` en settings.py
