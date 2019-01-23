from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('quiz/', views.quiz, name='quiz'),
    path('thanks/', views.thanks, name="thanks"),
    path('matches/<slug:slug>/', views.matches, name="matches")
]
