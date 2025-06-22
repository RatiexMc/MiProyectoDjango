# Importamos path para definir las rutas
from django.urls import path

# Importamos las vistas de la app libros
from .views import (
    AutorListCreateView,         # API: lista y crea autores
    LibroListCreateView,         # API: lista y crea libros
    LibroDetailView,             # API: detalle libro (GET, PUT, DELETE)
    GeneroListCreateView,        # API: lista y crea géneros
    CalificacionUsuarioListCreateView, # API: lista y crea calificaciones

    subir_libro,                 # Vista HTML: formulario para subir libro
    biblioteca_libros,           # Vista HTML: listado de libros (biblioteca)
    eliminar_libro,              # Vista HTML: eliminar libro
    editar_libro,                # Vista HTML: editar libro
    ver_libro,                   # Vista HTML: ver detalle de un libro
    calificar_libro,             # Vista HTML: calificar libro
    estadisticas_view,           # Vista HTML: estadísticas y gráficos

    AutorDetailView,             # API: detalle de autor (GET, PUT, DELETE)
    GeneroDetailView,            # API: detalle de género (GET, PUT, DELETE)
    CalificacionUsuarioDetailView # API: detalle de calificación (GET, PUT, DELETE)
)

# Definimos las rutas (endpoints)
urlpatterns = [
    # API REST
    path('autores/', AutorListCreateView.as_view(), name='lista_crear_autor'),
    path('libros/', LibroListCreateView.as_view(), name='lista_crear_libro'),
    path('libros/<int:pk>', LibroDetailView.as_view(), name='libro-detalle'),
    path('generos/', GeneroListCreateView.as_view(), name='genero_list_create'),
    path('calificaciones/', CalificacionUsuarioListCreateView.as_view(), name='calificacion_list_create'),

    # Vistas HTML
    path('subir/', subir_libro, name='subir_libro'),           # Formulario para subir libro
    path('', biblioteca_libros, name='biblioteca_libros'),     # Vista biblioteca (listado de libros)
    path('eliminar/<int:pk>/', eliminar_libro, name='eliminar_libro'), # Eliminar libro
    path('editar/<int:pk>/', editar_libro, name='editar_libro'),       # Editar libro
    path('ver/<int:pk>/', ver_libro, name='ver_libro'),               # Ver detalle de libro
    path('libros/<int:libro_id>/calificar/', calificar_libro, name='calificar_libro'), # Calificar libro
    path('estadisticas/', estadisticas_view, name='estadisticas'),  # Ver estadísticas

    # API REST (detalle)
    path('autores/<int:pk>/', AutorDetailView.as_view(), name='autor-detalle'),
    path('generos/<int:pk>/', GeneroDetailView.as_view(), name='genero-detalle'),
    path('calificaciones/<int:pk>/', CalificacionUsuarioDetailView.as_view(), name='calificacion-detalle'),
]
