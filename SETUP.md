# SETUP - CREACIÓN DEL PROYECTO DESDE CERO

Esta guía es para crear el proyecto backend Django + DRF desde cero.

## 1. Instalación de Python en Windows
- Descargar [Python 3.14.2](https://www.python.org/downloads/windows/)
- Activar el checkbox para agregar Python a las variables de entorno
- Instalar Python
- Verificar la versión: `python --version`

## 2. Verificar venv
- Ejecutar: `python -m venv --help`
- A partir de Python 3.3, venv viene incluido por defecto

## 3. Crear entorno virtual
- Ejecutar: `python -m venv entorno_yakuwise`

## 4. Activar entorno virtual
- Ejecutar: `.\entorno_yakuwise\Scripts\activate`

## 5. Instalar Django
- Ejecutar: `py -m pip install Django==5.2.9`

## 6. Crear proyecto Django
- Ejecutar: `django-admin startproject backend`

## 7. Generar requirements.txt
- Ubicarse en el proyecto creado
- Ejecutar: `python -m pip freeze > requirements.txt`

## 8. Crear aplicación
- Desde el directorio raíz (donde está manage.py):
  ```bash
  python manage.py startapp users
  ```
- Agregar a `INSTALLED_APPS` en `settings.py`: `'users'`

## 9. Instalar Django Rest Framework
- Ejecutar: `pip install djangorestframework`
- Agregar a `INSTALLED_APPS` en `settings.py`:
  ```python
  INSTALLED_APPS = [
      ...
      'rest_framework',
      'apps.usuarios',
  ]
  ```

## 10. Crear archivos faltantes
- Crear `urls.py` y `serializers.py` en la aplicación

## 11. Actualizar requerimientos
- Ejecutar: `pip freeze > requirements.txt`
- Verificar: `pip list`

## 12. Instalar PostgreSQL
- Instalar PostgreSQL
- Crear la base de datos

## 13. Instalar psycopg3
- Ejecutar: `pip install "psycopg[binary]"`
- Actualizar: `pip freeze > requirements.txt`

## 14. Configurar base de datos en settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tu_nombre_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c client_encoding=UTF8'
        }
    }
}
```

## 15. Crear modelos
- Definir modelos en `models.py` de la aplicación

## 16. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## 17. Crear fixtures
- Crear directorio `fixtures/`
- Crear archivos JSON con datos iniciales
- Ejemplo: `python manage.py dumpdata security.Rol --indent 2 > fixtures/rol.json`

## 18. Ejecutar proyecto
```bash
python manage.py runserver
```

## 19. Crear .gitignore
```
venv/
env/
__pycache__/
*.pyc
.env
```

## 20. Instalar formateadores de código
```bash
pip install isort black flake8
pip freeze > requirements_dev.txt
```

Para usar:
```bash
isort .
black .
flake8 .
```
