# Importamos la clase base AppConfig de Django
from django.apps import AppConfig

# Definimos la clase de configuración para la app 'accounts'
class AccountsConfig(AppConfig):
    # Indicamos que el campo de clave primaria por defecto para modelos será BigAutoField
    # Es un entero grande autoincremental, útil para bases de datos con muchos registros
    default_auto_field = 'django.db.models.BigAutoField'

    # Nombre de la app. Debe coincidir con el nombre de la carpeta 'accounts'
    name = 'accounts'
