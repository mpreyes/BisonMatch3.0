from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('get_name/', views.get_name, name='get_name'),
    path('profile/', views.profile, name='profile'),
    path('quiz/', views.quiz, name='quiz'),
]