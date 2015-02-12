from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.safestring import mark_safe



from accounts.forms import RegisterForm, LoginForm
from accounts.models import MyUser

from analytics.models import PageView
from analytics.signals import page_view
from comments.models import Comment
from videos.models import Video, Category




#@login_required(login_url='/enroll/login/')
#@login_required









def home(request):

	page_view.send(
		request.user,
		page_path=request.get_full_path()
		)
	if request.user.is_authenticated():
		page_view_objs = request.user.pageview_set.get_videos()[:6]

		recent_videos = []
		for obj in page_view_objs:
			if not obj.primary_object in recent_videos:
				#print obj.primary_object
				recent_videos.append(obj.primary_object)
		recent_comments = Comment.objects.recent()

		#top items
		video_type = ContentType.objects.get_for_model(Video)
		popular_videos_list = PageView.objects.filter(primary_content_type=video_type)\
		 .values("primary_object_id")\
		 .annotate(the_count=Count("primary_object_id"))\
		 .order_by("-the_count")[:4]
		popular_videos = []
		for item in popular_videos_list:
			try:
				new_video = Video.objects.get(id=item['primary_object_id'])
				popular_videos.append(new_video)
			except:
				pass

		random_videos = Video.objects.all().order_by('?')[:6]
		#print popular_videos
		# one item
		#PageView.objects.filter(primary_content_type=video_type, primary_object_id=21).count()


		context = {
			"random_videos": random_videos,
			"recent_videos": recent_videos,
			"recent_comments": recent_comments,
			"popular_videos": popular_videos,
			}
		template = "accounts/home_logged_in.html"
		#return HttpResponseRedirect('/dashboard/')
	else:
		featured_categories = Category.objects.get_featured()
		featured_videos = Video.objects.get_featured()
		login_form = LoginForm()
		register_form = RegisterForm()
		template = "accounts/home_visitor.html"
		context = {
			"register_form": register_form, 
			"login_form": login_form, 
			"featured_videos":featured_videos,
			"featured_categories": featured_categories,
		}
	
	return render(request,template,context)




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



