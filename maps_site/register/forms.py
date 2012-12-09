from django import forms
from django.contrib.auth.models import User

attrs_required = {'class' : 'required'}
attrs_optional = { 'class' : 'optional' }

class RegistrationForm(forms.Form):
	username = forms.RegexField(regex=r'^\w+$', 
			max_length=30, 
			widget = forms.TextInput(attrs=attrs_required),
			)
	email = forms.EmailField(widget = forms.TextInput(attrs=attrs_required))

	password = forms.CharField(max_length=30,
			widget=forms.PasswordInput(attrs=attrs_required))

	first_name = forms.CharField(max_length=30, 
		widget = forms.TextInput(attrs=attrs_optional),
		required = False
		)

	last_name = forms.CharField(max_length=30, 
		widget=forms.TextInput(attrs=attrs_optional),
		required=False)

	def clean_username(self):
		try:
			user = User.objects.get(username=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError('This username is taken')
	def clean_email(self):
		#usually emails are not case sensitive
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
				raise forms.ValidationError('This email is already in sue')
		return self.cleaned_data['email']

	def save(self):
		user = User.objects.create_user(username = self.cleaned_data['username'],
						email = self.cleaned_data['email'],
						password = self.cleaned_data['password'])
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()
		return user

