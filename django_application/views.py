from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm


def index(request):
    return render(request, 'django_application/index.html')

def register(request):

    registered = False

    if request.method == 'POST':
        form = CreateUserForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            registered = True
    else:
        form = CreateUserForm()

    context = {
    'form': form,
    'registered': registered,
    }

    return render(request, 'django_application/registration.html', context)

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('django_application:index'))
            else:
                return HttpResponse('Your account is not active.')
        else:
            return HttpResponse('Invalid data')
    else:
        return render(request, 'django_application/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('django_application:index'))
