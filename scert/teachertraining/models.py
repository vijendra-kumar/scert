# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    empId = models.IntegerField(unique=True)
    aadhar_no = models.IntegerField(unique=True)
    age = models.IntegerField()
    joining_date = models.DateField('joining date')
    last_promotion_date = models.DateField('last promotion date')
    subject = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.IntegerField()
    def __str__(self):
        return '%s' % (self.name)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if not sender.is_superuser:
            if created:
                print 'not a superuser'
                Teacher.objects.create(user=instance)
            else:
                instance.teacher.save()


class TrainingPlan(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField('training plan start date')
    end_date = models.DateField('training plan end date')
    def __str__(self):
        return '%s' % (self.name)        

class Training(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField()
    type_of_training = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    def __str__(self):
        return '%s' % (self.name)
    
class TrainingPlanDetail(models.Model):
    FundingSource1 = 'FS1'
    FundingSource2 = 'FS2'
    FundingSource3 = 'FS3'
    FundingSource4 = 'FS4'
    FUNDING_SOURCE = (
        (FundingSource1, 'FundSource1'),
        (FundingSource2, 'FundSource2'),
        (FundingSource3, 'FundSource3'),
        (FundingSource4, 'FundSource4'),
    )
    traininPlanId = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    traingId = models.ForeignKey(Training, on_delete=models.CASCADE)
    fundingSource = models.CharField(
        max_length = 3,
        choices = FUNDING_SOURCE,
        default = FundingSource1,
    )
    start_date = models.DateField('training start date')
    end_date = models.DateField('training end date')
    def __str__(self):
        return '%s' %(self.traingId)
    


class Prerequisite(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    TrainingId = models.ForeignKey(Training, on_delete=models.CASCADE)

class Postrequisite(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    TrainingId = models.ForeignKey(Training, on_delete=models.CASCADE)
    
    
class TrainingPlanEnrollment(models.Model):
    INITIAL = 'INITIAL'
    SUBMITTED = 'SUBMITTED'
    APPROVED = 'APPROVED'
    REQUISITE_STATUS = (
        (INITIAL, 'Initial'),
        (SUBMITTED, 'Submitted'),
        (APPROVED, 'Approved'),
    )
    NOMINATED = 'NOMINATED'
    REGISTRATIONDONE = 'REGISTRATIONDONE'
    PRETRAININGREQUISITE = 'PRE-REQUISITE'
    MAINTRAINING = 'MAINTRAINING'
    POSTTRAININGREQUISITE = 'POST-REQUISITE'
    COMPLETE = 'COMPLETE'
    DISQUALIFIED = 'DISQUALIFIED'
    TRAINING_STATUS = (
        (NOMINATED, 'Nominated'),
        (REGISTRATIONDONE, 'RegistrationDone'),
        (PRETRAININGREQUISITE, 'PreTrainingRequisite'),
        (MAINTRAINING, 'MainTraining'),
        (POSTTRAININGREQUISITE, 'PostTrainingRequisite'),
        (COMPLETE, 'Complete'),
        (DISQUALIFIED, 'Disqualified'),
    )
    trainingPlanDetailId = models.ForeignKey(TrainingPlanDetail, on_delete=models.CASCADE)
    teacherId = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    trainingStatus = models.CharField(
        max_length = 16,
        choices = TRAINING_STATUS,
        default = NOMINATED,
    )
    TrainingPrerequisiteStatus = models.CharField(
        max_length = 9,
        choices = REQUISITE_STATUS,
        default = INITIAL,
    )
    TrainingPostrequisiteStatus = models.CharField(
        max_length = 9,
        choices = REQUISITE_STATUS,
        default = INITIAL,
    )    
    class Meta:
        unique_together = ('teacherId', 'trainingPlanDetailId')

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{}/{1}'.format(instance.user.id,'pre', filename)

class TrainingPrerequisiteStatus(models.Model):
    TrainingStatusId = models.ForeignKey(TrainingPlanEnrollment, on_delete=models.CASCADE)
    TrainingPrerequisiteId = models.ForeignKey(Prerequisite, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)


class TrainingPrerequisiteComments(models.Model):
    TrainingPrerequisiteStatusId = models.ForeignKey(TrainingPrerequisiteStatus, on_delete=models.CASCADE)
    comment = models.CharField(max_length = 200)
    

def user_directory_path_post(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{}/{1}'.format(instance.user.id,'post', filename)

class TrainingPostrequisiteStatus(models.Model):
    TrainingStatusId = models.ForeignKey(TrainingPlanEnrollment, on_delete=models.CASCADE)
    TrainingPostrequisiteId = models.ForeignKey(Postrequisite, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path_post)

class TrainingPostrequisiteComments(models.Model):
    TrainingPostrequisiteStatusId = models.ForeignKey(TrainingPostrequisiteStatus, on_delete=models.CASCADE)
    comment = models.CharField(max_length = 200)
