# CREACIÓN DE PROYECTO BACKEND CON DJANGO Y DRF

## 1. Instalación de python en windows
* Descargar [python 3.14.2](https://www.python.org/downloads/windows/)
* Recordar activar check para las variables de entorno.
* Instalar python.
* Verificar la version instalada con ```python --version```

## 2. Verificar que venv está instalado y accesible
*   Digitar el siguiente comando ```python -m venv --help```

    A partir de Python 3.3, venv viene incluido por defecto, así que si tienes Python instalado.
        
    Si venv está disponible, verás la documentación del módulo. Si no, recibirás un error como No module named venv.

## 3. Crear el entorno virtual entorno_yakuwise
*   Ejecutar el siguiente comando ```python -m venv nombre_de_entorno```

## 4. Activar entorno virtual
*   Ejecutar el siguiente comando ```.\nombre_de_entorno\Scripts\activate```

## 5. Instalar django 5.2.9
*   Ejecutar el siguiente comando ```py -m pip install Django==5.2.9```

## 6. Crear un proyecto con django
* Ejecuta el siguiente comandodo ```django-admin startproject backend```

## 7. Genera el archivo requirements.txt
* Ubicarse en el proyecto creado
* Crea un archivo con las librerías utilizadas en el entorno_proyecto
* Ejecutar el siguiente comando ```python -m pip freeze -> requirements.txt```

## 8. Crear una aplicación en nuestro proyecto
* Desde su terminal (CMD o PowerShell), navegue hasta el directorio raíz de su proyecto Django (donde se encuentra el archivo manage.py) y ejecute el siguiente comando:
    ```python manage.py startapp users```

* Agregar a INSTALLED_APPS de settings.py de la carpeta del proyecto la nueva aplicación creada denominada ```'users'```.

## 9. Instalar Django Rest Framework 3.16.1
* Ejecutar el siguiente comando ```pip install djangorestframework```

* Debes avisarle a Django que ahora cuenta con las funcionalidades de DRF. Abre tu archivo config/settings.py y busca la lista INSTALLED_APPS: 
    ```
        INSTALLED_APPS = [
        ...
        'django.contrib.staticfiles',
        'rest_framework',  # <--- Agrega esta línea
        'apps.usuarios',   # Asegúrate de que tus apps locales estén aquí
    ```

## 10. Crear los archivos faltantes:
Crear los archivos ```urls.py``` y ```serializer.py``` en la aplicacion denominada usuarios.

## 11. Actualizar los requerimientos del proyecto
* ### 11.1. Actualizar requirements.txt
    Ejecutar el siguiente comando  ```pip freeze -> requirements.txt```

* ### 11.2. Listar librerías instaladas en el proyecto
    Para ello, digitar el siguiente comando: ```pip list```  que  es lista los paquetes con sus números de versión.

## 12. Conexion postgresql y django
* Previamente, instalar postgresql, crear la base de datos.

* Instalar psycopg 3, ejecutando  ```pip install "psycopg[binary]"```

* Actualizar los requerimientos  ```pip freeze -> requirements.txt```

* Listar ```pip freeze```

    | Package             | Version|
    |-------------------- |--------|
    | asgiref             | 3.11.0 |
    | Django              | 5.2.9  |
    | djangorestframework | 3.16.1 |
    | pip                 | 25.3   |
    | psycopg             | 3.3.2  |
    | psycopg-binary      | 3.3.2  |
    | sqlparse            | 0.5.4  |
    | tzdata              | 2025.2 |

* Crear la base de datos y sus tablas en postgreSQL

* En tu proyecto Django, asegúrate de tener instalado el adaptador necesario y configurar el archivo settings.py:
    ```
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'tu_nombre_db',
                'USER': 'tu_usuario',
                'PASSWORD': 'tu_password',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
    ```
## 13. Crear modelos en models.py de la aplicacion creada
* Digita el comando : ```python manage.py inspectdb > nombre_app/models.py```

## 14. Ejecutar la migracion las tablas 
* Primero ejecutar esto ```python manage.py makemigrations```

* Ejecutar el siguiente comando: ```python manage.py migrate```

## 15. Ejecutar el proyecto
* Navegue al directorio donde se encuentra el archivo manage.py y ejecute:

    ```python manage.py runserver ```

## 16. Crear el archivo .gitignore
* Ignorar la carpeta del entorno virtual y otros
    ```venv/```

    ```env/ ```

