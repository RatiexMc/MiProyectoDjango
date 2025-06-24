# Proyecto Django - Biblioteca de Libros

Esta plataforma web permite gestionar una biblioteca digital con libros en formato `.epub`. Los usuarios pueden registrarse, iniciar sesión y realizar acciones como subir, editar o eliminar libros. También dispone de una API REST protegida para integraciones externas.
Cuenta con:
- Registro y autenticación de usuarios (vía sesión y JWT)
- Búsqueda de libros por autor y nombre
- Gestión de visualizar, modificar, eliminar o descargar libros
- Subida de libros en formato `.epub`
- Creación de nuevos autores y géneros
- Calificación y reseñas a cualquier libros
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
    .\venv\Scripts\activate # En Windows
   ```

4. Instala las dependencias que se crearon con:
   ```bash
   pip freeze > requirements.txt
   ```
   Se pueden instalar con:
   ```bash
   pip install -r requirements.txt
   ```

5. Crea la base de datos en PostgreSQ abriendo la terminal y escribe:

   ```bash
   CREATE DATABASE midbdjango;
   ```
   ![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/CREATEDATABASE.png)

6. Configura los parámetros en `miApp/settings.py`. 
   ```python
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
```python
...
# Listar y crear libros
class LibroListCreateView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
...
```
![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/CREAR%20UN%20LIBRO.png
)

###  Listado de Libros

```http
GET http://127.0.0.1:8000/api/libros/libros/
```
```python
...
# Listar y crear libros
class LibroListCreateView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
...
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



## Documentación del Scripts 'conversor.py'
El archivo conversor.py está diseñado para interactuar con una base de datos de Django y exportar la información de modelos como Libros y  CalificacionUsuario a archivos .csv. Esto permite su posterior análisis con herramientas como pandas, facilitando la generación de gráficos  y estadísticas

### Sus principales funciones son:
 - db_to_csv: Exporta datos de libros (con autor, géneros, vistas y calificaciones) a un CSV.
 - reviews_to_csv: Exporta el número de calificaciones hechas por cada usuario.
 - csv_to_dataframe: Carga el archivo CSV de libros a un DataFrame de pandas.
 - reviews_dataframe: Carga el archivo CSV de calificaciones a un DataFrame.

¿Porque utilizamos pandas?
- Utilizamos pandas por la estructura de datos, en nuestro caso Dataframe, que nos permite organizar los datos extraídos en una estructura tabular(filas y columnas)
- Nos proporciona `to_csv()` que permite guardar un Dataframe como archivo `.csv` directamente en una línea de código, simplificando y automatizando el proceso
- Los métodos de `read_csv()` de pandas permiten cargar directamente para el análisis directamente y posterior, lo que es más fluida y flexible que manejar el archivo línea por línea
- Nos permite agrupar facilmente con `groupby`, analizarla con `mean(), count()` y visuarlizarla con `matplotlib, seaborn, etc`
- Y es ampliamente compatible en la cienca de datos y el aprendizaje automático, puede integrarse fácilmente con bibliotecas como `scikit-learns, plotly, statsmodels, etc`

### Scripts conversor.py con comentarios explicativos
```bash
# Importación de librerías estándar
import os
import django
import pandas as pd
from django.db import models

# Configura las variables de entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miApp.settings')
django.setup()

# Importación de modelos desde la app 'libros'
from libros.models import Libro, CalificacionUsuario
from django.conf import settings

