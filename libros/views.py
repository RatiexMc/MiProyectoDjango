# Imports básicos
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LibroForm, CalificacionForm 
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .models import Autor, Libro, Genero, CalificacionUsuario
from .serializers import AutorSerializer, LibroSerializer, GeneroSerializer, CalificacionUsuarioSerializer
from django.db.models import Q
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated  # Protege las vistas API
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.conf import settings
from conversor import db_to_csv, reviews_to_csv

# ------------------------ Vistas API protegidas ------------------------

# Listar y crear autores
class AutorListCreateView(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

    def perform_create(self, serializer):
        # Asocia el autor al usuario que realiza la creación
        serializer.save(creado_por=self.request.user)

# Listar y crear géneros
class GeneroListCreateView(generics.ListCreateAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [IsAuthenticated]  # Requiere usuario autenticado

    def perform_create(self, serializer):
        # Asocia el género al usuario que realiza la creación
        serializer.save(creado_por=self.request.user)

# Listar y crear libros
class LibroListCreateView(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

# Obtener, actualizar, eliminar libro
class LibroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

# Listar y crear calificaciones de usuario
class CalificacionUsuarioListCreateView(generics.ListCreateAPIView):
    queryset = CalificacionUsuario.objects.all()
    serializer_class = CalificacionUsuarioSerializer

# Eliminar, actualizar, obtener autor por ID
class AutorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

# Eliminar, actualizar, obtener género por ID
class GeneroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer

# Eliminar, actualizar, obtener calificación por ID
class CalificacionUsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalificacionUsuario.objects.all()
    serializer_class = CalificacionUsuarioSerializer

# ------------------------ Vistas HTML ------------------------

# Subir un nuevo libro (vista con formulario HTML)
@login_required
def subir_libro(request):
    libro = None
    mensaje = None

    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        # Actualizamos queryset de autores y géneros
        form.fields['autor'].queryset = Autor.objects.all()
        form.fields['generos'].queryset = Genero.objects.all()

        if form.is_valid():
            libro = form.save()
            mensaje = "¡Libro subido correctamente!"
            form = LibroForm()  # Limpiamos formulario
    else:
        form = LibroForm()
        form.fields['autor'].queryset = Autor.objects.all()
        form.fields['generos'].queryset = Genero.objects.all()

    return render(request, 'libros/subir_libro.html', {
        'form': form,
        'libro': libro,
        'mensaje': mensaje
    })

# Calificar un libro (vista con formulario HTML)
@login_required
def calificar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.usuario = request.user
            calificacion.libro = libro
            calificacion.save()
            return redirect('ver_libro', pk=libro.id)
    else:
        form = CalificacionForm()

    return render(request, 'libros/calificar_libro.html', {
        'libro': libro,
        'form': form
    })

# Biblioteca de libros con buscador
@login_required
def biblioteca_libros(request):
    query = request.GET.get("q")
    if query:
        libros = Libro.objects.filter(
            Q(nombre__icontains=query) |
            Q(autor__nombre__icontains=query)
        )
    else:
        libros = Libro.objects.all()

    return render(request, 'libros/biblioteca_libros.html', {'libros': libros})

# Eliminar un libro
@login_required
def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    libro.delete()
    messages.success(request, "Libro eliminado correctamente.")
    return redirect('biblioteca_libros')

# Editar un libro
@login_required
def editar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    mensaje = None

    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            mensaje = "¡Libro actualizado correctamente!"
            return redirect('biblioteca_libros')
    else:
        form = LibroForm(instance=libro)

    return render(request, 'libros/editar_libro.html', {
        'form': form,
        'libro': libro,
        'mensaje': mensaje
    })

# Ver detalle del libro (con reseñas)
@login_required
def ver_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    reseñas = CalificacionUsuario.objects.filter(libro=libro).order_by('-fecha')
    return render(request, 'libros/ver_libro.html', {
        'libro': libro,
        'reseñas': reseñas
    })
# ---------- Vista de estadísticas ----------
@login_required
def estadisticas_view(request):
    """Muestra gráficos estadísticos generados a partir de los datos."""
    csv_path = settings.MEDIA_ROOT / 'db_export.csv'
    reviews_path = settings.MEDIA_ROOT / 'reviews.csv'
    # Si los archivos no existen o están vacíos, se recrean desde la base
    if (not csv_path.exists() or csv_path.stat().st_size == 0 or
            not reviews_path.exists() or reviews_path.stat().st_size == 0):
        db_to_csv(csv_path)
        reviews_to_csv(reviews_path)

    # Lectura de los CSV con pandas
    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()
    try:
        df_reviews = pd.read_csv(reviews_path)
    except pd.errors.EmptyDataError:
        df_reviews = pd.DataFrame()
    # Preparación de columnas de géneros
    df['generos'] = df['generos'].str.split(',')
    df_gen = df.explode('generos')

    # Conteo de libros por género
    genero_counts = df_gen['generos'].value_counts()
    # Conteo de reseñas realizadas por cada usuario
    if 'usuario__username' in df_reviews.columns:
        usuario_counts = df_reviews.set_index('usuario__username')['count']
    else:
        usuario_counts = pd.Series(dtype=int)
    top_user = usuario_counts.idxmax() if not usuario_counts.empty else 'N/A'
    top_user_count = int(usuario_counts.max()) if not usuario_counts.empty else 0
    genero_mas = genero_counts.idxmax() if not genero_counts.empty else 'N/A'
    genero_mas_count = int(genero_counts.max()) if not genero_counts.empty else 0
    genero_menos = genero_counts.idxmin() if not genero_counts.empty else 'N/A'
    genero_menos_count = int(genero_counts.min()) if not genero_counts.empty else 0

    # Determinar libros con mejor y peor calificación
    if 'calificacion_media' in df.columns and not df.empty:
        best_idx = df['calificacion_media'].idxmax()
        book_best = df.loc[best_idx, 'nombre']
        book_best_count = int(df.loc[best_idx, 'calificaciones_count']) if 'calificaciones_count' in df.columns else 0
        worst_idx = df['calificacion_media'].idxmin()
        book_worst = df.loc[worst_idx, 'nombre']
        book_worst_count = int(df.loc[worst_idx, 'calificaciones_count']) if 'calificaciones_count' in df.columns else 0
    else:
        book_best = 'N/A'
        book_best_count = 0
        book_worst = 'N/A'
        book_worst_count = 0

    # Top 10 libros con más reseñas
    top_reviews = (df.sort_values('calificaciones_count', ascending=False)
                     .head(10)
                     .set_index('nombre')['calificaciones_count']) if 'calificaciones_count' in df.columns else pd.Series(dtype=int)

    # Promedio de calificaciones por autor
    if 'autor' in df.columns and 'calificacion_media' in df.columns:
        avg_by_author = (df.groupby('autor')['calificacion_media']
                           .mean()
                           .sort_values(ascending=False)
                           .head(10))
    else:
        avg_by_author = pd.Series(dtype=float)

    # Promedio de calificaciones por género
    if 'calificacion_media' in df_gen.columns:
        avg_by_genre = (df_gen.groupby('generos')['calificacion_media']
                          .mean()
                          .sort_values(ascending=False))
    else:
        avg_by_genre = pd.Series(dtype=float)

    # Libros sin calificación
    if 'calificaciones_count' in df.columns:
        books_no_rating = df[df['calificaciones_count'] == 0]['nombre'].tolist()
    else:
        books_no_rating = []

    # --- Graficación de resultados ---
    # Gráfico de distribución de libros por género
    fig1, ax1 = plt.subplots()
    genero_counts.plot(kind='bar', ax=ax1, color=plt.cm.Paired.colors)
    ax1.set_xlabel('Género')
    ax1.set_ylabel('Cantidad de libros')
    ax1.set_title('Libros por género')
    img1 = BytesIO()
    fig1.tight_layout()
    fig1.savefig(img1, format='png')
    plt.close(fig1)
    img1.seek(0)
    grafico_genero = base64.b64encode(img1.read()).decode('utf-8')

    # Gráfico de calificación media por libro


# Gráfico de top libros mejor calificados (con colores distintos por barra)
    fig2, ax2 = plt.subplots(figsize=(10, 5))

    if 'calificacion_media' in df.columns and not df.empty:
        top_n = 10
        df_top = df.sort_values('calificacion_media', ascending=False).head(top_n)
        nombres = df_top['nombre']
        calificaciones = df_top['calificacion_media']
    
        colores = plt.cm.tab10.colors  # Paleta de 10 colores diferentes
        barras = ax2.barh(nombres[::-1], calificaciones[::-1], color=colores)

        ax2.set_xlabel('Calificación promedio')
        ax2.set_title(f'Top {top_n} libros mejor calificados')
        ax2.set_xlim(0, 5)
        ax2.tick_params(axis='y', labelsize=9)

        # Mostrar valores numéricos
        for i, barra in enumerate(barras):
            ancho = barra.get_width()
            ax2.text(ancho + 0.05, barra.get_y() + barra.get_height()/2,
                f'{calificaciones.iloc[::-1].iloc[i]:.1f}', va='center', fontsize=8)

        fig2.tight_layout()

    img2 = BytesIO()
    fig2.savefig(img2, format='png', dpi=150)
    plt.close(fig2)
    img2.seek(0)
    grafico_calificacion = base64.b64encode(img2.read()).decode('utf-8')





    # Gráfico de número de reseñas por usuario
    fig3, ax3 = plt.subplots()
    if not usuario_counts.empty:
        usuario_counts.plot(kind='bar', ax=ax3, color=plt.cm.viridis.colors)
    else:
        ax3.text(0.5, 0.5, 'Sin datos', ha='center', va='center')
    ax3.set_xlabel('Usuario')
    ax3.set_ylabel('Cantidad de reseñas')
    ax3.set_title('Reseñas por usuario')
    fig3.tight_layout()
    img3 = BytesIO()
    fig3.savefig(img3, format='png')
    plt.close(fig3)
    img3.seek(0)
    grafico_usuarios = base64.b64encode(img3.read()).decode('utf-8')

    # Gráfico con los libros que más reseñas recibieron
    fig4, ax4 = plt.subplots()
    if not top_reviews.empty:
        top_reviews.plot(kind='bar', ax=ax4, color=plt.cm.Dark2.colors)
    else:
        ax4.text(0.5, 0.5, 'Sin datos', ha='center', va='center')
    ax4.set_xlabel('Libro')
    ax4.set_ylabel('Reseñas')
    ax4.set_title('Top libros con reseñas')
    fig4.tight_layout()
    img4 = BytesIO()
    fig4.savefig(img4, format='png')
    plt.close(fig4)
    img4.seek(0)
    grafico_top_reviews = base64.b64encode(img4.read()).decode('utf-8')

    # Gráfico de promedio de calificaciones por autor
    fig5, ax5 = plt.subplots()
    if not avg_by_author.empty:
        avg_by_author.plot(kind='bar', ax=ax5, color=plt.cm.Set3.colors)
    else:
        ax5.text(0.5, 0.5, 'Sin datos', ha='center', va='center')
    ax5.set_xlabel('Autor')
    ax5.set_ylabel('Promedio de calificaciones')
    ax5.set_title('Promedio por autor')
    fig5.tight_layout()
    img5 = BytesIO()
    fig5.savefig(img5, format='png')
    plt.close(fig5)
    img5.seek(0)
    grafico_autor = base64.b64encode(img5.read()).decode('utf-8')

    # Gráfico de promedio de calificaciones por género
    fig6, ax6 = plt.subplots()
    if not avg_by_genre.empty:
        avg_by_genre.plot(kind='bar', ax=ax6, color=plt.cm.Pastel1.colors)
    else:
        ax6.text(0.5, 0.5, 'Sin datos', ha='center', va='center')
    ax6.set_xlabel('Género')
    ax6.set_ylabel('Promedio de calificaciones')
    ax6.set_title('Promedio por género')
    fig6.tight_layout()
    img6 = BytesIO()
    fig6.savefig(img6, format='png')
    plt.close(fig6)
    img6.seek(0)
    grafico_genero_prom = base64.b64encode(img6.read()).decode('utf-8')

    context = {
        'genero_mas': genero_mas,
        'genero_mas_count': genero_mas_count,
        'genero_menos': genero_menos,
        'genero_menos_count': genero_menos_count,
        'book_best': book_best,
        'book_best_count': book_best_count,
        'book_worst': book_worst,
        'book_worst_count': book_worst_count,
        'top_user': top_user,
        'top_user_count': top_user_count,
        'grafico_genero': grafico_genero,
        'grafico_calificacion': grafico_calificacion,
        'grafico_usuarios': grafico_usuarios,
        'grafico_top_reviews': grafico_top_reviews,
        'grafico_autor': grafico_autor,
        'grafico_genero_prom': grafico_genero_prom,
        'books_no_rating': books_no_rating,
    }
    return render(request, 'libros/estadisticas.html', context)
