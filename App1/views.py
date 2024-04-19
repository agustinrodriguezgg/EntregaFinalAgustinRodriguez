from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
#Import App1
from App1.models import Curso,Profesor, Alumno, Avatar
from App1.forms import Curso_fomulario, Profesor_formulario, Alumno_formulario, UserEditForm

# Create your views here.

def inicio(request):
    avatares = Avatar.objects.filter(user=request.user.id)
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
                avatares = Avatar.objects.filter(user=request.user.id)
                return render( request , "inicio.html" , {"url":avatares[0].imagen.url ,"mensaje":f"Bienvenido/a {usuario}"})
            else:
                return HttpResponse(f"Usuario no encontrado")
        else:
            return HttpResponse(f"FORM INCORRECTO {form}")
    form = AuthenticationForm()
    return render( request , "login.html" ,{"form":form})

def register(request):
    if request.method == "POST":
        avatares = Avatar.objects.filter(user=request.user.id)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            avatares = Avatar.objects.filter(user=request.user.id)
            return HttpResponse("Usuario creado")
    else:
        form = UserCreationForm()
        avatares = Avatar.objects.filter(user=request.user.id)
    return render(request , "registro.html" , {"form":form,"url":avatares[0].imagen.url})

def editar_perfil(request):
    usuario = request.user
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method == "POST":
        mi_formulario = UserEditForm(request.POST)
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            usuario.email = informacion["email"]
            password = informacion["password1"]
            usuario.set_password(password)
            usuario.save()
            return render(request , "inicio.html",{"mensaje":f"Usuario editado Correctamente","url":avatares[0].imagen.url} )
    else:
        avatares = Avatar.objects.filter(user=request.user.id)
        miFormulario = UserEditForm(initial={'email':usuario.email})
    return render( request , "editar_perfil.html", {"miFormulario":miFormulario, "usuario":usuario,"url":avatares[0].imagen.url})
#CURSOS

