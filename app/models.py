"""
Definition of models.
"""

from datetime import datetime
from tabnanny import verbose
from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

# Класс вакансии
class Vacancy(models.Model):
    title = models.CharField(max_length = 64, unique_for_date = 'posted', verbose_name = 'Заголовок')
    description = models.CharField(max_length = 256, verbose_name = 'Краткое описание')
    content = models.TextField(verbose_name = 'Описание вакансии')
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")

    # метод возвращает строку с URL-адресом записи
    def get_absolute_url(self):
        return reverse("vacancy", args=[str(self.id)])

    # метод возвращает название, используемое для представления отдельных записей в административном разделе
    def __str__(self):
        return self.title

    # Метаданные – вложенный класс, который задает дополнительные параметры модели:

    class Meta:
        db_table = "Vacancys" # имя таблицы для модели
        ordering = ["-posted"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "вакансия" # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "вакансии" # тоже для всех статей блога

admin.site.register(Vacancy)

class Comment(models.Model):
    text = models.TextField(verbose_name = "Текст отклика")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата отклика")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор отклика")
    vacancy = models.ForeignKey(Vacancy, on_delete = models.CASCADE, verbose_name = "Вакансия отклика")

    def __str__(self):
        return "Отклик %d %s к %s" % (self.id, self.author, self.vacancy)

    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Отклики к вакансии"
        verbose_name_plural = "Отклики к вакансиям"

admin.site.register(Comment)