# Función para exportar información de libros a un archivo CSV
def db_to_csv(csv_path=None):
    # Si no se especifica una ruta, se guarda por defecto en MEDIA_ROOT
    if csv_path is None:
        csv_path = settings.MEDIA_ROOT / 'db_export.csv'
    
    data = []
    
    # Recorre todos los libros registrados en la base de datos
    for libro in Libro.objects.all():
        # Obtiene los nombres de los géneros asociados y los une en una sola cadena
        generos = ','.join(libro.generos.values_list('nombre', flat=True))
        
        # Calcula el promedio y la cantidad de calificaciones del libro
        calif_data = libro.calificaciones_usuario.aggregate(
            avg=models.Avg('calificacion'), 
            count=models.Count('id')
        )
        
        calif_avg = calif_data['avg']
        calif_count = calif_data['count']
        
        # Agrega los datos del libro al listado
        data.append({
            'id': libro.id,
            'nombre': libro.nombre,
            'autor': libro.autor.nombre,
            'generos': generos,
            'fecha_lanzamiento': libro.fecha_lanzamiento,
            'vistas': libro.vistas,
            'calificacion_media': calif_avg if calif_avg is not None else 0,
            'calificaciones_count': calif_count,
        })

    # Convierte los datos en un DataFrame de pandas
    df = pd.DataFrame(data)

    # Exporta el DataFrame a un archivo CSV
    df.to_csv(csv_path, index=False)
    return csv_path

# Función para exportar la cantidad de reseñas por usuario
def reviews_to_csv(csv_path=None):
    """Exporta la cantidad de reseñas realizadas por cada usuario."""
    if csv_path is None:
        csv_path = settings.MEDIA_ROOT / 'reviews.csv'
    
    # Agrupa por nombre de usuario y cuenta la cantidad de calificaciones
    qs = (
        CalificacionUsuario.objects
        .values('usuario__username')
        .annotate(count=models.Count('id'))
        .order_by('-count')
    )

    data = list(qs)

    # Crea un DataFrame con los datos obtenidos
    df = pd.DataFrame(data, columns=['usuario__username', 'count'])

    # Exporta los datos a un archivo CSV
    df.to_csv(csv_path, index=False)
    return csv_path

# Función para leer el archivo CSV de libros y devolver un DataFrame
def csv_to_dataframe(csv_path=None):
    if csv_path is None:
        csv_path = settings.MEDIA_ROOT / 'db_export.csv'
    return pd.read_csv(csv_path)

# Función para leer el archivo CSV de reseñas y devolver un DataFrame
def reviews_dataframe(csv_path=None):
    if csv_path is None:
        csv_path = settings.MEDIA_ROOT / 'reviews.csv'
    return pd.read_csv(csv_path)

# Ejecución directa del script
if __name__ == '__main__':
    path_books = db_to_csv()
    path_reviews = reviews_to_csv()
    print(f'Datos exportados a {path_books} y {path_reviews}')
  ```



## Resultados y Explicación de los Gráficos

### Salida de resultados a respuestas como:

- ¿Cual es el género más libros guardado?
- ¿Cual es el género menos libros guardados?
- ¿Cual es el libro con mejor calificación?
- ¿Cual es el libro con peor calificación?
- ¿Cual es el usuario que mas reseñas realizó?
  
![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/SALIDA.png
)

- ¿Cuales libros no fueron calificados?

![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/LibrosSinCalificar.png
)

-¿Cuantos libros hay por género?

![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/CantidadDeLibroXGenero.png
)

-¿Cual es el promedio del top 10 mejores libros calificados?

![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/Top10LibrosXCalificaciones.png
)

-¿Cuantas reseñas hay por usuarios?

![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/CantidadRese%C3%B1asXUsuario.png
)

-¿Cual es el top 10 libros con mayores reseñas?

![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/Rese%C3%B1asXLibro.png
)

-¿Cual es el promedio de calificaciones por autores?

![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/PromediodeCalificacionesXAutor.png
)

-¿Cual es el promedio de calificaciones por género?

![Descripción de la imagen](https://github.com/RatiexMc/MiProyectoDjango/blob/master/img_readme/PromediodeCalificacionesXGenero.png
)









## Licencias de los paquetes utilizados:
Este proyecto esta sujeta bajo los términos de la licencia MIT y utiliza las siguientes bibliotecas de código abierto sujeto a licencias propias
Puedes utilizar, copiar, editar y distribuir este software con o sin fines comerciales, siempre que tengas aviso del copyright original

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
