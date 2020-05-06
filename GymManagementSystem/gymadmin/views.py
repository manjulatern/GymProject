from django.shortcuts import render, HttpResponse
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def dashboard(request):
	template = loader.get_template('dashboard.html')
	context = {
			}
	return HttpResponse(template.render(context, request))