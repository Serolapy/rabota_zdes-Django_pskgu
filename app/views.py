from .forms import PoolForm 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def links (request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ссылки',
            'year':datetime.now().year,
        }
    )

def pool (request):
    assert isinstance(request, HttpRequest)
    data = None
    rating = {'1' : 'Ужасно', '2' : 'Плохо', '3' : 'Неплохо', '4' : 'Хорошо', '5' : 'Отлично'}
    message_type = {'1' : 'Предложение', '2' : 'Просьба', '3' : 'Пожелание'}

    if request.method == 'POST':
        form = PoolForm(request.POST)
        if form.is_valid():
            data = dict()
            data['email'] = form.cleaned_data['email']
            data['text'] = form.cleaned_data['text']
            data['message_type'] = message_type[form.cleaned_data['message_type']]
            data['rating'] = rating[form.cleaned_data['rating']]
            data['send_email'] = 'Да' if form.cleaned_data['send_email'] else 'Нет'
            form = None
    else:
        form = PoolForm()
    return render(
        request,
        'app/pool.html',
        {
            'title':'Отзывы о работе сайта',
            'form': form,
            'year':datetime.now().year,
            'data':data
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации
        else:
            regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
            return render(
                request,
                'app/registration.html',
                {
                    'regform': regform, # передача формы в шаблон веб-страницы
                    'year':datetime.now().year,
                }
           )