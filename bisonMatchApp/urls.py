from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('quiz/', views.quiz, name='quiz'),
    path('get_image/', views.get_image, name="get_image"),
    path('thanks/', views.thanks, name="thanks"),
]