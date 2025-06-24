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
