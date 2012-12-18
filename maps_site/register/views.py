# Create your views here.
from register.forms import RegistrationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

def register(request):
	if request.method == 'POST':
		print request.POST
		form = RegistrationForm( request.POST )
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
		else:
			return render(request, 'register/register.html', {'form':form})
		
	form = RegistrationForm()
	return render(request, 'register/register.html', { 'form':form })

	
		
