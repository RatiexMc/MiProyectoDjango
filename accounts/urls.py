from django.urls import path
from .views import RegisterView, login_view, register_view, logout_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #/register/	POST	API de registro de usuarios (DRF, JSON)
    path('register/', RegisterView.as_view(), name='register'),                      # ← API con DRF
    #/login/	POST	API que devuelve token JWT (login con API REST)
    path('login/', TokenObtainPairView.as_view(), name='login'),                     # ← API para token JWT
    #/token/refresh/	POST	API para refrescar un token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),        # ← API para refrescar JWT
    #/iniciar-sesion/	GET, POST	Vista HTML para login tradicional con formulario
    path('iniciar-sesion/', login_view, name='iniciar_sesion'),                      # ← Vista HTML login
    #/registrarse/	GET, POST	Vista HTML para registro tradicional con formulario
    path('registrarse/', register_view, name='register_view'),                       # ← Vista HTML registro
    #/cerrar-sesion/	GET	Cierra la sesión del usuario actual
    path('cerrar-sesion/', logout_view, name='cerrar_sesion'),                       # ← Cerrar sesión 
]
#Este archivo define las rutas (URLs) que maneja la app accounts
#Define las rutas que maneja la app accounts:
#Tanto para API REST (registro, login con JWT) como para vistas HTML tradicionales (formularios de login y registro).
#Permite que tu sistema soporte:
#Login/registro moderno via API → para apps móviles, SPAs (React, Vue, etc.).
#Login/registro clásico vía HTML → para usuarios web normales.
#Organiza claramente las rutas según su propósito.