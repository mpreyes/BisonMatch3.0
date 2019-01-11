from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .models import Lustudent
from .forms import NameForm

# Create your views here.

def index(request):
    #return HttpResponse("Hello, world. You're at the Bison Match 3.0 index page.... ")
    return render(request, 'bisonMatchApp/index.html')

def about(request):
    LU_student = Lustudent.objects.values('name')
    context = {'LU_student': LU_student}
    return render(request, 'bisonMatchApp/about.html', context)

def profile(request):
    return render(request, 'bisonMatchApp/profile.html') 

def quiz(request):
    return render(request, 'bisonMatchApp/quiz.html')
