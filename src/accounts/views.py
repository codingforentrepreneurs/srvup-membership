from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.safestring import mark_safe


# Create your views here.


from .forms import LoginForm, RegisterForm
from .models import MyUser

def auth_logout(request):
	logout(request)
	return HttpResponseRedirect('/')



def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		print username, password
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			if next_url is not None:
				return HttpResponseRedirect(next_url)
			return HttpResponseRedirect("/")

	context = {"form": form}
	return render(request, "login.html", context)
	

def auth_register(request):

	form = RegisterForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password2']
		#MyUser.objects.create_user(username=username, email=email, password=password)
		new_user = MyUser()
		new_user.username = username
		new_user.email = email
		#new_user.password = password #WRONG
		new_user.set_password(password) #RIGHT
		new_user.save()

	context = {
		"form": form,
		"action_value": "",
		"submit_btn_value": "Register",
	}

	return render(request,"accounts/register_form.html", context)






