## Restful API 

**Descripción del Proyecto**

Resful Api enfocada en crear, leer, actualizar y eliminar(CRUD), conjuntos de datos almacenados en una base de datos, en este caso, esta API esta enfocada en administrar informacion de imagenes.

## Tecnologías y Librerías Usadas

- La API está construida con:

- Django

- Django Rest Framework

- Psycopg2 (Adaptador de Python para PostgresSQL)

- Django Filter

- Numpy

## Logs

Se creo un archivo contante que permite almacenar solicitudes y respuestas del backend, este se encuentra dentro de la carpeta logs

## Instalación

Sigue estos pasos para configurar y ejecutar la API:

- Ingresar a la carpeta de la API 

cd Restful API

- Crear un entorno virtual

python -m venv env

- Activa el entorno virtual

Windows: env\Scripts\activate

- Instalar dependencias

pip install django djangorestframework psycopg2-binary numpy django-filter

- Configurar la base de datos

En el archivo settings.py de la carpeta api se debe de cambiar los valores del objeto DATABASES de esta manera:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'api',
        'USER': '', // En esta parte se ingresa el usario de postgres
        'PASSWORD': '', // Se ingresa la contraseña del usuario
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

- Aplicar migraciones

Correr en la terminal los comandos:

python manage.py makemigrations

python manage.py migrate

- Ejecutar el servidor

correr el comando:

python manage.py runserver

**Opcional**

- Crear un superuser para visualizar datos en el admin de django

python manage.py createsuperuser

## Endpoints

## POST

Endpoint para la creacion de registros en la base de datos

**POST** http://127.0.0.1:8000/api/images/

Dentro de la solicitud se envian los datos que se desean registrar, por ejemplo:

{
    "1": {
        "id": "aabbcc1",
        "data": [
            "53 26 49 33 45 80 68 85 38 98",
            "26 55 85 77 92 82 69 54 95 42",
            "18 94 43 82 82 88 75 95 90 90",
            "96 97 82 91 63 43 74 97 97 50",
            "64 73 54 12 26 91 39 75 12 70"
        ],
        "deviceName": "CT SCAN"
    },
    "2": {
        "id": "aabbcc2",
        "data": [
            "82 66 26 64 67 18 59 50 18 17",
            "4 8 51 9 51 65 32 22 80 7",
            "76 96 26 71 60 61 67 92 68 45",
            "20 11 16 11 30 4 85 73 46 15",
            "84 49 98 100 75 79 55 5 12 54"
        ],
        "deviceName": "MRI"
    },
}

## GET

Endpoints enfocados a solicitar registros en la base de datos, en este caso existen 12 endpoints para consultar datos, esto por la implementacion de filtros

- Para traer todos los datos

**GET** http://127.0.0.1:8000/api/images/

- Para traer un solo dato por el ID

**GET** http://127.0.0.1:8000/api/images/aabbcc2/

- Para traer todos los datos que su media antes de la normalizacion sea mayor o igual a:

**GET** http://127.0.0.1:8000/api/images/?average_before_normalization_gte=52

- Para traer todos los datos que su media antes de la normalizacion sea menor o igual a:

**GET** http://127.0.0.1:8000/api/images/?average_before_normalization_lte=52

- Para traer todos los datos que su media despues de la normalizacion sea mayor o igual a:

**GET** http://127.0.0.1:8000/api/images/?average_after_normalization_gte=1

- Para traer todos los datos que su media despues de la normalizacion sea menor o igual a:

**GET** http://127.0.0.1:8000/api/images/?average_after_normalization_lte=1

- Para traer todos los datos que hayan sido creados despues de

**GET** http://127.0.0.1:8000/api/images/?created_date_gte=2023-10-01

- Para traer todos los datos que hayan sido creados antes de

**GET** http://127.0.0.1:8000/api/images/?created_date_lte=2023-10-01

- Para traer todos los datos que hayan sido actualizados despues de

**GET** http://127.0.0.1:8000/api/images/?updated_date_gte=2023-10-01

- Para traer todos los datos hayan sido actualizados antes de

**GET** http://127.0.0.1:8000/api/images/?updated_date_lte=2023-10-01

- Para traer todos los datos que el tamaño sea mayor o igual a

**GET** http://127.0.0.1:8000/api/images/?data_zise_gte=31

- Para traer todos los datos que el tamaño sea menor o igual a

**GET** http://127.0.0.1:8000/api/images/?data_zise_lte=31

## PUT

Endpoint enfocado a actualizar registros en la base de datos

**PUT** http://127.0.0.1:8000/api/images/aabbcc1/

Dentro de la solicitud se envian los datos que se desean actualizar, por ejemplo:

{
    "deviceName": "MRI"
}

## DEL

Endpoint enfocado en la eliminacion de registros en la base de datos

**DEL** http://127.0.0.1:8000/api/images/aabbcc1/

Esto abrirá la aplicación en http://localhost:4200/