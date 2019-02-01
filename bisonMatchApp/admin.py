from django.contrib import admin
from .models import Lustudent, StudentMatches
from django.http import HttpResponseRedirect
from django.db import IntegrityError, DatabaseError, connection
from django.core.mail import send_mail
from django.template import loader

from contextlib import closing
from operator import itemgetter

admin.site.disable_action('delete_selected')

numMatches = 5
totalQuestions = 10

@admin.register(Lustudent)
class LustudentAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'lnumber', 'emailaddress', 'gender', 'paid']
    ordering = ['lnumber']
    actions = ['generateMatches','markPaid', 'sendReminderEmail', 'sendResultEmail']

    def markPaid(self, request, queryset):
        try:
            rows_updated = queryset.update(paid = 1)
            if rows_updated == 1:
                message_bit = "1 student was"
            else:
                message_bit = "%s students were" % rows_updated
            self.message_user(request, "%s successfully marked as paid." % message_bit)
        except DatabaseError:
            self.message_user(request, "An error occured with your request.")
        return
    markPaid.short_description = 'Mark student as paid'

    def generateMatches(self, request, queryset):
        students = queryset
        totalInserts = 0
        for student in students:
            matches = getMatchesForStudent(student) 
            totalInserts += len(matches)
            for match in matches:
                try:
                    StudentMatches.objects.create(studentlnumber=student.lnumber, matchlnumber=match['lnumber'], percent=match['percent'])
                except (IntegrityError, DatabaseError):
                    self.message_user(request, "An error occured with your request, match %s with %s was not added to StudentMatches"% (student.lnumber, match['lnumber']))
        self.message_user(request, 'Done: %s rows should have been inserted' %totalInserts)
        return HttpResponseRedirect("../studentmatches/")
    generateMatches.short_description = 'Generate Matches for Students (Ensure all selected)'

    def sendReminderEmail(self, request, queryset):
        students = queryset
        for student in students:
            if student.paid:
                html_message = loader.render_to_string('bisonMatchApp/paid_remind_email.html', {'name': student.name})
                subject = "BisonMatch Reminder"
                message = "Hi " + student.name + ",\n"
                message += "Reminder that your Bison Match results will be available via email Monday February 11, just in time to find a Valentine's Date!\n"
                message += "Have a wonderful day!\n"
                message += "Love, \n Your Friends at Bison Match"
            else: 
                html_message = loader.render_to_string('bisonMatchApp/unpaid_remind_email.html', {'name': student.name})
                subject = "Its Not Too Late To Find Love!"
                message = "Hi " + student.name + ",\nIt's not too late for you to buy your results from Bison Match!\n"
                message += "Visit bisonmatch.info/bisonMatch/thanks or stop by the Bison Match table in the student center to pay for your results.\n" 
                message += "Once you have paid, you will receive your results via email on Monday February 11, just in time to find a Valentine's Date!\n"
                message += "Have a wonderful day!\n"
                message += "Love, \n Your Friends at Bison Match"
            #Send email with appropriate subject and message
            send_mail(
                subject, #subject
                message,   #body
                'bisonmatch2.0@gmail.com', #from us
                [student.emailaddress], #to student
                fail_silently=False,
                html_message=html_message
            )
        return
    sendReminderEmail.short_description = 'Send Reminder to Students (Ensure all selected)'
    
    def sendResultEmail(self, request, queryset):
        students = queryset
        for student in students:
            if student.paid:
                html_message = loader.render_to_string('bisonMatchApp/paid_results_email.html', {'name': student.name, 'lnumber': student.lnumber})
                subject = "Your Bison Match Results Are Now Available!!!"
                message = "Hi " + student.name + ",\n"
                message += "Thank you for supporting your local ACM chapter by buying your results!\n"
                message += "To view your Bison Match results, go to bisonmatch.info/bisonmatch/matches" + student.lnumber
                message += "\nHappy Valentine's Day!\n\nMuch Love,\nYour Friends at Bison Match"
            else: 
                html_message = loader.render_to_string('bisonMatchApp/unpaid_results_email.html', {'name': student.name, 'lnumber': student.lnumber})
                subject = "Its Not Too Late To Find Love!"
                message = "Hi " + student.name + ",\n"
                message += "It's not too late to view your Bison Match results!\n"
                message += "Just go to bisonmatch.info/thanks to buy your results.\n"
                message += "Once you have paid for your results, you can view them at bisonmatch.info/bisonmatch/matches" + student.lnumber
                message += "\nHappy Valentine's Day!\n\nMuch Love,\nYour Friends at Bison Match"
            send_mail(
                subject, #subject
                message,   #body
                'bisonmatch2.0@gmail.com', #from us
                [student.emailaddress], #to student
                fail_silently=False,
                html_message=html_message
            )
        return
    sendResultEmail.short_description = 'Send Match Link to Students (Ensure all selected)'
    


@admin.register(StudentMatches)
class StudentMatchesAdmin(admin.ModelAdmin):
    list_display = ['studentlnumber', 'matchlnumber', 'percent']
    ordering = ['studentlnumber']
    actions = ['delete_selected']


def getMatchesForStudent(student):
    pointedStudents = getPotentialMatchesAndPoints(student)
    # Test sorting
    sortedStudents = sorted(pointedStudents, key=itemgetter('percent'), reverse=True)
    finalMatches = sortedStudents[0:numMatches]
    return finalMatches

def getPotentialMatchesAndPoints(student):
    #student is male(0) get female(1) matches
    if student.gender == 0:
        potentialStudents = Lustudent.objects.filter(gender = 1)
    #student is female(1) get male(0) matches
    elif student.gender == 1:
        potentialStudents = Lustudent.objects.filter(gender = 0)
    #student is undefined(2) get all students
    elif student.gender == 2:
        potentialStudents = Lustudent.objects.exclude(lnumber = student.lnumber)
        print(potentialStudents)
    pointedStudents = []
    qs = ['ans1', 'ans2', 'ans3', 'ans4', 'ans5', 'ans6', 'ans7', 'ans8', 'ans9', 'ans10']
    for potentialStudent in potentialStudents:
        points = 0
        for q in qs:
            if getattr(student, q) == getattr(potentialStudent, q):
                points += 1
        percent = (points/totalQuestions) * 100
        pointedStudents.append({'lnumber': potentialStudent.lnumber, 'percent': percent})
    return pointedStudents
