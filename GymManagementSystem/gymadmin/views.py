from django.shortcuts import render, HttpResponse
from django.template import loader
from django.http import HttpResponse

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

	context = {
			'logged_in': logged_in,
			'username':user,
			'user':userObj,
			'profile_complete': profile_complete
			}
	return HttpResponse(template.render(context, request))

def is_authenticated(request):
	user = request.session.get('username')
	return user