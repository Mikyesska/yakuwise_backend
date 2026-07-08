# Yakuwise Backend

Backend Django + Django Rest Framework para el proyecto Yakuwise.

## Documentación

- **[SETUP.md](SETUP.md)** - Guía para crear el proyecto desde cero
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Guía para desarrolladores (levantar el proyecto existente)

## Resumen rápido

### Para levantar el proyecto (desarrolladores)

1. Clonar el repositorio
2. Crear y activar entorno virtual: `python -m venv entorno_yakuwise` y `.\entorno_yakuwise\Scripts\activate`
3. Instalar dependencias: `pip install -r requirements.txt` y `pip install -r requirements_dev.txt`
4. Configurar `.env` (copiar de `.env_example`)
5. Crear base de datos en PostgreSQL
6. Ejecutar migraciones: `python manage.py makemigrations` y `python manage.py migrate`
7. Cargar fixtures: `python manage.py loaddata fixtures/rol.json fixtures/tipo_documento.json`
8. Ejecutar servidor: `python manage.py runserver`

## Estructura del proyecto

```
yakuwise_backend/
├── bk_yakuwise/           # Proyecto Django principal
│   ├── apps/              # Aplicaciones internas
│   │   ├── security/      # Autenticación y roles
│   │   ├── cliente/       # Gestión de clientes
│   │   └── monitoreoparametro/
│   ├── fixtures/          # Datos iniciales (rol, tipo_documento)
│   ├── manage.py
│   └── yakuwise/          # Configuración
├── entorno_yakuwise/      # Entorno virtual
├── requirements.txt       # Dependencias de producción
├── requirements_dev.txt   # Dependencias de desarrollo
└── .env_example           # Ejemplo de variables de entorno
```

## Tecnologías

- Python 3.14.2
- Django 5.2.9
- Django Rest Framework 3.16.1
- PostgreSQL
- psycopg3
