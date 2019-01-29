from django.urls import path
from django.conf.urls import include, url
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('quiz/', views.quiz, name='quiz'),
    path('thanks/', views.thanks, name="thanks"),
    path('payment_success/', views.payment_success, name="payment_success"),
    path('payment_error/', views.payment_error, name="payment_error"),
    #url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^show_me_the_money/', include('paypal.standard.ipn.urls')),
    url(r'^matches/(?P<slug>[-\w]+)/$', views.matches)
]
