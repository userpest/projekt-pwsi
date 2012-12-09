# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse

def register(request):
	return render_to_response('maps_app/register.html')

