from django.conf.urls import url

from . import views

app_name = 'teachertraining'
urlpatterns = [
    url(r'^$', views.mainpage, name='mainpage'),
    url(r'^login/', views.loginx, name='login'),
    url(r'^home/', views.home, name='home'),    
    url(r'^trainingDetails/', views.trainingDetails, name='trainingDetails'),
    url(r'^AssignTraining/(?P<prk>[a-zA-z0-9]*)', views.AssignTraining, name='assignTraining'),
    url(r'^RegisterTraining/', views.RegisterTraining, name='RegisterTraining'),    
    url(r'^InProgressTraining/', views.InProgressTraining, name='InProgressTraining'),    
    url(r'^CompletedTraining/', views.CompletedTraining, name='CompletedTraining'),            
    url(r'^Profile/', views.Profile, name='Profile'),                
    url(r'^WorklistTrainings/(?P<prk>[a-zA-z0-9]*)', views.WorklistTrainings, name='WorklistTrainings'),                    
    url(r'^WorklistTrainingDetail/(?P<prk>[a-zA-z0-9]*)', views.WorklistTrainingDetail, name='WorklistTrainingDetail'),                        
    url(r'^validate_Teachers/(?P<prk>[a-zA-z0-9]*)', views.validate_Teachers, name='validate_Teachers'),                        
    url(r'^Worklist', views.Worklist, name='Worklist'),                    
    url(r'^Logout/', views.Logout, name='Logout'),      
    url(r'^AddTraining/', views.AddTraining, name='AddTraining'),          
    url(r'^AddTrainingPlan/', views.AddTrainingPlan, name='AddTrainingPlan'),          
    url(r'^Register/(?P<prk>[a-zA-z0-9]*)', views.Register, name='Register'),                
    url(r'^RegisterFromWorklist/(?P<prk>[a-zA-z0-9]*)', views.RegisterFromWorklist, name='RegisterFromWorklist'),                    
    url(r'^TeachersEnrolled/(?P<prk>[a-zA-z0-9]*)', views.TeachersEnrolled, name='TeachersEnrolled'),    
    url(r'^CompletePrerequisites/(?P<prk>[a-zA-z0-9]*)', views.CompletePrerequisites, name='CompletePrerequisites'),       
    url(r'^CompletePostrequisites/(?P<prk>[a-zA-z0-9]*)', views.CompletePostrequisites, name='CompletePostrequisites'),           
    url(r'^ApproveRegistration/', views.ApproveRegistration, name='ApproveRegistration'),  
    url(r'^ReviewPreRequisite/', views.ReviewPreRequisite, name='ReviewPreRequisite'),  
    url(r'^TeachersEnquiry/', views.TeachersEnquiry, name='TeachersEnquiry'),    
    url(r'^TrainingEnquiry/', views.TrainingEnquiry, name='TrainingEnquiry'),    
    url(r'^AllTrainings/', views.AllTrainings, name='AllTrainings'),    
    url(r'^submitPrerequisite/(?P<prk>[a-zA-z0-9]*)', views.submitPrerequisite, name='submitPrerequisite'),    
    url(r'^TeacherSubmitsPrerequisite/(?P<prk>[a-zA-z0-9]*)', views.TeacherSubmitsPrerequisite, name='TeacherSubmitsPrerequisite'),        
    url(r'^TeacherSubmitsPostrequisite/(?P<prk>[a-zA-z0-9]*)', views.TeacherSubmitsPostrequisite, name='TeacherSubmitsPostrequisite'),            
    url(r'^MoveToMainTraining/(?P<prk>[a-zA-z0-9]*)', views.MoveToMainTraining, name='MoveToMainTraining'),            
    url(r'^MoveToPost/(?P<prk>[a-zA-z0-9]*)', views.MoveToPost, name='MoveToPost'),                
    url(r'^MoveToComplete/(?P<prk>[a-zA-z0-9]*)', views.MoveToComplete, name='MoveToComplete'),                    
]
