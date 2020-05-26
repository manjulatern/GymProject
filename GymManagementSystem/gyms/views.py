from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.http import HttpResponse

from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from uuid import uuid4

from gyms.models import *

# Create your views here.
def index(request):
	template = loader.get_template('index.html')
	logged_in = False
	user = ''
	userObj = ""
	profile_complete = 0
	
	page = request.GET.get('page', 1)
	gyms = Gym.objects.all()
	paginator = Paginator(gyms, 5)
	
	try:
		gyms = paginator.page(page)
	except PageNotAnInteger:
		gyms = paginator.page(1)
	except EmptyPage:
		gyms = paginator.page(paginator.num_pages)

	if is_authenticated(request):
		user = request.session.get('username')
		profile_complete = request.session.get('profile_complete')
		logged_in = True
		userObj = User.objects.filter(username=user).first()
		

	context = {
			'logged_in': logged_in,
			'username':user,
			'user':userObj,
			'profile_complete': profile_complete,
			'post_title': "This is a new Post",
			'author': 'ManjulB',
			'post_content': 'This is the content of a post',
			'item_list': ['D1','D2','D3','D4'],
			'comments': '',
			'gyms':gyms
			}
	return HttpResponse(template.render(context, request))

def login(request):
	context = {}
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = User.objects.filter(username=username,password=password,status='Active').first()
		if user:
			request.session['username'] = username
			request.session['profile_complete'] = user.profile_complete
			request.session['user_id'] = user.pk
			if user.profile_complete == 0:
				return redirect('/profile')
			else:
				return redirect('/')

		else:
			template = loader.get_template('login.html')
			context = {
				'logged_in': False,
				'message': "Please enter valid credentials or have you activated your account?"
			}

		return HttpResponse(template.render(context, request))

	template = loader.get_template('login.html')
	return HttpResponse(template.render(context, request))

def register(request):
	if request.method == 'GET':
		template = loader.get_template('register.html')
		context = {
			}
	elif request.method == 'POST':
		
		full_name = request.POST.get('full_name')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password = request.POST.get('password')

		rand_token = uuid4().hex

		user = User()
		user.full_name = full_name
		user.email = email
		if User.objects.filter(email=user.email):
			return render(request, 'register.html', {'error': "email already used"})
		user.username = username
		if User.objects.filter(username=user.username):
			return render(request, 'register.html', {'error': "username already taken"})
		user.password = password
		user.status = "Inactive"
		user.token = rand_token
		user.save()
		
		subject = 'Gymaholic: Activate your Account'
		body = 'Please click on the below link to activate your account'
		sender_email = 'covid19.ncit@gmail.com'
		recipients = email.strip().split(" ")


		try:
			email_context = {'full_name': full_name,'token':rand_token, 'email':email,'host':request.get_host()}
			send_html_email(recipients, subject, 'email.html', email_context)
			#send_mail(subject, body, sender_email, recipients)
		except Exception as e:
			print("Email could not be sent. %s", e)
		
		context = {
			"message": "Success",
			"full_name": full_name,
			"email": email
			}
		template = loader.get_template('register.html')
	
		
	return HttpResponse(template.render(context, request))

def activate(request):
	token = request.GET.get('token')
	email = request.GET.get('email')
	user = User.objects.filter(email=email,token=token).first()
	if user:
		user.status = "Active"
		user.save()
		context = {
			"message": "Success",
			"activate": True
			}
		template = loader.get_template('register.html')
	else:
		context = {
			"message": "Failure",
			"activate": False
			}
		template = loader.get_template('register.html')
	return HttpResponse(template.render(context, request))

def profile(request):
	context = {}
	template = loader.get_template('profile.html')
	message = ""
	if is_authenticated(request):
		username = request.session['username']
		user = User.objects.filter(username=username).first()
		if request.method == 'POST':
			phone_number = request.POST.get('phone_number').strip()
			user_type = int(request.POST.get('user_type'))
			address = request.POST.get('address').strip()
			pan_vat_number = request.POST.get('pan_vat_number').strip()
			if user_type == 0:
				pan_vat_number = ""
			profile_complete = 0

			if user_type == 0:
				if phone_number and address:
					profile_complete = 1

			if user_type == 1:
				if phone_number and address and pan_vat_number:
					profile_complete = 1
			
			user.phone_number = phone_number
			user.user_type = user_type
			user.profile_complete = profile_complete

			user.pan_vat_number = pan_vat_number
			user.address = address
			user.save()
			request.session['profile_complete'] = user.profile_complete
			message = "Your Profile has been updated"
			context = {'logged_in': True,'user':user, 'username':username,'profile_complete':profile_complete,'message':message}
		else:
			context = {'logged_in': True,'user':user,'username':username,'profile_complete': user.profile_complete, 'message':message}
		return HttpResponse(template.render(context, request))

	else:
		return redirect('/login')

def profile_image(request):
	if is_authenticated(request):
		context = {}
		username = request.session.get('username')
		user = User.objects.filter(username=username).first()
		if request.method == 'POST' and request.FILES['image']:
			myfile = request.FILES['image']
			fs = FileSystemStorage()
			filename = fs.save(myfile.name, myfile)
			user.image = filename
			user.save()
		return redirect('/profile')
	else:
		return redirect('/login')

def logout(request):
	context = {}
	del request.session['username']
	
	return redirect('/')

def send_html_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
	msg_html = render_to_string(template_name, context)
	msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, bcc=to_list)
	msg.content_subtype = "html"  # Main content is now text/html
	return msg.send()

def email(request):
	context = {'full_name': "Manjul Bhattarai",'token':"1234", 'email':"07.manutdilam@gmail.com",'host':request.get_host()}
	template = loader.get_template('email.html')
	return HttpResponse(template.render(context, request))

def is_authenticated(request):
	user = request.session.get('username')
	return user
