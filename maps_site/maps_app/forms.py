from django import forms
from models import SharedInfo,Address
from django.contrib.auth.models import User
from django.forms.fields import Field, FileField
from models import *

checkbox_attrs = { 'class' : 'user_list_checkbox' }

saved_attrs = {'onclick' : 'Dajaxice.maps_app.saved_checked(Dajax.process,{\'change\':1})'  } 
shared_attrs = { 'onclick': 'Dajaxice.maps_app.shared_checked(Dajax.process,{\'change\':1})' } 

class UserList(forms.Form):
	def __init__(self, users,*args, **kwargs):
		super(UserList, self).__init__(*args, **kwargs)
		USERS_CHOICES = [] 
		
		initial = kwargs.pop('initial', {'users':()})	


		for i in users:
			USERS_CHOICES.append((i.id, i.username))

		self.fields[u'users'] = forms.MultipleChoiceField(initial = initial['users'], 
				label = "User list",
				choices = USERS_CHOICES,
				widget = forms.widgets.CheckboxSelectMultiple(attrs=checkbox_attrs))
		#print self.fields

		    
	def clean_users(self):

		for i in self.cleaned_data['users']:
			try:
				User.objects.get(id=int(i))
			except User.DoesNotExist:
				raise forms.ValidationError('such user does not exist'+str(i))

		return self.cleaned_data['users']

	def clean(self):
		print self.cleaned_data
		return self.cleaned_data

	def save(self,entry):
		SharedInfo.objects.filter(addr=entry).delete()
		#print "hi"
		#print self.cleaned_data
		for i in self.cleaned_data['users']:
			usr = User.objects.get(id=int(i))
			SharedInfo.objects.create(addr=entry, shared_user = usr)

			
class MarkersForm(forms.Form):
	showShared = forms.BooleanField(label = "show shared entries markers",
			widget = forms.widgets.CheckboxInput(
					attrs = shared_attrs)
					) 
	showSaved =forms.BooleanField( label = "show saved entries markers", 
			widget = forms.widgets.CheckboxInput(
					attrs = saved_attrs)
			)
