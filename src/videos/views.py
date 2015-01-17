from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404

# Create your views here.
from .models import Video, Category


@login_required
def video_detail(request, cat_slug, id):
	try:
		cat = Category.objects.get(slug=cat_slug)
	except:
		raise Http404
	try:
		obj = Video.objects.get(id=id)
		return render(request, "videos/video_detail.html", {"obj": obj})
	except:
		raise Http404



def category_list(request):
	queryset = Category.objects.all()
	context = {
		"queryset": queryset,
	}
	return render(request, "videos/category_list.html", context)



@login_required
def category_detail(request, cat_slug):
	try:
		obj = Category.objects.get(slug=cat_slug)
		queryset = obj.video_set.all()
		return render(request, "videos/video_list.html", {"obj": obj, "queryset": queryset})
	except:
		raise Http404



# def video_edit(request):

# 	return render(request, "videos/video_single.html", {})


# def video_create(request):

# 	return render(request, "videos/video_single.html", {})
