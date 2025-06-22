"""Utilidades para exportar los datos de la base de datos a CSV
y cargar dicho CSV en un DataFrame de pandas."""

import os
import django
import pandas as pd
from django.db import models

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miApp.settings')
django.setup()

from libros.models import Libro, CalificacionUsuario
from django.conf import settings


def db_to_csv(csv_path=None):
    if csv_path is None:
        csv_path = settings.MEDIA_ROOT / 'db_export.csv'
    data = []
    for libro in Libro.objects.all():
        generos = ','.join(libro.generos.values_list('nombre', flat=True))
        calif_data = libro.calificaciones_usuario.aggregate(
            avg=models.Avg('calificacion'), count=models.Count('id'))
        calif_avg = calif_data['avg']
        calif_count = calif_data['count']
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
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    return csv_path


def reviews_to_csv(csv_path=None):
    """Exporta la cantidad de reseñas realizadas por cada usuario."""
    if csv_path is None:
        csv_path = settings.MEDIA_ROOT / 'reviews.csv'
    
    qs = (
        CalificacionUsuario.objects
        .values('usuario__username')
        .annotate(count=models.Count('id'))
        .order_by('-count')
    )
    data = list(qs)
    df = pd.DataFrame(data, columns=['usuario__username', 'count'])
    df.to_csv(csv_path, index=False)
    return csv_path


def csv_to_dataframe(csv_path=None):
    if csv_path is None:
        csv_path = settings.MEDIA_ROOT / 'db_export.csv'
    return pd.read_csv(csv_path)


def reviews_dataframe(csv_path=None):
    if csv_path is None:
        csv_path = settings.MEDIA_ROOT / 'reviews.csv'
    return pd.read_csv(csv_path)


if __name__ == '__main__':
    path_books = db_to_csv()
    path_reviews = reviews_to_csv()
    print(f'Datos exportados a {path_books} y {path_reviews}')