def curso_formulario(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method =="POST":
        mi_formulario = Curso_fomulario(request.POST)
        if mi_formulario.is_valid():
            avatares = Avatar.objects.filter(user=request.user.id)
            datos = mi_formulario.cleaned_data
            curso = Curso(nombre=request.POST["nombre"], comision=request.POST["comision"])
            curso.save()
            return render(request,"curso_formulario.html",{"url":avatares[0].imagen.url})
    return render(request,"curso_formulario.html",{"url":avatares[0].imagen.url})


def cursos_ver(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    cursos = Curso.objects.all()
    return render (request, "cursos.html",{"cursos":cursos,"url":avatares[0].imagen.url})


def curso_buscar(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "curso_buscar.html",{"url":avatares[0].imagen.url})


def curso_resultado(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        cursos = Curso.objects.filter(nombre__icontains= nombre)
        return render(request,"curso_resultado.html",{"cursos":cursos,"url":avatares[0].imagen.url})
    else:
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request,"curso_buscar_error.html",{"url":avatares[0].imagen.url})

def curso_eliminar(request, id):
    avatares = Avatar.objects.filter(user=request.user.id)
    curso = Curso.objects.get(id=id)
    curso.delete()
    cursos = Curso.objects.all()
    return render (request, "cursos.html", {"cursos":cursos,"url":avatares[0].imagen.url})

def curso_editar(request, id):
    avatares = Avatar.objects.filter(user=request.user.id)
    curso = Curso.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Curso_fomulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso.nombre = datos["nombre"]
            curso.comision = datos["comision"]
            curso.save()
            curso = Curso.objects.all()
            return render (request, "cursos.html", {"cursos":curso,"url":avatares[0].imagen.url})
    else:
        avatares = Avatar.objects.filter(user=request.user.id)
        mi_formulario = Curso_fomulario (initial={"nombre":curso.nombre, "comision":curso.comision})
    return render(request, "curso_editar.html",{"mi_formulario":mi_formulario, "curso":curso,"url":avatares[0].imagen.url})

#PROFESORES

def profesor_formulario(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method =="POST":
        mi_formulario = Profesor_formulario(request.POST)
        if mi_formulario.is_valid():
            avatares = Avatar.objects.filter(user=request.user.id)
            datos = mi_formulario.cleaned_data
            profesor = Profesor(nombre=request.POST["nombre"], dni=request.POST["dni"])
            profesor.save()
            return render(request, "profesor_formulario.html",{"cursos":cursos,"url":avatares[0].imagen.url})
    return render(request, "profesor_formulario.html",{"cursos":cursos,"url":avatares[0].imagen.url})


def profesores_ver(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    profesores = Profesor.objects.all()
    return render(request, "profesores.html",{"profesores":profesores,"url":avatares[0].imagen.url})


def profesor_buscar(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request,"profesor_buscar.html",{"url":avatares[0].imagen.url})


def profesor_resultado(request):
    if request.GET["nombre"]:
        avatares = Avatar.objects.filter(user=request.user.id)
        nombre = request.GET["nombre"]
        profesores = Profesor.objects.filter(nombre__icontains= nombre)
        return render(request,"profesor_resultado.html",{"profesores":profesores, "url":avatares[0].imagen.url})
    else:
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request,"profesor_buscar_error.html",{"url":avatares[0].imagen.url})

def profesor_eliminar(request, id):
    avatares = Avatar.objects.filter(user=request.user.id)
    profesor = Profesor.objects.get(id=id)
    profesor.delete()
    profesores = Profesor.objects.all()
    return render (request, "profesores.html", {"profesores":profesores,"url":avatares[0].imagen.url})

def profesor_editar(request, id):
    avatares = Avatar.objects.filter(user=request.user.id)
    profesor = Profesor.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Profesor_formulario(request.POST)
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            profesor.nombre = datos["nombre"]
            profesor.dni = datos["dni"]
            profesor.save()
            profesor = Profesor.objects.all()
            return render (request, "profesores.html", {"profesores":profesor,"url":avatares[0].imagen.url})
    else:
        avatares = Avatar.objects.filter(user=request.user.id)
        mi_formulario = Profesor_formulario (initial={"nombre":profesor.nombre, "dni":profesor.dni})
    return render(request, "profesor_editar.html",{"mi_formulario":mi_formulario, "profesor":profesor,"url":avatares[0].imagen.url})

#ALUMNOS

def alumno_formulario(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    if request.method == "POST":
        mi_formulario = Alumno_formulario(request.POST)
        if mi_formulario.is_valid():
            avatares = Avatar.objects.filter(user=request.user.id)
            datos = mi_formulario.cleaned_data
            alumno = Alumno(nombre=request.POST["nombre"], dni=request.POST["dni"])
            alumno.save()
            return render(request , "alumno_formulario.html",{"profesor":profesor,"url":avatares[0].imagen.url})
    return render(request , "alumno_formulario.html",{"profesor":profesor,"url":avatares[0].imagen.url})


def alumnos_ver(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    alumnos = Alumno.objects.all()
    return render(request,"alumnos.html",{"alumnos":alumnos,"url":avatares[0].imagen.url})


def alumno_buscar(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, "alumno_buscar.html",{"url":avatares[0].imagen.url})


def alumno_resultado(request):
    if request.GET["nombre"]:    
        avatares = Avatar.objects.filter(user=request.user.id)
        nombre = request.GET["nombre"]
        alumnos = Alumno.objects.filter(nombre__icontains= nombre)
        return render(request,"alumno_resultado.html",{"url":avatares[0].imagen.url})
    else:
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request,"alumno_buscar_error.html",{"url":avatares[0].imagen.url})

def alumno_eliminar(request, id):
    avatares = Avatar.objects.filter(user=request.user.id)
    alumno = Alumno.objects.get(id=id)
    alumno.delete()
    alumnos = Alumno.objects.all()
    return render (request, "alumnos.html", {"alumnos":alumnos,"url":avatares[0].imagen.ur})

def alumno_editar(request, id):
    avatares = Avatar.objects.filter(user=request.user.id)
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
        avatares = Avatar.objects.filter(user=request.user.id)
        mi_formulario = Alumno_formulario (initial={"nombre":alumno.nombre, "dni":alumno.dni,"url":avatares[0].imagen.url})
    return render(request, "alumno_editar.html",{"mi_formulario":mi_formulario, "alumno":alumno,"url":avatares[0].imagen.url})
