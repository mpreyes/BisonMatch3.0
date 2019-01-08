from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .models import Lustudent

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the Bison Match 3.0 index page.... ")

def about(request):
    LU_student = Lustudent.objects.values('name')
    context = {'LU_student': LU_student}
    return render(request, 'bisonMatchApp/index.html', context)
