from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.template import loader
from django.db import connection

from .models import Lustudent
from .forms import ProfileForm, UploadImageForm
from contextlib import closing
from operator import itemgetter

# Create your views here.

def index(request):
    return render(request, 'bisonMatchApp/index.html')

def about(request):
    LU_student = Lustudent.objects.values('name')
    context = {'LU_student': LU_student}
    return render(request, 'bisonMatchApp/about.html', context)

def getAllMatches():
    sql = "SELECT * FROM LUStudent WHERE paid = 0"
    with closing(connection.cursor()) as cursor:
        cursor = connection.cursor()
        cursor.execute(sql)
        students = cursor.fetchall()
    connection.close()
    for student in students:
        getMatchesForStudent(student)
    return

def getPotentialMatchesAndPoints(student):
    #student is male and prefers males match with males that like males or both
    if student[6] == 0 and student[7] == 0:
        sql = "SELECT * from LUStudent WHERE gender = 0 AND (preference = 0 OR preference = 2) AND lnumber != " + student[1]
    #student is female and prefers females match with females that like females or both
    elif student[6] == 1 and student[7] == 1:
        sql = "SELECT * from LUStudent WHERE gender = 1 AND (preference = 1 OR preference = 2) AND lnumber != " + student[1]
    #student is male and prefers both match anyone that like males or both 
    elif student[6] == 0 and student[7] == 2:
        sql = "SELECT * from LUStudent WHERE (preference = 0 OR preference = 2) AND lnumber != " + student[1] 
    #student is female and prefers both match anyone that like females or both 
    elif student[6] == 1 and student[7] == 2:
        sql = "SELECT * from LUStudent WHERE (preference = 1 OR preference = 2) AND lnumber != " + student[1] 
    #student is male and prefers females match with females that like males or both
    elif student[6] == 0 and student[7] == 1:
        sql = "SELECT * from LUStudent WHERE gender = 1 AND (preference = 0 OR preference = 2) AND lnumber != " + student[1]
    #student is female and prefers males match with males that like females or both
    elif student[6] == 1 and student[7] == 0:
        sql = "SELECT * from LUStudent WHERE gender = 0 AND (preference = 1 OR preference = 2) AND lnumber != " + student[1]

    with closing(connection.cursor()) as cursor:
        cursor = connection.cursor()
        cursor.execute(sql)
        potentialStudents = cursor.fetchall()
    connection.close()
    pointedStudents = []
    for potentialStudent in potentialStudents:
        points = 0
        for q in range(8, 18):
            if student[q] == potentialStudent[q]:
                points += 1
        pointedStudents.append({'name': potentialStudent[0], 'emailaddress': potentialStudent[2], 'major': potentialStudent[3], 'bio': potentialStudent[4], 'idealdate': potentialStudent[5], 'points': points})

    return pointedStudents

def getMatchesForStudent(student):
    pointedStudents = getPotentialMatchesAndPoints(student)
    sortedStudents = sorted(pointedStudents, key=itemgetter('points'), reverse=True)
    finalResults = sortedStudents[0:5]
    #send email
    return

def mapTupleToStudentDictionary(student):
    keys = ['name', 'lnumber', 'emailaddress', 'major', 'bio', 'idealdate', 'gender', 'preference', 'ans1', 'ans2', 'ans3', 'ans4', 'ans5', 'ans6', 'ans7', 'ans8', 'ans9', 'ans10', 'profilepicurl', 'paid']
    student = [dict(zip(keys, s)) for s in student]
    return student

def quiz(request):
    if request.method == 'POST':
        print("Processing post...")
        # Check in the terminal for how the session variables are coming in...
        for key, value in request.POST.items():
            print('{} => {}'.format(key, value))

        sql = "INSERT INTO lustudent VALUES ("
        sql += "'" + request.POST["name"] + "', "
        sql += "'" + request.POST["l-number"] + "', "
        sql += "'" + request.POST["email"] + "', "
        sql += "'" + request.POST["major"] + "', "
        sql += "'" + request.POST["bio"] + "', "
        sql += "'" + request.POST["idealdate"] + "', "
        sql += "'" + request.POST["gender"] + "', "
        sql += "'" + request.POST["preference"] + "', "
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

        #===========================================
        # TODO implement profile picture url
        #===========================================
        sql += "'dummyurl.png', "
        sql += "0);"

        cursor = connection.cursor()
        cursor.execute(sql)

        return HttpResponseRedirect('/bisonMatch/thanks/')
    else:
        return render(request, 'bisonMatchApp/quiz.html')

def thanks(request):
    #sendResult('reyes.madelyn.mr@gmail.com','results')
    return render(request, 'bisonMatchApp/thanks.html')


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
