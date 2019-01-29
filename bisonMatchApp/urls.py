from django.urls import path
from django.conf.urls import include, url
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('quiz/', views.quiz, name='quiz'),
    path('thanks/', views.thanks, name="thanks"),
    path('payment_finished/', views.payment_finished, name="payment_finished"),
    path('cancel/', views.payment_error, name="cancel"),
    url(r'^matches/(?P<slug>[-\w]+)/$', views.matches)
]
