from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
#Import App1
from App1.models import Curso,Profesor, Alumno
from App1.forms import Curso_fomulario, Profesor_formulario, Alumno_formulario

# Create your views here.

def inicio(request):
    return render(request, "inicio.html")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            user = authenticate(username=usuario , password=contra)
            if user is not None:
                login(request , user )
                return render( request , "inicio.html" , {"mensaje":f"Bienvenido/a {usuario}"})
            else:
                return HttpResponse(f"Usuario no encontrado")
        else:
            return HttpResponse(f"FORM INCORRECTO {form}")
    form = AuthenticationForm()
    return render( request , "login.html" ,{"form":form})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Usuario creado")
    else:
        form = UserCreationForm()
    return render(request , "registro.html" , {"form":form})

#CURSOS

def curso_formulario(request):
    if request.method =="POST":
        mi_formulario = Curso_fomulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso = Curso(nombre=request.POST["nombre"], comision=request.POST["comision"])
            curso.save()
            return render(request,"curso_formulario.html")
    return render(request,"curso_formulario.html")


def cursos_ver(request):
    cursos = Curso.objects.all()
    dicc = {"cursos": cursos}
    plantilla = loader.get_template("cursos.html")
    documento = plantilla.render(dicc)
    return HttpResponse(documento)


def curso_buscar(request):
    return render(request, "curso_buscar.html")


def curso_resultado(request):

    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        cursos = Curso.objects.filter(nombre__icontains= nombre)
        return render(request,"curso_resultado.html",{"cursos":cursos})
    else:
        return render(request,"curso_buscar_error.html")

def curso_eliminar(request, id):
    curso = Curso.objects.get(id=id)
    curso.delete()
    cursos = Curso.objects.all()
    return render (request, "cursos.html", {"cursos":cursos})

def curso_editar(request, id):
    curso = Curso.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Curso_fomulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso.nombre = datos["nombre"]
            curso.comision = datos["comision"]
            curso.save()
            curso = Curso.objects.all()
            return render (request, "cursos.html", {"cursos":curso})
    else:
        mi_formulario = Curso_fomulario (initial={"nombre":curso.nombre, "comision":curso.comision})
    return render(request, "curso_editar.html",{"mi_formulario":mi_formulario, "curso":curso})

#PROFESORES

def profesor_formulario(request):
    if request.method =="POST":
        mi_formulario = Profesor_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            profesor = Profesor(nombre=request.POST["nombre"], dni=request.POST["dni"])
            profesor.save()
            return render(request, "profesor_formulario.html")
    return render(request, "profesor_formulario.html")


def profesores_ver(request):
    profesores = Profesor.objects.all()
    dicc = {"profesores":profesores}
    plantilla = loader.get_template("profesores.html")
    documento = plantilla.render(dicc)
    return HttpResponse(documento)


def profesor_buscar(request):
    return render(request,"profesor_buscar.html")


def profesor_resultado(request):
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        profesores = Profesor.objects.filter(nombre__icontains= nombre)
        return render(request,"profesor_resultado.html",{"profesores":profesores})
    else:
        return render(request,"profesor_buscar_error.html")

def profesor_eliminar(request, id):
    profesor = Profesor.objects.get(id=id)
    profesor.delete()
    profesores = Profesor.objects.all()
    return render (request, "profesores.html", {"profesores":profesores})

def profesor_editar(request, id):
    profesor = Profesor.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Profesor_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            profesor.nombre = datos["nombre"]
            profesor.dni = datos["dni"]
            profesor.save()
            profesor = Profesor.objects.all()
            return render (request, "profesores.html", {"profesores":profesor})
    else:
        mi_formulario = Profesor_formulario (initial={"nombre":profesor.nombre, "dni":profesor.dni})
    return render(request, "profesor_editar.html",{"mi_formulario":mi_formulario, "profesor":profesor})

#ALUMNOS

def alumno_formulario(request):
    if request.method == "POST":
        mi_formulario = Alumno_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            alumno = Alumno(nombre=request.POST["nombre"], dni=request.POST["dni"])
            alumno.save()
            return render(request , "alumno_formulario.html")
    return render(request , "alumno_formulario.html")


def alumnos_ver(request):
    alumnos = Alumno.objects.all()
    dicc = {"alumnos":alumnos}
    plantilla = loader.get_template("alumnos.html")
    documento = plantilla.render(dicc)
    return HttpResponse(documento)


def alumno_buscar(request):
    return render(request, "alumno_buscar.html")


def alumno_resultado(request):
    if request.GET["nombre"]:    
        nombre = request.GET["nombre"]
        alumnos = Alumno.objects.filter(nombre__icontains= nombre)
        return render(request,"alumno_resultado.html",{"alumnos":alumnos})
    else:
        return render(request,"alumno_buscar_error.html")

def alumno_eliminar(request, id):
    alumno = Alumno.objects.get(id=id)
    alumno.delete()
    alumnos = Alumno.objects.all()
    return render (request, "alumnos.html", {"alumnos":alumnos})

def alumno_editar(request, id):
    alumno = Alumno.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Alumno_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            alumno.nombre = datos["nombre"]
            alumno.dni = datos["dni"]
            alumno.save()
            alumno = Alumno.objects.all()
            return render (request, "alumnos.html", {"alumnos":alumno})
    else:
        mi_formulario = Alumno_formulario (initial={"nombre":alumno.nombre, "dni":alumno.dni})
    return render(request, "alumno_editar.html",{"mi_formulario":mi_formulario, "alumno":alumno})
