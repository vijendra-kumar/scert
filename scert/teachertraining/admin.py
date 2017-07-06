# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.html import format_html
from django.contrib import admin
from django.shortcuts import reverse, redirect
from .models import TrainingPlan, Teacher, Training, TrainingPlanDetail, Prerequisite, Postrequisite, TrainingPlanEnrollment
from . import views
from . import forms
from django.conf.urls import url
from django.contrib.admin import AdminSite

# Register your models here.
class TrainingPlanInline(admin.TabularInline):
    model = TrainingPlanDetail
    extra = 0
    fields = ('id','traininPlanId', 'traingId', 'fundingSource', 'start_date', 'end_date' )

class TrainingPlanAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(TrainingPlanAdmin,self).get_urls()
        custom_urls = [
            url(
                r'^/enrollTeachers/$',
                self.admin_site.admin_view(self.enroll_teachers),
                name='enrollteachers-training',
            ),
        ]
        return custom_urls + urls
    def TeachersEnrolled(self, obj):
        return format_html('<a class="button" href="{}">ViewTeachersEnrolled</a>',
            '/tt/TeachersEnrolled/%s' %( obj.pk))
    TeachersEnrolled.short_description = 'TeachersEnrolled'
    TeachersEnrolled.allow_tags = True 

    def AssignTrainingToTeachers(self, obj):
        return format_html('<a class="button" href="{}">AssignTrainingToTeachers</a>',
            '/tt/AssignTraining/%s' %( obj.pk))
    AssignTrainingToTeachers.short_description = 'TeachersAssignment'
    AssignTrainingToTeachers.allow_tags = True    
    list_display = ('id', 'name', 'start_date','end_date', 'AssignTrainingToTeachers', 'TeachersEnrolled')
    fields = ('name',('start_date','end_date'))
    inlines = [TrainingPlanInline]
    actions = [AssignTrainingToTeachers,TeachersEnrolled]

    def enroll_teachers(
        self,
        request,
        args):
        if request.method != 'POST':
            form = forms()
            print 'send the form'
        else:
            form = forms(request.POST)
            print args
            if form.is_valid():
                print 'form is valid'
        return redirect('/admin/teachertraining/trainingplan/')

admin.site.register(TrainingPlan, TrainingPlanAdmin)



# Register your models here.
class TrainingPreInline(admin.TabularInline):
    model = Prerequisite
    extra = 0
    fields = ('name','description')

class TrainingPostInline(admin.TabularInline):
    model = Postrequisite
    extra = 0
    fields = ('name','description')


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'duration')
    inlines = [TrainingPreInline, TrainingPostInline]

admin.site.register(Training, TrainingAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'empId', 'subject', 'joining_date', 'email')

admin.site.register(Teacher, TeacherAdmin)

admin.site.site_header = "SCERT Administration"
admin.site.site_url='/tt/home'
