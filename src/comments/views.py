
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect

# Create your views here.

from videos.models import Video

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
		parent_id = request.POST.get('parent_id')
		video_id = request.POST.get("video_id")
		origin_path = request.POST.get("origin_path")
		try:
			video = Video.objects.get(id=video_id)
		except:
			video = None

		print video
		parent_comment = None
		if parent_id is not None:
			try:
				parent_comment = Comment.objects.get(id=parent_id)
			except:
				parent_comment = None

			if parent_comment is not None and parent_comment.video is not None:
				video = parent_comment.video

		form = CommentForm(request.POST)
		if form.is_valid():
			comment_text = form.cleaned_data['comment']
			if parent_comment is not None:
				# parent comments exists
				new_comment = Comment.objects.create_comment(
					user=request.user, 
					path=parent_comment.get_origin, 
					text=comment_text,
					video = video,
					parent=parent_comment
					)
				messages.error(request, "Thank you for your response. <a href='/somellink/'>Linked Item</a>", extra_tags='safe')
				return HttpResponseRedirect(parent_comment.get_absolute_url())
			else:
				new_comment = Comment.objects.create_comment(
					user=request.user, 
					path=origin_path, 
					text=comment_text,
					video = video
					)
				messages.success(request, "Thank you for the comment.")
				return HttpResponseRedirect(new_comment.get_absolute_url())
		else:
			print origin_path
			messages.error(request, "There was an error with your comment.")
			return HttpResponseRedirect(origin_path)

	else:
		raise Http404
