# Proyecto Django - Biblioteca de Libros

Esta plataforma web permite gestionar una biblioteca digital con libros en formato `.epub`. Los usuarios pueden registrarse, iniciar sesión y realizar acciones como subir, editar o eliminar libros. También dispone de una API REST protegida para integraciones externas.
Cuenta con:
- Registro y autenticación de usuarios (vía sesión y JWT)
- Búsqueda de libros por autor y nombre
- Gestión de libros, autores y libros
- Subida de libros en formato `.epub`
- Calificación y reseñas de libros
- Estadísticas con gráficos a partir de `conversor.py`


## Librerías utilizadas:
```bash
asgiref==3.8.1
certifi==2025.4.26
charset-normalizer==3.4.2
contourpy==1.3.2
cycler==0.12.1
Django==5.2.1
django-widget-tweaks==1.5.0
djangorestframework==3.16.0
djangorestframework_simplejwt==5.5.0
fonttools==4.58.4
idna==3.10
kiwisolver==1.4.8
matplotlib==3.10.3
numpy==2.3.1
packaging==25.0
pandas==2.3.0
pillow==11.2.1
psycopg2==2.9.10
psycopg2-binary==2.9.10
PyJWT==2.9.0
pyparsing==3.2.3
python-dateutil==2.9.0.post0
python-decouple==3.8
pytz==2025.2
requests==2.32.3
six==1.17.0
sqlparse==0.5.3
tzdata==2025.2
urllib3==2.4.0
```

## Pasos para probar el proyecto
1. Asegúrate de tener **Python**, **pip** y **PostgreSQL** instalados.

2. Clona o descarga el repositorio y abre una terminal en la carpeta raíz.

3. Crea un entorno virtual y activa el entorno virtual:
   ```bash
   python -m venv venv
   `.\venv\Scripts\activate` # En Windows
   ```

4. Instala las dependencias que se crearon con:
   ```bash
   pip freeze > requirements.txt
   ```

5. Se pueden instalar con:
   ```bash
   pip install -r requirements.txt
   ```

6. Crea la base de datos en PostgreSQ abriendo la terminal y escribe:

   ```bash
   CREATE DATABASE midbdjango;
   ```
   ![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/CREATEDATABASE.png)

7. Configura los parámetros en `miApp/settings.py`. 
   ```bash
    DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql',
        'NAME':'midbdjango',
        'USER':'juniorovs',
        'PASSWORD':'12345',
        'HOST':'localhost',
        'PORT':'5432',
   }
   }
   ```

7. Ejecuta las migraciones:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. Crea un superusuario:
   ```bash
   python manage.py createsuperuser
   ```

9. (Opcional) Carga usuarios de ejemplo:
   ```bash
   python manage.py populate_users
   ```

11. Ejecuta `python conversor.py` para generar estadísticas iniciales.

12. Inicia el servidor de desarrollo con `python manage.py runserver` y accede a `http://127.0.0.1:8000/`.

## API del Proyecto BIBLIOTECA

###  Registro de Libros

```http
POST http://127.0.0.1:8000/api/auth/register/
```
```bash
<<EL CODIGO DEL REGISTRO DE LIBROS VA AQUI>>
```
![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/CREAR%20UN%20LIBRO.png
)

###  Listado de Libros

```http
GET http://127.0.0.1:8000/api/libros/libros/
```
```bash
<<EL CODIGO DEL LISTADO DE LIBROS VA AQUI>>
```
![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/LISTAR%20TODOS%20LOS%20LIBROS.png
)

## Tabla de endpoints API
En el repositorio se incluyen dos colecciones para probar la API:

- `Libros.postman_collection.json`
- `SistemaLogin-Register.postman_collection.json`

La siguiente tabla resume las rutas principales disponibles en el proyecto. Puedes importarlas en Postman usando el archivo SistemaLogin y Libros en formato .json
Algunas de ellas son:

| Método | Ruta | Descripción |
|-------|------|-------------|
| POST | `/api/auth/register/` | Registro de usuarios |
| POST | `/api/auth/login/` | Obtiene un par de tokens JWT |
| POST | `/api/auth/token/refresh/` | Refresca el token JWT |
| GET, POST | `/api/libros/autores/` | Listar o crear autores |
| GET, PUT, DELETE | `/api/libros/autores/{id}/` | Detalle de autor |
| GET, POST | `/api/libros/generos/` | Listar o crear géneros |
| GET, PUT, DELETE | `/api/libros/generos/{id}/` | Detalle de género |
| GET, POST | `/api/libros/libros/` | Listar o crear libros |
| GET, PUT, DELETE | `/api/libros/libros/{id}` | Detalle de libro |
| GET, POST | `/api/libros/calificaciones/` | Listar o crear calificaciones |
| GET, PUT, DELETE | `/api/libros/calificaciones/{id}/` | Detalle de calificación |



## Uso de `conversor.py`
Este script exporta la información de la base de datos a CSV y carga los archivos en `pandas` para generar estadísticas y gráficos. Ejecuta:
```bash
python conversor.py
```


















## Licencias de dependencias
| Paquete | Versión | Licencia |
|---------|---------|---------|
| Django | 5.2.1 | BSD License |
| PyJWT | 2.9.0 | MIT License |
| asgiref | 3.8.1 | BSD License |
| certifi | 2025.4.26 | MPL-2.0 |
| charset-normalizer | 3.4.2 | MIT License |
| contourpy | 1.3.2 | BSD License |
| cycler | 0.12.1 | BSD License |
| django-widget-tweaks | 1.5.0 | MIT License |
| djangorestframework | 3.16.0 | BSD License |
| djangorestframework_simplejwt | 5.5.0 | MIT License |
| fonttools | 4.58.4 | MIT License |
| idna | 3.10 | BSD License |
| kiwisolver | 1.4.8 | BSD License |
| matplotlib | 3.10.3 | PSF License |
| numpy | 2.3.1 | BSD License |
| packaging | 25.0 | BSD/Apache License |
| pandas | 2.3.0 | BSD License |
| pillow | 11.2.1 | UNKNOWN |
| psycopg2 | 2.9.10 | LGPL |
| psycopg2-binary | 2.9.10 | LGPL |
| pyparsing | 3.2.3 | MIT License |
| python-dateutil | 2.9.0.post0 | BSD/Apache License |
| python-decouple | 3.8 | MIT License |
| pytz | 2025.2 | MIT License |
| requests | 2.32.3 | Apache 2.0 |
| six | 1.17.0 | MIT License |
| sqlparse | 0.5.3 | BSD License |
| tzdata | 2025.2 | Apache License |
| urllib3 | 2.4.0 | MIT License |

Consulta la documentación oficial de cada paquete para más detalles sobre sus licencias.
