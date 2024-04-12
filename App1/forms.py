from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Curso_fomulario(forms.Form):
    nombre=forms.CharField(max_length=20)
    comision=forms.IntegerField()

class Profesor_formulario(forms.Form):
    nombre=forms.CharField(max_length=20)
    dni=forms.IntegerField()


class Alumno_formulario(forms.Form):
    nombre=forms.CharField(max_length=20)
    dni=forms.IntegerField()