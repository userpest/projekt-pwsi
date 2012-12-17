from django import forms
from models import SharedInfo,Address
from django.contrib.auth.models import User

checkbox_attrs = { 'class' : 'user_list_checkbox' }

class UserList(forms.Form):
	def __init__(self, e_id,users,*args, **kwargs):
		super(UserList, self).__init__(*args, **kwargs)
		self.e_id = e_id
		USERS_CHOICES = [] 
		for i in users:
			USERS_CHOICES.append((i.id, i.username))

		self.fields['users'] = forms.MultipleChoiceField(label = "User list",
				choices = USERS_CHOICES,
				widget = forms.widgets.CheckboxSelectMultiple(attrs=checkbox_attrs))

	def clean_e_id(self):
		print "clean eid called"

		try:
			Address.objects.get(id=self.cleaned_data['e_id'])
		except User.DoesNotExist:
			raise forms.ValidationError('such user does not exist'+str(i))

	def clean_users(self):
		for i in self.cleaned_data['users']:
			try:
				User.objects.get(id=int(i))
			except User.DoesNotExist:
				raise forms.ValidationError('such user does not exist'+str(i))

	def save(self):
		entry = Address.objects.get(id=self.e_id)
		SharedInfo.objects.filter(addr=entry).delete()

		for i in self.cleaned_data['users']:
			usr = User.objects.get(id=int(i))
			SharedInfo.objects.create(addr=entry, shared_user = usr)

			

