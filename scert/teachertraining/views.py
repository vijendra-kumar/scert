# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from forms import TrainingForm
from .models import TrainingPlan, Teacher, Training, TrainingPlanDetail, Prerequisite, Postrequisite, TrainingPlanEnrollment, TrainingPrerequisiteStatus, TrainingPrerequisiteStatus, TrainingPostrequisiteStatus
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse

def validate_Teachers(request,prk):
    tpDetails = TrainingPlanDetail.objects.get(pk=prk)
    n = tpDetails.traingId
    mydict = request.POST.dict()
    print 'validateTeachers'
    print mydict
    tnames = mydict['teachers_empId']
    tpeItr = tpDetails.trainingplanenrollment_set.all()
    alreadyRegister = []
    notValidTeacher = []
    for j in tnames.split(','):
        print 'inside split %s' %(j)
        try:
            e = Teacher.objects.get(empId=j)
            print 'e is %s' %(e.empId)
            lTrainingPlanEnrollments = e.trainingplanenrollment_set.all()
            for ltpeItr in lTrainingPlanEnrollments:
                print 'atleast one enrollment'
                print '%s' %(ltpeItr.trainingPlanDetailId.traingId)
                print '%s' %(n.id)
                if ltpeItr.trainingPlanDetailId.traingId.id == n.id:
                    print 'found matching'
                    alreadyRegister.append(j)
                    break
        except Exception as e:
            notValidTeacher.append(j)
    arMessage = ''
    nvtmessage = ''
    if alreadyRegister:
        arMessage = 'Teachers who have already enrolled for this training: %s' %(','.join([str(x) for x in alreadyRegister]))
    if notValidTeacher:
        nvtmessage = 'No valid teacher profile present with emp Id: %s' %(','.join([str(x) for x in notValidTeacher]))
    print arMessage
    print nvtmessage
    data = {
        'already_enrolled': alreadyRegister,'notValid_teacher': notValidTeacher
    }
    return JsonResponse(data)


def CompletePrerequisites(request,prk):
    tpe = TrainingPlanEnrollment.objects.get(id=prk)
    lTraining = tpe.trainingPlanDetailId.traingId
    lpre = lTraining.prerequisite_set.all()
    return render(request,'TeacherWorklistTrainingDetail.html',{'training':lTraining,'PreItr':lpre, 'tpe':tpe})

def CompletePostrequisites(request,prk):
    tpe = TrainingPlanEnrollment.objects.get(id=prk)
    lTraining = tpe.trainingPlanDetailId.traingId
    lpre = lTraining.postrequisite_set.all()
    return render(request,'TeacherPostRequisitePage.html',{'training':lTraining,'PreItr':lpre, 'tpe':tpe})

    
def handle_uploaded_file(f,training, preName):
    filepath = '/'+training+'/'+preName+'.txt'
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def submitPrerequisite(request,prk):
    if request.method == 'POST':
        print request
        lpreItr = Prerequisite.objects.get(id=prk).trainingprerequisitestatus_set.all()
        ltpe = None
        for itr in lpreItr:
            ltpe = itr.TrainingPlanEnrollmentId
            training = itr.TrainingPlanEnrollmentId.trainingPlanDetailId.traingId.name
            preName = itr.TrainingPrerequisiteId.name
            handle_uploaded_file(request.FILES['file'],training, preName)
        if ltpe is not None:
            lTraining = ltpe.trainingPlanDetailId.traingId
            lpre = lTraining.prerequisite_set.all()            
            return render(request,'TeacherWorklistTrainingDetail.html',{'training':lTraining,'PreItr':lpre})



def ApproveRegistration(request):
    mydict = request.POST.dict()
    print mydict
    print 'testing'
    enrollmentid = mydict['enrollmentid']
    enroll = TrainingPlanEnrollment.objects.get(id=enrollmentid)
    print enroll.teacherId.name
    print enroll.trainingPlanDetailId.traingId.name
    enroll.trainingStatus = TrainingPlanEnrollment.PRETRAININGREQUISITE
    enroll.save()
    print enroll.trainingStatus
    data = {}
    return JsonResponse(data)

def ReviewPreRequisite(request):
    pass
