from django.urls import path
from django.conf.urls import include, url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('quiz/', views.quiz, name='quiz'),
    path('thanks/', views.thanks, name="thanks"),
    path('payment_success/', views.thanks, name="payment_success"),
    url(r'^matches/(?P<slug>[-\w]+)/$', views.matches)
]