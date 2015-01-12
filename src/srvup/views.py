from django.shortcuts import render


def home(request):
	name = "Justin"
	context = {
		"the_name": name,
	}
	return render(request, "base.html", context)