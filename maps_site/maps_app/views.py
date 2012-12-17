# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user
from models import *

@login_required
def index(request):
	usr = get_user(request)	
	addrs  = Address.objects.filter(owner=usr)
	return render(request,'maps_app/index.html', {'users_saved_locations':addrs})
@login_required
def shared(request):
	return render(request,'maps_app/shared.html')
@login_required
def saved(request):
	return render(request,'maps_app/saved.html')
