from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(label="Username")
	password = forms.CharField(widget=forms.PasswordInput())