"""    mydict = request.POST.dict()
    print mydict
    print 'testing'
    enrollmentid = mydict['enrollmentid']
    enroll = TrainingPlanEnrollment.objects.get(id=enrollmentid)
    print enroll.teacherId.name
    print enroll.trainingPlanDetailId.traingId.name
    training = enroll.trainingPlanDetailId.traingId
    lprq = training.prerequisite_set.all()
    for itr in lprq:

    enroll.trainingStatus = TrainingPlanEnrollment.PRETRAININGREQUISITE
    enroll.save()
    print enroll.trainingStatus
    data = {}
    return JsonResponse(data)
"""

def AddTraining(request):
    if request.method == 'POST':
        lform = TrainingForm(request)
        return render(request, {'from':lform})
    else:
        lform = TrainingForm()
        return render(request,'AdminAddTrainings.html',{'form':lform})  

def getTeacherTrainings(request):
    lteacher = mydict['teacher_empId']
    e = Teacher.objects.get(empId=lteacher)
    print 'e is %s' %(e.empId)
    lTrainingPlanEnrollments = e.trainingplanenrollment_set.all()
    for ltpeItr in lTrainingPlanEnrollments:
        print ltpeItr.trainingPlanDetailId.traingId.name
    return render(request,'AdminTeacherEnquiryDetails.html',{'tpe':lTrainingPlanEnrollments}) 



def TeachersEnquiry(request):
    if request.method == 'POST':
        mydict = request.POST.dict()
        print mydict
        print 'testing'
        lteacher = mydict['teacher_empId']
        e = Teacher.objects.get(empId=lteacher)
        print 'e is %s' %(e.empId)
        lTrainingPlanEnrollments = e.trainingplanenrollment_set.all()
        for ltpeItr in lTrainingPlanEnrollments:
            print ltpeItr.trainingPlanDetailId.traingId.name
        return render(request,'AdminTeacherEnquiryDetails.html',{'tpe':lTrainingPlanEnrollments}) 
    else:
        e = Teacher.objects.get(user=request.user)
        print 'e is %s' %(e.empId)
        lTrainingPlanEnrollments = e.trainingplanenrollment_set.all()
        for ltpeItr in lTrainingPlanEnrollments:
            print ltpeItr.trainingPlanDetailId.traingId.name
        return render(request,'TeacherTrainings.html',{'tpe':lTrainingPlanEnrollments,'message':"WORKLIST"}) 


def TrainingEnquiry(request):
    if request.method == 'POST':
        mydict = request.POST.dict()
        print mydict
        print 'testing'
        ltraining = mydict.get('training_id',None)
        if ltraining is None:
            lAll = Training.objects.all()
        try:
            t = Training.objects.get(id=ltraining)
        except Exception as e:
            message = "Training id "+ltraining+ " does not exist."
            return render(request,'AdminTrainingEnquiry.html',{'message':message})
        print 't is %s' %(t.name)
        lTrainingPlanDetails = t.trainingplandetail_set.all()
        return render(request,'AdminTrainingEnquiryDetails.html',{'tpd':lTrainingPlanDetails}) 
    else:
        return render(request,'AdminTrainingEnquiry.html')

def AllTrainings(request):
    lAll = Training.objects.all()
    return render(request,'AdminAllTrainings.html',{'lAll':lAll})
                

def AddTrainingPlan(request):
    if request.method == 'POST':
        lform = TrainingPlanForm(request)
        return render(request, {'from':lform})
    else:
        lform = TrainingPlanForm()
        return render(request,'AdminAddTrainingPlan.html',{'form':lform})  

# Create your views here.
def mainpage(request):
    return render(request, 'index.html', {'message':''})


