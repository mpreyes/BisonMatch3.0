from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('quiz/', views.quiz, name='quiz'),
    path('thanks/', views.thanks, name="thanks"),
    url(r'^matches/(?P<slug>[-\w]+)/$', views.matches)
]
