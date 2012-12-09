# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request,'maps_app/index.html')
def shared(request):
	return render(request,'maps_app/shared.html')
def saved(request):
	return render(request,'maps_app/saved.html')
