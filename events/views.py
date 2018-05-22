from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .models import Schedule,Attending,NotAttending,EventAttendance

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate,logout

from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm,SignupForm,EventForm

from django.contrib.auth.models import User

from django.urls import reverse

from django.forms import formset_factory,BaseFormSet

import requests

from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import PasswordChangeForm

from django.conf import settings

from django.contrib import messages

from django.template.loader import render_to_string

from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token

from django.core.mail import EmailMessage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime


from django.views.generic import TemplateView, ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def index(request):
	if request.user.is_authenticated:
		return redirect('events:dashboard')
	

	return render(request, 'events/index.html')

def log_in(request):
    if request.user.is_authenticated:
        return redirect('polls:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
        	recaptcha_response = request.POST.get('g-recaptcha-response')
        	data = {
        		'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        		'response': recaptcha_response
        	}
        	r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        	result = r.json()
        	print(result)
        	if result['success']:
	            username = form.cleaned_data.get('username')
	            password = form.cleaned_data.get('password')
	            user = authenticate(username=username, password=password)
	            if user is not None:
	                if user.is_active:
	                    login(request, user)
	                    return redirect('events:dashboard')
	            else:
	                return render(request,'events/login.html',{'form' : form,'user' : user})
	        else:
	        	messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    else:
        form = UserLoginForm
    context = { 'form' : form }
    return render(request,'events/login.html', context)

@login_required(login_url='/login')
def log_out(request):
    logout(request)
    return redirect('events:index')



def register(request):
    if request.user.is_authenticated:
        return redirect('events:dashboard')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            print(result)

            if result['success']:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('events/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token':account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    else:
        form = SignupForm()

    context = { 'form' : form }
    return render(request, 'events/register.html', context)

@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('events:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'events/change_password.html', {
        'form': form
    })


def activate(request, uidb64, token, 
backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, 
backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Thank you for your email confirmation. Now you have logged In')
        return redirect('events:dashboard')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required(login_url='/login')
def dashboard(request):
    # username = request.user
    # event_list = Schedule.objects.all().exclude(username=username)
    # latest_event_list = event_list.order_by('id')
    # paginator = Paginator(latest_event_list,5)
    # page = request.GET.get('page')
    # events = paginator.get_page(page)
    # context = {
    #     'events':events,
    #     'latest_event_list':latest_event_list
    # }
    # return render(request, 'events/dashboard.html')
    username = request.user
    latest_event_list = Schedule.objects.exclude(username = username)

    context = {
        'latest_event_list': latest_event_list,
    }
    return render(request, 'events/dashboard.html',context)
@login_required(login_url='/login')
def attendance(request,title_id):
    username = request.user
    event = get_object_or_404(Schedule,pk=title_id)
    try:

        selected_event = Attending.objects.get(username=username,title=event.title)
        print(selected_event)

    except Attending.DoesNotExist:
        selected_event = None
        if NotAttending.objects.filter(username=username,title=event.title).exists():
            messages.error(request, 'You are already not attending this event!')
            return redirect('events:dashboard')
        else:
            create_event = Attending.objects.create(username=username,title=event.title)

    if selected_event == None:
        event.attending += 1
        print(event.attending)
        event.save()
        messages.success(request, 'You are attending this event!')
        return redirect('events:dashboard')
    else:
        messages.error(request, 'You are already attending this event!')
        return redirect('events:dashboard')

@login_required(login_url='/login')
def not_attending(request,title_id):
    username = request.user
    event = get_object_or_404(Schedule,pk=title_id)
    try:

        selected_event = NotAttending.objects.get(username=username,title=event.title)
        print(selected_event)

    except NotAttending.DoesNotExist:
        selected_event = None
        if Attending.objects.filter(username=username,title=event.title).exists():
            messages.error(request, 'You are already attending this event!')
            return redirect('events:dashboard')
        else:
            create_event = NotAttending.objects.create(username=username,title=event.title)

    if selected_event == None:
        event.not_attending += 1
        event.save()
        messages.success(request, 'Wish you came to the event!')
        return redirect('events:dashboard')
    else:
        messages.error(request, 'You are already not attending this event!')
        return redirect('events:dashboard')

@login_required(login_url='/login')
def my_events(request):
    username = request.user
    my_events = Attending.objects.filter(username=username)
    return render(request,'events/my_events.html', {'my_events':my_events})


@login_required(login_url='/login')
def list_of_attendees(request,title):
    username = request.user
    events = Attending.objects.filter(title=title)
    print(events)

    return render(request,'events/list_of_attendees.html',{'events':events})

@login_required(login_url='/login')
def event_list(request):
	username = request.user
	events_list = Schedule.objects.filter(username=username)
	context = {
		'events_list':events_list,
	}
	return render(request,'events/event_list.html', context)

@login_required(login_url='/login')
def create_event(request):
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			username = request.user
			event = username.schedule_set.create(title=request.POST['title'],day=request.POST['day'],start_time=request.POST['start_time'],venue=request.POST['venue'],notes=request.POST['notes'])
			print(event)
			return redirect('events:event_list')

	else:
		form = EventForm()
	username = request.user
	events_list = Schedule.objects.filter(username=username)
	context = {'form':form,'events_list':events_list}
	return render(request,'events/create_event.html', context)


@login_required(login_url='/login')
def edit_event(request,title_id):
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			event = get_object_or_404(Schedule,pk=title_id)
			event.title = request.POST['title']
			event.day = request.POST['day']
			event.start_time = request.POST['start_time']
			event.venue = request.POST['venue']
			event.notes = request.POST['notes']
			event.save()
			return redirect('events:event_list')
	else:
		event = get_object_or_404(Schedule,pk=title_id)
		data = {'title': event.title,'day':event.day,'start_time':event.start_time,'venue':event.venue,'notes':event.notes}
		form = EventForm(data)

	context = {'form':form, 'event':event}
	return render(request,'events/edit_event.html',context)

@login_required(login_url='/login')
def delete_event(request,title_id):
	event = get_object_or_404(Schedule,pk=title_id)
	event.delete()
	return redirect('events:event_list')









