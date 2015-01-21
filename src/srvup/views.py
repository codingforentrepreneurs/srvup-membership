from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.safestring import mark_safe



from accounts.forms import RegisterForm
from accounts.models import MyUser

from videos.models import Video

from .forms import LoginForm



#@login_required(login_url='/enroll/login/')
#@login_required


def home(request):

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

		#ADD MESSAGE for success.
		return redirect('login')
		#return HttpResponseRedirect(reverse('login'))
		



	# name = "Justin"
	# videos = Video.objects.all()
	# embeds = []

	# for vid in videos:
	# 	code = mark_safe(vid.embed_code)
	# 	embeds.append("%s" %(code))

	context = {
		"form": form,
		"action_value": "",
		"submit_btn_value": "Register",
		# "the_name": name,
		# "number": videos.count(),
		# "videos": videos,
		# "the_embeds": embeds,
		# "a_code": mark_safe(videos[0].embed_code)
	}
	return render(request, "form.html", context)




# def home(request):
# 	if request.user.is_authenticated():
# 		print 
# 		name = "Justin"
# 		videos = Video.objects.all()
# 		embeds = []

# 		for vid in videos:
# 			code = mark_safe(vid.embed_code)
# 			embeds.append("%s" %(code))

# 		context = {
# 			"the_name": name,
# 			"number": videos.count(),
# 			"videos": videos,
# 			"the_embeds": embeds,
# 			"a_code": mark_safe(videos[0].embed_code)
# 		}
# 		return render(request, "home.html", context)
# 	#redirect to login
# 	else:
# 		return HttpResponseRedirect('/login/')



@login_required(login_url='/staff/login/')
def staff_home(request):
	context = {
		
	}
	return render(request, "home.html", context)



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
			return HttpResponseRedirect(next_url)

	context = {"form": form}
	return render(request, "login.html", context)
	
