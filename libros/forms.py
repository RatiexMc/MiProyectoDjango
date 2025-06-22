#Importamos el módulo de formularios de Django
from django import forms
#Importamos los modelos que usaremos en los formularios
from .models import Libro, CalificacionUsuario
#Formulario para crear o editar un libro
class LibroForm(forms.ModelForm):
    class Meta:
        #Indicamos que el formulario está basado en el modelo del libro
        model = Libro
        #Campos del modelo que estarán disponible en el formulario
        fields = ['nombre', 'autor', 'fecha_lanzamiento', 'generos', 'archivo']
        #Personalizamos el widget del campo fecha_lanzamiento para que sea un selector de fecha html5
        widgets = {
            'fecha_lanzamiento': forms.DateInput(attrs={'type': 'date'}),
        }
#Formulario para crear una reseña y calificación de un libro        
class CalificacionForm(forms.ModelForm):
    class Meta:
        #Indicamos que el formulario está basado en el modelo CalificacionUsuario
        model = CalificacionUsuario
        #Campos del modelo que estarán disponible en el formulario
        fields = ['resenia', 'calificacion']
        #Personalizamos los widgets de los campos
        widgets = {
            #Reseña se mostrará como un textarea(campo de texto multilínea)
            'resenia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            #Calificación se mostrará como un input numérico con valores entre 1 y 5
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }

    #LibroForm: Permite que un usuario autenticado pueda agregar o editar un libro, desde un formulario html
    #CalificacionForm: Permite que un usuario deje una reseña y una calificación para un libro entre 1 y 5
    #Uso del modelForm: Facilita mucho el trabajo porque Django genera automáticamente  a partir de los modelos
    #Uso del Widgets personalizado: Mejora la presentación en los formularios del navegador


