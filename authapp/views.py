from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import SMAUserLoginForm, SMAUserRegisterForm, SMAUserEditForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    title = 'вход'

    login_form = SMAUserLoginForm(data=request.POST)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form': login_form,
        'next': next
    }

    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = SMAUserRegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = SMAUserRegisterForm()

    content = {'title': title,
               'register_form': register_form
    }

    return render(request, 'authapp/register.html', content)


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = SMAUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = SMAUserEditForm(instance=request.user)

    content = {'title': title,
               'edit_form': edit_form
    }

    return render(request, 'authapp/edit.html', content)