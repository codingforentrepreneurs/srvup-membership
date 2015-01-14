from django.shortcuts import render

from videos.models import Video

def home(request):
	name = "Justin"
	videos = Video.objects.all()
	embeds = []
	for vid in videos:
		embeds.append("%s" %(vid.embed_code))

	context = {
		"the_name": name,
		"number": videos.count(),
		"videos": videos,
		"the_embeds": embeds,
	}
	return render(request, "home.html", context)
	#return render_to_response("home.html", context, context_instance=RequestContext(request))