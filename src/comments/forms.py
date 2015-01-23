from django import forms

from .models import Comment


# class CommentForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ('user', 'path', 'text')

class CommentForm(forms.Form):
	comment = forms.CharField(widget=forms.Textarea)