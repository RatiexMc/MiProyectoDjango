#Importamos los serializadores de DRF
from rest_framework import serializers
#Importamos los modelos de la app libros
from .models import Autor, Libro, Genero, CalificacionUsuario
#Importamos el modelo de usuario
from django.contrib.auth.models import User
#Serializadores por el modelo de usuario
class AutorSerializer(serializers.ModelSerializer):
    #Mostramos el nombre de usuario que creó el autor(en vez de su ID)
    creado_por = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'nacionalidad', 'creado_por']

#Serializadores para el modelo de Género
class GeneroSerializer(serializers.ModelSerializer):
    #Mostramos el nombre del usuario que creó el género
    creado_por = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Genero
        fields = ['id', 'nombre', 'creado_por']


#Serializadores para el modelo de Libro 
class LibroSerializer(serializers.ModelSerializer):
    #Mostramos los datos completos del autor(lectura)
    autor = AutorSerializer(read_only=True)
    #Permitimos enviar solo el ID del autor al crear/editar(escritura)
    autor_id = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all(),source='autor', write_only=True)
    #Mostramos los géneros en forma de lista completa(lectura)
    generos = GeneroSerializer(many=True, read_only=True)
    #Permitimos enviar solo los IDs del género al crear/editar(escritura)
    generos_id = serializers.PrimaryKeyRelatedField(many=True, queryset=Genero.objects.all(), write_only=True,source='generos')
    #Permitimos subir archivos y devolver su URL
    archivo = serializers.FileField(use_url=True) 
    
    class Meta:
        model = Libro
        fields = ['id','nombre','autor','autor_id','fecha_lanzamiento','generos','generos_id','vistas','archivo']
#Serializadores para el modelo de CalificacionUsuario
class CalificacionUsuarioSerializer(serializers.ModelSerializer):
    #Mostramos el nombre del usuario(lectura)
    usuario = serializers.StringRelatedField(read_only=True)#Muestra el nombre del usuario
    #Permitimos solo enviar el ID del usuario al crear (escritura)
    usuario_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),source='usuario', write_only=True)
    #Mostramos el nombre de libro(lectura)
    libro = serializers.StringRelatedField(read_only=True)
    #Permitimos solo enviar el ID del libro al crear (escritura)
    libro_id = serializers.PrimaryKeyRelatedField(queryset=Libro.objects.all(),source='libro',write_only=True)

    class Meta:
        model = CalificacionUsuario
        fields = ['id','usuario','usuario_id','libro','libro_id','resenia','calificacion','fecha']






