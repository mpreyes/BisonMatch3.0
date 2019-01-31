from django.contrib import admin
from .models import Lustudent, StudentMatches
from django.http import HttpResponseRedirect
from django.db import IntegrityError, DatabaseError, connection
from django.core.mail import send_mail
from django.template import loader

from contextlib import closing
from operator import itemgetter

admin.site.disable_action('delete_selected')

numMatches = 10
totalQuestions = 10

@admin.register(Lustudent)
class LustudentAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'lnumber', 'emailaddress', 'gender', 'paid']
    ordering = ['lnumber']
    actions = ['generateMatches','markPaid']

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
        students = queryset()
        for student in students:
            html_message = loader.render_to_string('bisonMatchApp/results_email.html', {'name': results})
            if student.paid:
                subject = "BisonMatch Reminder"
                message = "Reminder that your BisonMatch results will be available via email Monday February 11, just in time to find a Valentine's Date!"
                message += "\n Have a wonderful day!"
                message += "Love, \n Your Friends at BisonMatch"
            else: 
                subject = "Its Not Too Late To Find Love!"
                message = "Hi " + student.name + "! It is not too late for you to buy your results from BisonMatch!\n"
                message += "Visit " + loader.render_to_string('thanks/') + " or stop by the BisonMatch table in the student center to pay for your results.\n" 
                message += "Once you have paid, you will receive your results via email on Monday February 11, just in time to find a Valentine's Date!"
                message += "\n Have a wonderful day!"
                message += "Love, \n Your Friends at BisonMatch"
            #Send email with appropriate subject and message
            send_mail(
                subject, #subject
                message,   #body
                'bisonmatch2.0@gmail.com', #from us
                [student.emailAddress], #to student
                fail_silently=False,
                html_message=html_message
            )
        return
    sendReminderEmail.short_description = 'Send Reminder to Students (Ensure all selected)'
    #MADELYN EDIT THIS
    def sendMatchEmails(self, request, queryset):
        students = queryset()
        for student in students:
            matchlink = "bisonmatch.info/matches/" + student.lnumber
            paylink = "bisonmatch.info/thanks/"
            html_message = loader.render_to_string('bisonMatchApp/results_email.html', {'name': results})
            if student.paid:
                subject = "Your BisonMatch Results Are Now Available!!!"
                message = "Hi " + student.name + "! \nThank you for supporting your local "
                message += "Association for Computing Machinery (ACM) Chapter by buying your results!\n"
                message += "Your BisonMatch results can be viewed here:\n" + matchlink + "\nHappy Valentine's Day!"
                message += "Love, \n Your Friends at BisonMatch"
            else: 
                subject = "Its Not Too Late To Find Love!"
                message = "Hi " + student.name + "! It is not too late for you to buy your results from BisonMatch!\n"
                message += "Visit " + paylink + " to pay for your results.\n" 
                message += "Once you have paid, you can view your results here: \n" + matchlink + "\nHappy Valentine's Day!"
                message += "Love, \n Your Friends at BisonMatch"
            #Send email with appropriate subject and message
            send_mail(
                subject, #subject
                message,   #body
                'bisonmatch2.0@gmail.com', #from us
                [student.emailAddress], #to student
                fail_silently=False,
                html_message=html_message
            )
        return
    sendMatchEmails.short_description = 'Send Match Link to Students (Ensure all selected)'
    


@admin.register(StudentMatches)
class StudentMatchesAdmin(admin.ModelAdmin):
    list_display = ['studentlnumber', 'matchlnumber', 'percent']
    ordering = ['studentlnumber']
    actions = ['delete_selected', 'sendResultEmail']

    def sendResultEmail(self,request, queryset):
        #TODO
        return
    sendResultEmail.short_description = 'Send results to students who paid.'

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
        potentialStudents = Lustudent.objects.filter(lnumber != student.lnumber)

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
