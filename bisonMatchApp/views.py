from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template import loader
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from .models import Lustudent, ImageUpload
from .forms import ProfileForm, UploadImageForm
from contextlib import closing
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

import base64
from django.core.files.base import ContentFile

# Create your views here.

def index(request):
    return render(request, 'bisonMatchApp/index.html')

def about(request):
    LU_student = Lustudent.objects.values('name')
    context = {'LU_student': LU_student}
    return render(request, 'bisonMatchApp/about.html', context)

def quiz(request):
    if request.method == 'POST':
        print("Processing post...")
        # Check in the terminal for how the session variables are coming in...
        for key, value in request.POST.items():
            if key != "image_data":
                print('{} => {}'.format(key, value))

        MEDIA_ROOT = "/media/user_profiles/"
        if request.POST["image_data"] != "":
            image_data = request.POST["image_data"]
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = str(request.POST["l-number"]) + "." + ext
            image = ContentFile(base64.b64decode(imgstr))
            document = ImageUpload()
            document.media.save(file_name, image)
            document.save()
            image_file_path = MEDIA_ROOT + file_name
        else:
            image_file_path = MEDIA_ROOT + "bisonMatchDefault.png"

        sql = "INSERT INTO lustudent VALUES ("
        sql += "\"" + request.POST["name"] + "\", "
        sql += "\"" + request.POST["l-number"] + "\", "
        sql += "\"" + request.POST["email"] + "\", "
        sql += "\"" + request.POST["major"] + "\", "
        sql += "\"" + request.POST["bio"] + "\", "
        sql += "\"" + request.POST["idealdate"] + "\", "
        sql += "\"" + request.POST["gender"] + "\", "
        sql += request.POST["question1"] + ", "
        sql += request.POST["question2"] + ", "
        sql += request.POST["question3"] + ", "
        sql += request.POST["question4"] + ", "
        sql += request.POST["question5"] + ", "
        sql += request.POST["question6"] + ", "
        sql += request.POST["question7"] + ", "
        sql += request.POST["question8"] + ", "
        sql += request.POST["question9"] + ", "
        sql += request.POST["question10"] + ", "
        sql += "\"" + image_file_path + "\", "
        sql += "0);"


        #TODO Consider replacing the below to lines with the following
        with closing(connection.cursor()) as cursor:
            cursor = connection.cursor()
            cursor.execute(sql)
        connection.close()
        #This ensures that both the cursor and the connection are closed

        lnumbers = getAllStudentNumbers()

        return HttpResponseRedirect('/bisonMatch/thanks/', {"lnumbers" : lnumbers})
    else:
        return render(request, 'bisonMatchApp/quiz.html')

@csrf_exempt
def thanks(request):
    if request.POST:
        lnumber = request.POST.get("invoice", "")

        if lnumber != "":
            with closing(connection.cursor()) as cursor:
                cursor = connection.cursor()
                cursor.execute("UPDATE lustudent SET paid=1 WHERE lnumber='" + str(lnumber) + "';")
            connection.close()
            print("Updated person with lnumber: " + str(lnumber))
        else:
            print("There has been a fata error...")
            return None
        return render(request, 'bisonMatchApp/index.html')


    lnumbers = getAllStudentNumbers()

    return render(request, 'bisonMatchApp/thanks.html', {"lnumbers" : lnumbers})

@csrf_exempt
def payment_finished(request):
    #sendResult('reyes.madelyn.mr@gmail.com','results')
    return render(request, 'bisonMatchApp/payment_success.html')

@csrf_exempt
def payment_error(request):
    #sendResult('reyes.madelyn.mr@gmail.com','results')
    return render(request, 'bisonMatchApp/payment_error.html')



def getStudentData(lnumber):
    student = None
    with closing(connection.cursor()) as cursor:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `lustudent` where `lnumber` = " + str(lnumber) + ";")
        student = cursor.fetchone()
    connection.close()
    return student

def getAllStudentNumbers():
    lnumbers = []
    with closing(connection.cursor()) as cursor:
        cursor = connection.cursor()
        cursor.execute("SELECT lnumber FROM lustudent;")
        res = cursor.fetchall()
    connection.close()

    for obj in res:
        if obj[0] != "":
            lnumbers.append(obj[0])
    return lnumbers

def matches(request, slug):
    matchLNumbers = []
    percentages = []
    paid = 0

    with closing(connection.cursor()) as cursor:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `studentmatches` where `studentlnumber` = " + str(slug) + ";")
        res = cursor.fetchall()
        for object in res:
            matchLNumbers.append(object[1])
            percentages.append(object[2])
    connection.close()

    with closing(connection.cursor()) as cursor:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `lustudent` where `lnumber` = " + str(slug) + ";")
        res = cursor.fetchone()
        print(res)
        paid = res[-1]
    connection.close()

    matches = []
    i = 0
    for lnumber in matchLNumbers:
        matches.append(list(getStudentData(lnumber)) + [percentages[i]])
        i += 1

    return render(request, 'bisonMatchApp/matches.html', {"matches" : matches, "paid" : paid})


def sendResult(emailAddress, results):  #run this function to send an email to our users
    html_message = loader.render_to_string('bisonMatchApp/results_email.html', {'name': results})
    subject = " hi"
    message = "boy "
    send_mail(
        subject, #subject
        message,   #body
    'bisonmatch2.0@gmail.com', #from us
    [emailAddress], #to you
    fail_silently=False,
    html_message=html_message,
)
