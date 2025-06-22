# Tabla de endpoints API
La siguiente tabla resume las rutas principales disponibles en el proyecto. Puedes importarlas en Postman usando el archivo SistemaLogin y Libros en formato .json
Algunas de ellas son:
| Método | Ruta | Descripción |
|-------|------|-------------|
| POST | `/api/auth/register/` | Registro de usuarios |
| POST | `/api/auth/login/` | Obtiene un par de tokens JWT |
| POST | `/api/auth/token/refresh/` | Refresca el token JWT |
| GET, POST | `/api/libros/autores/` | Listar o crear autores |
| GET, PUT, DELETE | `/api/libros/autores/{id}/` | Detalle de autor |
| GET, POST | `/api/libros/generos/` | Listar o crear géneros |
| GET, PUT, DELETE | `/api/libros/generos/{id}/` | Detalle de género |
| GET, POST | `/api/libros/libros/` | Listar o crear libros |
| GET, PUT, DELETE | `/api/libros/libros/{id}` | Detalle de libro |
| GET, POST | `/api/libros/calificaciones/` | Listar o crear calificaciones |
| GET, PUT, DELETE | `/api/libros/calificaciones/{id}/` | Detalle de calificación |