from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect

# Create your views here.
from .models import Comment
from .forms import CommentForm


@login_required
def comment_thread(request, id):
	comment = Comment.objects.get(id=id)
	form = CommentForm()
	context = {
	"form": form,
	"comment": comment,
	}
	return render(request, "comments/comment_thread.html", context)



def comment_create_view(request):
	if request.method == "POST" and request.user.is_authenticated():
		form = CommentForm(request.POST)
		if form.is_valid():
			parent_id = request.POST.get('parent_id')
			parent_comment = None
			if parent_id is not None:
				try:
					parent_comment = Comment.objects.get(id=parent_id)
				except:
					parent_comment = None

			comment_text = form.cleaned_data['comment']
			video = None
			

			if parent_comment is not None:
				if parent_comment.video is not None:
					video = parent_comment.video
				new_comment = Comment.objects.create_comment(
					user=request.user, 
					path=parent_comment.get_origin, 
					text=comment_text,
					video = video,
					parent=parent_comment
					)
				return HttpResponseRedirect(parent_comment.get_absolute_url())
			# else:
			# 	new_comment = Comment.objects.create_comment(
			# 		user=request.user, 
			# 		path=parent_comment.get_origin, 
			# 		text=comment_text,
			# 		video = obj,
			# 		parent=parent_comment
			# 		)
			#comment origin
	else:
		raise Http404
