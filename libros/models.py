#Importamos el módulo models de Django para definir modelos en la base de datos
from django.db import models
#Importamos el modelo de usuario de Django
from django.contrib.auth.models import User
#Importamos validador para restringir extensiones de archivos
from django.core.validators import FileExtensionValidator
# Modelo de autor con nombre, nacionalidad y creador (usuario que lo registró)
class Autor(models.Model):
    nombre = models.CharField(max_length=100)#Nombre del autor
    nacionalidad = models.CharField(max_length=50)#Nacionalidad del autor
    #Usuario que creo este autor en el sistema(Puede ser null si el usuario fue eliminado)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='autores_creados')
    #Representación legible de la instancia
    def __str__(self):
        return self.nombre
# Modelo de género con nombre y usuario creador
class Genero(models.Model):
    nombre = models.CharField(max_length=50)#Nombre del género
    #Usuario que creo este género en el sistema
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='generos_creados')

    def __str__(self):
        return self.nombre

# Modelo principal de libro
class Libro(models.Model):
    nombre = models.CharField(max_length=200)#Nombre o Título del libro
    #Relación con Autor (Cada libro tiene un autor)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    fecha_lanzamiento = models.DateField() #Fecha del lanzamiento del libro
    generos = models.ManyToManyField(Genero)  # Relación M:N con género
    vistas = models.PositiveIntegerField(default=2)#Contador de vistas del libro(por defecto:2)
    #Archivo EPUB del Libro
    archivo = models.FileField(
        upload_to='libros/',#Carpeta dentro de /media/libros/
        validators=[FileExtensionValidator(allowed_extensions=['epub'])],#Solo acepta archivos .epub
        help_text="Solo archivos EPUB"
    )

    def __str__(self):
        return self.nombre

# Modelo para registrar calificaciones de usuario a libros
class CalificacionUsuario(models.Model):
    #Usuario que hace la calificación
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    #Libro que es calificado
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='calificaciones_usuario')
    #Texto de la reseña
    resenia = models.TextField(blank=True)
    #Calificación del 1 al 5
    calificacion = models.PositiveSmallIntegerField()  # Por ejemplo: 1=malo a 5=muy bueno
    #Fecha de la calificación (automáticamente asignada al crear)
    fecha = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.usuario.username} - {self.libro.nombre} ({self.calificacion})"

#Definimos la estructura de datos para todo la gestión del libro
#Autor: Almacena autores ligada a un usuario creador
#Genero: Almacena géneros ligada a un usuario creador
#Libro: Almacena libros con: Nombre, Autor, Fecha, Género, Archivo epub y contador de vistas
#CalificaciónUsuario: Permite a los usuarios calificar del 1 al 5 con una reseña en un libro específico

#Relaciones entre modelos:
#Libro → 1 autor, muchos géneros, muchas calificaciones.
#Autor → muchos libros.
#Usuario → muchas calificaciones, puede haber creado autores y géneros.
#Uso de:
#FileField con validación → asegura que solo se suban archivos .epub.
#ManyToManyField → permite que libros tengan múltiples géneros.
#PositiveIntegerField y PositiveSmallIntegerField → para campos numéricos positivos.

