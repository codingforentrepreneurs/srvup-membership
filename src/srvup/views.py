from django.shortcuts import render


def home(request):
	name = "Justin"
	context = {
		"the_name": name,
		"number": 12,
	}
	return render(request, "home.html", context)
	#return render_to_response("home.html", context, context_instance=RequestContext(request))