from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.http import HttpResponse

from .forms import GymForm

from gyms.models import *

# Create your views here.
def dashboard(request):
	template = loader.get_template('dashboard.html')
	logged_in = False
	user = ''
	profile_complete = 0
	if is_authenticated(request):
		user = request.session.get('username')
		profile_complete = request.session.get('profile_complete')
		logged_in = True
		userObj = User.objects.filter(username=user).first()
		gymObj = Gym.objects.filter(user=userObj.pk)

		request.session['gym_count'] = gymObj.count()

		context = {
				'logged_in': logged_in,
				'username':user,
				'user':userObj,
				'gym_count': gymObj.count(),
				'profile_complete': profile_complete
				}
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/login')

def create_gym(request):
	if is_authenticated(request):
		user = request.session.get('username')
		gym_count = request.session.get('gym_count')
		userObj = User.objects.filter(username=user).first()
		if request.POST:
			gym_form = GymForm(request.POST)
			if gym_form.is_valid():
				gym = gym_form.save()
				userObj = User.objects.filter(username=user).first()
				gymObj = Gym.objects.filter(user=userObj.pk)
				request.session['gym_count'] = gymObj.count()
				return redirect("/gymadmin/gyms")
			else:
				template = loader.get_template('add_gym.html')
				context = {'gym_form':gym_form,'gym_count':gym_count,'user':userObj}
				return HttpResponse(template.render(context, request))

		gym_form = GymForm()
		template = loader.get_template('add_gym.html')
		context = {'gym_form':gym_form,'gym_count':gym_count,'user':userObj,'logged_in':True}
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/login')

def edit_gym(request,gym_id):
	if is_authenticated(request):
		user = request.session.get('username')
		userObj = User.objects.filter(username=user).first()
		gym_count = request.session.get('gym_count')
		gym = Gym.objects.filter(pk=gym_id).first()
		if gym.user_id == userObj.id:
			template = loader.get_template('gyms/edit_gym.html')
			context = {'gym':gym,'gym_count':gym_count,'user':userObj,'logged_in':True}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/gymadmin/gyms')
	else:	
		return redirect('/login')

def update_gym(request):
	if is_authenticated(request):
		gym_count = request.session.get('gym_count')
		if request.POST:
			gym_form = GymForm(request.POST)
			gym_id = request.POST.get("gym_id")
			gym = Gym.objects.filter(pk=gym_id).first()
			if gym_form.is_valid():
				gym.name = gym_form.cleaned_data["name"]
				gym.location = gym_form.cleaned_data["location"]
				gym.summary = gym_form.cleaned_data["summary"]
				gym.featured_photo = gym_form.cleaned_data["featured_photo"]
				gym.user = gym_form.cleaned_data["user"]
				gym.price = gym_form.cleaned_data["price"]
				gym.save()
				return redirect("/gymadmin/gyms")
			else:
				template = loader.get_template('gyms/edit_gym.html')
				context = {'gym':gym,'gym_count':gym_count,'logged_in':True}
				return HttpResponse(template.render(context, request))
	else:
		return redirect('/login')

def gyms(request):
	if is_authenticated(request):
		template = loader.get_template('gyms/home.html')
		user = request.session.get('username')
		user_id = request.session.get('user_id')
		userObj = User.objects.filter(username=user).first()
		gym_count = request.session.get('gym_count')
		gyms = Gym.objects.filter(user_id=user_id)
		context = {'gyms':gyms,'gym_count':gym_count,'user':userObj,'logged_in':True}
		return HttpResponse(template.render(context, request))
	else:
		return redirect('/login')

def gym_details(request,gym_id):
	if is_authenticated(request):
		template = loader.get_template('gyms/details.html')
		gym_count = request.session.get('gym_count')
		user = request.session.get('username')
		userObj = User.objects.filter(username=user).first()
		gym = Gym.objects.filter(pk=gym_id).first()
		if gym.user_id == userObj.id:
			context = {'gym':gym,'gym_count':gym_count,'user':userObj,'logged_in':True}
			return HttpResponse(template.render(context, request))
		else:
			return redirect('/gymadmin/gyms')
	else:
		return redirect('/login')

def gym_delete(request,gym_id):
	if is_authenticated(request):
		#template = loader.get_template('gyms/details.html')
		#gym_count = request.session.get('gym_count')
		user = request.session.get('username')
		userObj = User.objects.filter(username=user).first()
		gym = Gym.objects.filter(pk=gym_id).first()
		if gym.user_id == userObj.id:
			gym.delete()
		return redirect('/gymadmin/gyms')
	else:
		return redirect('/login')

def is_authenticated(request):
	user = request.session.get('username')
	return user