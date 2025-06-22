#Importamos la clase base AppConfig de Django
from django.apps import AppConfig

#Definimos la clase de configuración para la app 'libros'
class LibrosConfig(AppConfig):
    #Indicamos que el campo de la clave primaria por defecto para modelos será BigAutoField
    #BigAutoField es un entero grande autoincremental, recomendado para escalabilidad
    default_auto_field = 'django.db.models.BigAutoField'
    #Nombre de la app. Debe coincidir con el nombre de la carpeta 'libros'
    name = 'libros'

#Es el archivo que declara oficialmente la existencia de la app libros
#Define que la app utilizará Big AutoField como tipo por defecto de primary key
