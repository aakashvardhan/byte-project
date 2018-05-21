from django import forms
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Schedule
# from .models import SurveyChoice

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(max_length=200, help_text='Required')
    last_name = forms.CharField(max_length=200,help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name','password1', 'password2')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EventForm(forms.ModelForm):
	class Meta:
		model = Schedule
		fields = ('title','day','start_time','venue','notes',)


class EntryForm(forms.Form):
    name = forms.CharField(max_length=100)
    date = forms.DateTimeField()
    description = forms.CharField(widget=forms.Textarea)