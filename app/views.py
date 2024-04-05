from .forms import PoolForm 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import Comment, Vacancy # использование модели комментариев
from .forms import CommentForm, VacancyForm # использование формы ввода комментария

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

def vacancy (request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Vacancy.objects.all() # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/vacancy.html',
        {
            'title':'Вакансии',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def vacancyPost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Vacancy.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(vacancy=parametr)
    form = CommentForm(request.POST)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.vacancy = Vacancy.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            
            return redirect('vacancyPost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария
    
    
    return render(
        request,
        'app/vacancyPost.html',
        {
            'title' : post_1.title,
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'year':datetime.now().year,
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
        }
    )

def vacancyNew(request):
    #form = VacancyForm(request.POST, request.FILES)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = VacancyForm(request.POST, request.FILES)
        if form.is_valid():
            vacancy_f = form.save(commit=False)
            vacancy_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            vacancy_f.posted = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            vacancy_f.save() # сохраняем изменения после добавления полей
            
            return redirect('vacancy') # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = VacancyForm() # создание формы для ввода комментария
    
    
    return render(
        request,
        'app/vacancyNew.html',
        {
            'year':datetime.now().year,
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
        }
    )

def video(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/video.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )