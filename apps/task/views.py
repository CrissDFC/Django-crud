import re
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from apps.task.forms import TaskForm
from apps.task.models import Task
from django.utils import timezone


# Generic Views
def home(request):
    return render(request, 'task/home.html')

@login_required
def task(request):
    """
    Vista que muestra las tareas pendientes del usuario autenticado.

    :param request: Solicitud HTTP del usuario.
    :type request: HttpRequest
    :return: Página renderizada con las tareas completadas.
    :rtype: HttpResponse
    """
    tasks = Task.objects.filter(user=request.user, date_complete__isnull=True)
    return render(request, 'task/task.html', {
        'tasks': tasks,
    })



#Task Completed List

@login_required
def task_completed_list(request):
    """
        Vista que muestra la lista de tareas completadas del usuario autenticado.

        :param request: Solicitud HTTP del usuario.
        :type request: HttpRequest
        :return: Página renderizada con las tareas completadas.
        :rtype: HttpResponse
    """
    tasks = Task.objects.filter(user=request.user, date_complete__isnull=False).order_by('-date_complete')
    return render(request, 'task/task_completed_list.html', {
        'tasks': tasks,
    })


# Strong password validation
def strong_password(password):
    """
        Valida si la contraseña es robusta:
        - Al menos 8 caracteres
        - Al menos una letra mayúscula
        - Al menos una letra minúscula
        - Al menos un número
        - Al menos un carácter especial
    """
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*()_+=\-{}\[\]:;\"'<>,.?/]", password):
        return "Password must contain at least one special character."
    return None  # Sí pasa todas las validaciones


# User Creation
def user_signup(request):
    """
        Vista para el registro de nuevos usuarios.

        :param request: Solicitud HTTP del usuario.
        :type request: HttpRequest
        :return: Página de registro o redirección al login.
        :rtype: HttpResponse
    """
    if request.method == 'GET':
        return render(request, 'task/signup.html', {
            'form': UserCreationForm,
        })
    else:
        password_error = strong_password(request.POST['password1'])
        if password_error:
            return render(request, 'task/signup.html', {
                'form': UserCreationForm,
                'error': password_error,
            })
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['email'],
                    password=request.POST['password1'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                )
                user.save()
                return redirect('login')
            except IntegrityError:
                return render(request, 'task/signup.html', {
                    'form': UserCreationForm,
                    "error": 'Email already exists'
                })
        return render(request, 'task/signup.html', {
            'form': UserCreationForm,
            "error": 'Passwords do not match'
        })


# User Login
def user_login(request):
    """
        Vista para el inicio de sesión de usuarios.

        :param request: Solicitud HTTP del usuario.
        :type request: HttpRequest
        :return: Página de login o redirección a tareas si está autenticado.
        :rtype: HttpResponse
    """
    if request.user.is_authenticated:
        return redirect('task')
    else:
        if request.method == 'GET':
            return render(request, 'task/login.html', {
                'form': AuthenticationForm(),
            })
        else:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('task')
            else:
                return render(request, 'task/login.html', {
                    'form': AuthenticationForm(),
                    'error': 'Username/password incorrect',
                })


# User Logout
@login_required
def user_logout(request):
    """
        Vista para cerrar sesión del usuario autenticado.

        :param request: Solicitud HTTP del usuario.
        :type request: HttpRequest
        :return: Redirección a la página de inicio.
        :rtype: HttpResponse
    """
    logout(request)
    return redirect('home')


# Task Creations
@login_required
def create_task(request):
    """
        Vista para crear una nueva tarea.

        :param request: Solicitud HTTP del usuario.
        :type request: HttpRequest
        :return: Página de creación de tarea o redirección a tareas.
        :rtype: HttpResponse
    """
    if request.method == 'GET':
        return render(request, 'task/create_task.html', {
            'form': TaskForm,
        })
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('task')
        else:
            return render(request, 'task/create_task.html', {
                'form': TaskForm,
                'error': 'Could not create task',
            })


# Task Detail

@login_required
def task_detail(request, task_id):
    """
        Vista que muestra los detalles de una tarea específica del usuario.

        :param request: Solicitud HTTP del usuario.
        :type request: HttpRequest
        :param task_id: ID de la tarea a mostrar.
        :type task_id: Int
        :return: Página con los detalles de la tarea.
        :rtype: HttpResponse
        """
    task_det = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, 'task/task_detail.html', {
        'task': task_det,
    })



# Task Edit

@login_required
def task_edit(request, task_id):
    """
        Vista para editar una tarea existente del usuario.

        :param request: Solicitud HTTP del usuario.
        :type request: HttpRequest
        :param task_id: ID de la tarea a editar.
        :type task_id: Int
        :return: Página de edición de tarea o redirección a tareas.
        :rtype: HttpResponse
    """
    task_upt = get_object_or_404(Task, id=task_id, user=request.user)
    form = TaskForm(instance=task_upt)
    if request.method == 'GET':
        return render(request, 'task/task_update.html', {
            'form': form,
        })
    else:
        form = TaskForm(request.POST, instance=task_upt)
        if form.is_valid():
            form.save()
            return redirect('task')
        else:
            return render(request, 'task/task_update.html', {
                'form': form,
                'error': 'Could not update task',
            })

# Task Completed
@login_required
def task_completed(request, task_id):
    """
        Vista que marca una tarea como completada.

        :param request: Solicitud HTTP del usuario.
        :type request: HttpRequest
        :param task_id: ID de la tarea a completar.
        :type task_id: Int
        :return: Redirección a la lista de tareas pendientes.
        :rtype: HttpResponse
    """
    task_comp = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task_comp.date_complete = timezone.now()
        task_comp.save()
        return redirect('task')


@login_required
def task_delete(request, task_id):
    """
        Vista que elimina una tarea del usuario.

        :param request: Solicitud HTTP del usuario.
        :type request: HttpRequest
        :param task_id: ID de la tarea a eliminar.
        :type task_id: Int
        :return: Redirección a la lista de tareas pendientes o completadas.
        :rtype: HttpResponse
    """
    task_del = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task_del.delete()
        if task_del.date_complete:
            return redirect('task_completed_list')
        else:
            return redirect('task')