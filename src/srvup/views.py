from django.shortcuts import render
from django.utils.safestring import mark_safe
from videos.models import Video

def home(request):
	name = "Justin"
	videos = Video.objects.all()
	embeds = []

	for vid in videos:
		code = mark_safe(vid.embed_code)
		embeds.append("%s" %(code))

	context = {
		"the_name": name,
		"number": videos.count(),
		"videos": videos,
		"the_embeds": embeds,
		"a_code": mark_safe(videos[0].embed_code)
	}
	return render(request, "home.html", context)
	#return render_to_response("home.html", context, context_instance=RequestContext(request))