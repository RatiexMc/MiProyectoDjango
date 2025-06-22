#Importamos el modelo de usuario de Django
from django.contrib.auth.models import User
#Importamos la clase base de serializadores de DRF
from rest_framework import serializers
#Definimos un serializador para registrar nuevos usuarios
class RegisterSerializer(serializers.ModelSerializer):
    #Configuramos qué campos del modelo user estarán disponibles en la API
    class Meta:
        model = User #Modelo de Django que representa un usuario
        fields =('username','email','password') # Campos que queremos exponer
        extra_kwargs = {'password':{'write_only':True}} # La contraseña no se devuelve en la respuesta

    #Sobreescribimos el método crete para personalizar la creación del usuario
    def create(self, validated_data):
        #Craemos un nuevo usuario usando el método create_user, que maneja el hashing de la contraseña
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user #Devolvemos el nuevo usuario creado
#Este archivo permite que un endpoint de registro pueda recibir datos en JSON



