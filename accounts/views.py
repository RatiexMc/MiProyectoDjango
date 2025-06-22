# Importamos funciones de renderizado de plantillas y redirección
from django.shortcuts import render, redirect

# Importamos generics para crear vistas basadas en clases en la API REST
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Importamos nuestro serializador personalizado
from .serializers import RegisterSerializer

# Importamos el modelo de usuario de Django
from django.contrib.auth.models import User

# Importamos funciones para autenticar, iniciar y cerrar sesión
from django.contrib.auth import authenticate, login, logout

# Para mostrar mensajes (aunque en este código no se usan explícitamente)
from django.contrib import messages

# Para retornar respuestas HTTP si fuera necesario (aquí no se usa)
from django.http import HttpResponse

# Importamos requests para hacer peticiones HTTP (se usa en register_view)
import requests

# Vista que muestra el home (página de inicio)
def home_view(request):
    return render(request, 'home.html')

# Vista API REST que permite registrar usuarios (usa RegisterSerializer)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # Permite que cualquier usuario (incluso no autenticado) pueda
    # acceder a este endpoint para registrarse
    permission_classes = [AllowAny]
    # Evita comprobaciones CSRF eliminando la autenticación por sesión
    authentication_classes = []

# Vista HTML para iniciar sesión mediante formulario
def login_view(request):
    if request.method == "POST":
        # Obtenemos los datos enviados en el formulario
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Autenticamos el usuario
        user = authenticate(request, username=username, password=password)
        
        # Si es válido, iniciamos sesión y redirigimos a /libros/
        if user is not None:
            login(request, user)
            return redirect('/libros/')
        else:
            # Si no es válido, mostramos error
            return render(request, "accounts/login.html", {"error": "Credenciales Incorrectas"})
    
    # Si es GET, mostramos el formulario de login
    return render(request, "accounts/login.html")

# Vista HTML para registrar usuario mediante formulario
def register_view(request):
    mensaje = None
    error = None

    if request.method == "POST":
        # Obtenemos los datos del formulario
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        # Validar que las contraseñas coincidan
        if password != confirm:
            error = "Las contraseñas no coinciden."
            return render(request, "accounts/register.html", {
                "error": error,
                "mensaje": mensaje
            })

        # Enviar datos al endpoint API de registro (RegisterView)
        response = requests.post(
            "http://127.0.0.1:8000/api/auth/register/",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )

        # Si el registro fue exitoso
        if response.status_code == 201:
            mensaje = "¡Usuario registrado correctamente!"
        else:
            # Si hubo error, extraemos mensaje
            error_data = response.json()
            error = (
                error_data.get("username") or
                error_data.get("email") or
                error_data.get("password") or
                "Error al registrar."
            )

    # Renderizamos la plantilla de registro con posibles mensajes
    return render(request, "accounts/register.html", {"mensaje": mensaje, "error": error})

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('home')
#Resumen (para qué sirve este archivo):
#home_view: muestra la página inicial.
#RegisterView: API REST para registrar usuario (consume RegisterSerializer).
#login_view: permite login tradicional con formulario → si correcto, redirige a /libros/.
#register_view: permite registro tradicional → llama a la API REST para registrar el usuario (curioso, aquí el formulario HTML llama a la API REST en segundo plano).
#logout_view: cierra la sesión y redirige a home.
#Observaciones:
#El register_view HTML usa requests.post() para invocar la API REST de registro, en vez de crear el usuario directamente. Esto es una buena práctica si quieres que toda la lógica pase por la API REST.
#Muy bien estructurado → tienes login/registro tanto API (para apps móviles / JS) como HTML (para usuarios normales).