from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .models import Lustudent
from .forms import ProfileForm

my_var = ""

# Create your views here.

def index(request):
    #return HttpResponse("Hello, world. You're at the Bison Match 3.0 index page.... ")
    return render(request, 'bisonMatchApp/index.html')

def about(request):
    LU_student = Lustudent.objects.values('name')
    context = {'LU_student': LU_student}
    return render(request, 'bisonMatchApp/about.html', context)

def get_image(request):
    return render(request, 'bisonMatchApp/get_image.html') 

def profile(request):
    if request.method == 'POST':
    # create a form instance and populate it with data from the request:
        form = ProfileForm(request.POST)
    # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            request.session['name'] = form.cleaned_data['name']
            request.session['lnumber'] = form.cleaned_data['lnumber']
            request.session['emailaddress'] = form.cleaned_data['emailaddress']
            request.session['gender'] = form.cleaned_data['gender']
            request.session['bio'] = form.cleaned_data['bio']
            
            return HttpResponseRedirect('/bisonMatch/quiz/')
# if a GET (or any other method) we'll create a blank form
    else:
        form = ProfileForm()

    return render(request, 'bisonMatchApp/profile.html', {'form': form})
   # return render(request, 'bisonMatchApp/profile.html') 


def quiz(request):
    profile_info = []
    name = request.session['name']
    lnumber = request.session['lnumber']
    emailaddress = request.session['emailaddress']
    gender = request.session['gender']
    bio = request.session['bio']

    profile_info.append(name)
    profile_info.append(lnumber)
    profile_info.append(emailaddress)
    profile_info.append(gender)
    profile_info.append(bio)

    return render(request, 'bisonMatchApp/quiz.html',{'profile_info': profile_info})
