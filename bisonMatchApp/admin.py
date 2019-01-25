from django.contrib import admin
from .models import Lustudent, StudentMatches
from django.http import HttpResponseRedirect
from django.db import IntegrityError, DatabaseError, connection

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
        paidStudents = queryset.filter(paid = 1)
        totalInserts = 0
        for student in paidStudents:
            matches = getMatchesForStudent(student) #list of dictionaries
            totalInserts += len(matches)
            for match in matches:
                try:
                    StudentMatches.objects.create(studentlnumber=student.lnumber, matchlnumber=match['lnumber'], percent=match['percent'])
                except (IntegrityError, DatabaseError):
                    self.message_user(request, "An error occured with your request, match %s with %s was not added to StudentMatches"% (student.lnumber, match['lnumber']))
        self.message_user(request, 'Done: %s rows should have been inserted' %totalInserts)
        return HttpResponseRedirect("../studentmatches/")
    generateMatches.short_description = 'Generate matches for all paid students'


    def sendNotPaidEmail(self,request, queryset):
        #TODO
        return
    sendNotPaidEmail.short_description = 'Send reminder to students who have not paid.'


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