def loginx(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print request.POST  
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print user.username
            if user.is_staff:
                return render(request, 'BaseAdminLogin.html',{'user':user})
            else:
                return render(request, 'BaseTeacherLogin.html',{'user':user})
        else:
            return HttpResponse("Invalid login")
    # if a GET (or any other method) we'll create a blank form

    else:
        context = {'message': "Invalid username or password..."}
    return render(request, 'index.html',context)

def Logout(request):
    user = logout(request)
    return render(request, 'index.html')

def Worklist(request):
    lTrainingPlanItr = TrainingPlan.objects.all()
    return render(request, 'AdminWorklistMain.html',{'lTrainingPlanItr':lTrainingPlanItr})
#    return render(request, 'AdminWorklistTree.html',{'lTrainingPlanItr':lTrainingPlanItr})

def WorklistTrainings(request,prk):
    print 'worklistTraining tset'
    ltpd = TrainingPlan.objects.filter(id=prk)
    for itr in ltpd:
        tpDetails = itr.trainingplandetail_set.all()
        return render(request,'AdminWorklistTraining.html',{'tpDetails':tpDetails, 'tp':itr})

def WorklistTrainingDetail(request,prk):
    print request.user
    if request.user.is_staff:
        lt = TrainingPlanDetail.objects.filter(id=prk)
        for itr in lt:
            tpeItr = itr.trainingplanenrollment_set.all()
            if request.user.is_staff:
                 return render(request,'AdminWorklistTrainingDetail.html',{'training':itr.traingId, 'tpe':tpeItr,'ltpd':itr}) 
    else:
        ltpe = TrainingPlanEnrollment.objects.get(id=prk)
        return render(request,'TeacherWorklistTrainingDetail.html',{'tpe':ltpe})                 

def home(request):
    # if this is a POST request we need to process the form data
    if request.user.is_staff:
        return render(request, 'BaseAdminLogin.html',{'user':request.user})
    else:
        return render(request, 'BaseTeacherLogin.html',{'user':request.user})

def trainingDetails(request):
    if request.user.is_authenticated:
        print('%s logged in' %(request.user))
        lteacherset = Teacher.objects.filter(user=request.user)
        for lteacher in lteacherset:
            print lteacher
            lTrainingsEnrolled = TrainingPlanEnrollment.objects.filter(teacherId=lteacher.id)
            print lTrainingsEnrolled
            for lte in lTrainingsEnrolled:
                print lte.trainingPlanDetailId.traingId
        return render(request,'trainingDetails.html',{'trainings':lTrainingsEnrolled})

def AssignTraining(request,prk):
    tpDetails = TrainingPlanDetail.objects.get(pk=prk)
    mydict = request.POST.dict()
    n = tpDetails.traingId
    tnames = mydict['teachers_empId']
    tpeItr = tpDetails.trainingplanenrollment_set.all()
    for ltpe in tpeItr:
        if ltpe:
            pass
    alreadyRegister = []
    notValidTeacher = []
    for j in tnames.split(','):
        e = Teacher.objects.get(empId=j)
        if e is not None:
            lTrainingPlanEnrollments = e.trainingplanenrollment_set.all()
            for ltpeItr in lTrainingPlanEnrollments:
                if ltpeItr.trainingPlanDetailId.traingId == n.id:
                    alreadyRegister.append(j)
                    break
            try:
                enroll = TrainingPlanEnrollment()
                enroll.trainingPlanDetailId = tpDetails
                enroll.teacherId = e
                enroll.save()
                #Find out the training pre-requisites and create pre-requisite status objects.
                for itr in n.prerequisite_set.all():
                    lpre = TrainingPrerequisiteStatus()
                    lpre.TrainingPrerequisiteId = itr
                    lpre.TrainingPlanEnrollmentId = enroll
                    lpre.save()

                for itr1 in n.postrequisite_set.all():
                    lpost = TrainingPrerequisiteStatus()
                    lpost.TrainingPostrequisiteId = itr1
                    lpost.TrainingPlanEnrollmentId = enroll
                    lpost.save()

                print 'teacher %s enrolled in training %s' %(e, n)                
            except IntegrityError as e:
                pass
        else:
            notValidTeacher.append(j)
    return render(request,'AdminWorklistTrainingDetail.html',{'training':n, 'tpe':tpeItr,'ltpd':tpDetails, 'armessage':alreadyRegister, 'nvtmessage':notValidTeacher})             
#return redirect('/admin/teachertraining/trainingplan/')
    
def TeachersEnrolled(request,prk):
    tp = TrainingPlan.objects.get(pk=prk)
    tpDetails = tp.trainingplandetail_set.all()
    for tpd in tpDetails:
        tpenrolled = tpd.trainingplanenrollment_set.all()
    return render(request, 'teachersenrolled.html',{'pk':prk, 'tpDetails':tpDetails, 'tp':tp})


def RegisterTraining(request):
    if request.user.is_authenticated:
        print('%s logged in' %(request.user))
        lteacherset = Teacher.objects.filter(user=request.user)
        if lteacherset != None:
            for lteacher in lteacherset:
                print lteacher
                lTrainingsEnrolled = TrainingPlanEnrollment.objects.filter(teacherId=lteacher.id)
                for lte in lTrainingsEnrolled:
                    if lte.trainingStatus == TrainingPlanEnrollment.NOMINATED:
                        return render(request,'TeacherRegisterTraining.html',{'trainings':lTrainingsEnrolled,'heading':"YOU NEED TO REGISTER FOR BELOW TRAININGS",'whichTraining':"register"})    
        return render(request,'TeacherRegisterTrainingFailed.html',{'heading':"NO TRAININGS TO REGISTER"})


def InProgressTraining(request):
    if request.user.is_authenticated:
        print('%s logged in' %(request.user))
        lteacherset = Teacher.objects.filter(user=request.user)
        if lteacherset != None:
            for lteacher in lteacherset:
                print lteacher
                lTrainingsEnrolled = TrainingPlanEnrollment.objects.filter(teacherId=lteacher.id)
                for lte in lTrainingsEnrolled:
                    if lte.trainingStatus != TrainingPlanEnrollment.COMPLETE:
                        return render(request,'TeacherRegisterTraining.html',{'trainings':lTrainingsEnrolled,'heading':"YOUR TRAININGS IN PROGRESS",'whichTraining':"inProgress"})    
        return render(request,'TeacherRegisterTrainingFailed.html',{'heading':"NO TRAININGS IN PROGRESS"})


def CompletedTraining(request):
    if request.user.is_authenticated:
        print('%s logged in' %(request.user))
        lteacherset = Teacher.objects.filter(user=request.user)
        if lteacherset != None:
            for lteacher in lteacherset:
                print lteacher
                lTrainingsEnrolled = TrainingPlanEnrollment.objects.filter(teacherId=lteacher.id)
                for lte in lTrainingsEnrolled:
                    if lte.trainingStatus == TrainingPlanEnrollment.COMPLETE:
                        return render(request,'TeacherRegisterTraining.html',{'trainings':lTrainingsEnrolled,'heading':"YOUR COMPLETED TRAININGS",'whichTraining':"complete"})    
        return render(request,'TeacherRegisterTrainingFailed.html',{'heading':"NO COMPLETE TRAININGS"})


def Register(request,prk):
    if request.user.is_authenticated:
        print('%s logged in' %(request.user))
        tpe = TrainingPlanEnrollment.objects.filter(id=prk)
        for tpei in tpe:
            lTrainingsEnrolled = TrainingPlanEnrollment.objects.filter(teacherId=tpei.teacherId.id)
            ltraining = tpei.trainingPlanDetailId.traingId.name            
            print tpei.trainingStatus
            if tpei.trainingStatus == TrainingPlanEnrollment.NOMINATED:
                tpei.trainingStatus = TrainingPlanEnrollment.REGISTRATIONDONE
                tpei.save()
                heading = "You have successfully registered for "
                return render(request,'TeacherRegisterTraining.html',{'trainings':lTrainingsEnrolled,'heading':heading, 'training':ltraining})    
            else:
                heading = "You have already registered for this training."
        return render(request,'TeacherRegisterTraining.html',{'trainings':lTrainingsEnrolled,'heading':heading, 'training':ltraining})    

def RegisterFromWorklist(request,prk):
    if request.user.is_authenticated:
        print('%s logged in' %(request.user))
        tpe = TrainingPlanEnrollment.objects.get(id=prk)
        lTrainingsEnrolled = TrainingPlanEnrollment.objects.filter(teacherId=tpe.teacherId.id)
        ltraining = tpe.trainingPlanDetailId.traingId.name            
        print tpe.trainingStatus
        if tpe.trainingStatus == TrainingPlanEnrollment.NOMINATED:
            tpe.trainingStatus = TrainingPlanEnrollment.REGISTRATIONDONE
            tpe.save()
            return render(request,'TeacherTrainings.html',{'tpe':lTrainingsEnrolled, 'message':"You have successfully registered for ",'training':ltraining })
        return render(request,'TeacherTrainings.html',{'tpe':lTrainingsEnrolled, 'message':"WORKLIST" })        


def Profile(request):
    if request.user.is_authenticated:
        print('%s logged in' %(request.user))

        lteacherset = Teacher.objects.filter(user=request.user)
        if lteacherset != None:
            for lteacher in lteacherset:
                return render(request,'TeacherProfile.html',{'profile':lteacher,'flag':'True'})            
        return render(request,'TeacherProfile.html',{'flag':'false'})                        


def TeacherSubmitsPrerequisite(request,prk):
    if request.user.is_authenticated:
        print('%s logged in' %(request.user))
        tpe = TrainingPlanEnrollment.objects.get(id=prk)
        if tpe.trainingStatus == TrainingPlanEnrollment.PRETRAININGREQUISITE:
            if tpe.TrainingPrerequisiteStatus == TrainingPlanEnrollment.INITIAL:
                tpe.TrainingPrerequisiteStatus = TrainingPlanEnrollment.SUBMITTED
                tpe.save()
        lTraining = tpe.trainingPlanDetailId.traingId
        return render(request,'TeacherWorklistTrainingDetail.html',{'training':lTraining, 'tpe':tpe, 'message':"Pre requistes submitted successfully."})            

def TeacherSubmitsPostrequisite(request,prk):
    if request.user.is_authenticated:
        print('%s logged in' %(request.user))
        tpe = TrainingPlanEnrollment.objects.get(id=prk)
        if tpe.trainingStatus == TrainingPlanEnrollment.POSTTRAININGREQUISITE:
            if tpe.TrainingPostrequisiteStatus == TrainingPlanEnrollment.INITIAL:
                tpe.TrainingPostrequisiteStatus = TrainingPlanEnrollment.SUBMITTED
                tpe.save()
        lTraining = tpe.trainingPlanDetailId.traingId
        return render(request,'TeacherWorklistTrainingDetail.html',{'training':lTraining, 'tpe':tpe, 'message':"Pre requistes submitted successfully."})            

def MoveToMainTraining(request,prk):
    ltpe = TrainingPlanEnrollment.objects.get(id=prk)
    if ltpe.trainingStatus == TrainingPlanEnrollment.PRETRAININGREQUISITE:
        ltpe.trainingStatus = TrainingPlanEnrollment.MAINTRAINING
        ltpe.TrainingPrerequisiteStatus = TrainingPlanEnrollment.APPROVED
        ltpe.save()

    if request.user.is_staff:
        lt = ltpe.trainingPlanDetailId
        tpeItr = lt.trainingplanenrollment_set.all()
        if request.user.is_staff:
            return render(request,'AdminWorklistTrainingDetail.html',{'training':lt.traingId, 'tpe':tpeItr,'ltpd':lt})     


def MoveToPost(request,prk):
    ltpe = TrainingPlanEnrollment.objects.get(id=prk)
    print ltpe.id
    if ltpe.trainingStatus == TrainingPlanEnrollment.MAINTRAINING:
        print ltpe.trainingStatus
        ltpe.trainingStatus = TrainingPlanEnrollment.POSTTRAININGREQUISITE
        print ltpe.trainingStatus
        ltpe.save()
    if request.user.is_staff:
        lt = ltpe.trainingPlanDetailId
        tpeItr = lt.trainingplanenrollment_set.all()
        if request.user.is_staff:
            return render(request,'AdminWorklistTrainingDetail.html',{'training':lt.traingId, 'tpe':tpeItr,'ltpd':lt})                 

def MoveToComplete(request,prk):
    ltpe = TrainingPlanEnrollment.objects.get(id=prk)
    print ltpe.id
    print ltpe.trainingStatus
    if ltpe.trainingStatus == TrainingPlanEnrollment.POSTTRAININGREQUISITE:
        print ltpe.trainingStatus
        ltpe.trainingStatus = TrainingPlanEnrollment.COMPLETE
        print ltpe.trainingStatus
        ltpe.save()
    if request.user.is_staff:
        lt = ltpe.trainingPlanDetailId
        tpeItr = lt.trainingplanenrollment_set.all()
        if request.user.is_staff:
            return render(request,'AdminWorklistTrainingDetail.html',{'training':lt.traingId, 'tpe':tpeItr,'ltpd':lt})                             