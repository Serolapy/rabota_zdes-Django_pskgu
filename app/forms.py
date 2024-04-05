"""
Definition of forms.
"""

from tkinter import Widget
from typing_extensions import Required
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from django.db import models
from .models import Comment, Vacancy

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

# отзыв о работе сайта
class PoolForm (forms.Form):
    email = forms.EmailField(required = True, label='Ваш e-mail')
    rating = forms.ChoiceField(label='Оцените работу сайта', choices=[('5', 'Отлично'), ('4', 'Хорошо'), ('3', 'Неплохо'), ('2', 'Плохо'), ('1', 'Ужасно')], initial=1)
    message_type = forms.ChoiceField(label='Выберите тип обращения', choices=[('1', 'Предложение'), ('2', 'Просьба'), ('3', 'Пожелание')])
    text = forms.CharField(label='Ваши предложения и замечания', widget=forms.Textarea())
    send_email = forms.BooleanField(label='Прислать ответ на электронную почту?', required=False)

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text

class VacancyForm (forms.ModelForm):
   class Meta:
        model = Vacancy # используемая модель
        fields = ('title', 'description', 'image', 'content')
        labels = {'title': 'Заголовок', 'description': 'Краткое описание', 'image': 'Картинка', 'content': 'Текст вакансии'} # метка к полю формы text