"""
Definition of urls for rabota_zdes.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('links/', views.links, name='links'),
    path('pool/', views.pool, name='pool'),
    path('about/', views.about, name='about'),
    path('video/', views.video, name='video'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('registration/', views.registration, name= 'registration'),
    path('vacancy/', views.vacancy, name= 'vacancy'),
    path('vacancy/new', views.vacancyNew, name= 'vacancyNew'),
    path('vacancy/<int:parametr>/', views.vacancyPost, name='vacancyPost'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()