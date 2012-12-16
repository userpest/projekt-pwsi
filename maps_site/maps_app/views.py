# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
@login_required
def index(request):
	return render(request,'maps_app/index.html')
@login_required
def shared(request):
	return render(request,'maps_app/shared.html')
@login_required
def saved(request):
	return render(request,'maps_app/saved.html')
