from django import forms
from django.forms import ModelForm
from models import Training,TrainingPlan, TrainingPlanDetail

class TrainingForm(ModelForm):
    class Meta:
    	model = Training
    	fields = '__all__'

class TrainingPlanForm(ModelForm):
    class Meta:
    	model = TrainingPlan
    	fields = '__all__'

