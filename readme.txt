# CREACIÓN DE PROYECTO BACKEND CON DJANGO Y DRF
# --- Entorno virtual ---
## Instalar pyenv
sudo apt install pyenv
## Instalar la version de python con la que se creará el entorno virtual
pyenv install 3.13.5
## Actualizar lista de versiones de python disponibles
cd ~/.pyenv
git pull
pyenv install --list | grep 3.13
## Crear un envtorno virtual con la version especifica de python con pyenv
pyenv virtualenv 3.13.5 entorno_yakuwise
## Activar entorno virtual
pyenv activate entorno_yakuwise

# --- Django ---
## Instalar django
pip install django
## Crear un archivo con las librerías utilizadas en el entorno_proyecto
pip freeze -> requirements.txt
## Crear un proyecto con django
django-admin startproject backend .
## Crear una aplicación en nuestro proyecto
python manage.py startapp onlineshop
## Crear los archivos faltantes: urls.py y serializer.py
## Agregar a INSTALLED_APPS de settings.py de la carpeta del proyecto la nueva aplicación creada
## Crear modelos en models.py y ejecutar
python manage.py makemigrations
python manage.py migrate

# --- Django Rest Framework ---
## Instalar django rest framework
pip install djangorestframework

# --- Requerimientos del proyecto ---
## Actualizar requirements.txt
pip freeze -> requirements.txt

## Listar librerías instaladas en el proyecto
pip list // lista de paquetes con sus números de versión
pip show // muestra información sobre un paquete especifico
