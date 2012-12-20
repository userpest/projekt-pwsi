# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user
from models import *
from annoying.functions import get_object_or_None
from forms import *


@login_required
def index(request):
	usr = get_user(request)	
	addrs  = Address.objects.filter(owner=usr)
	markers =get_object_or_None(UsersMarkerOptions,user=usr)
#	print markers.showShared
#	print markers.showSaved
	markers_form = MarkersForm(
			initial = { 'showShared': markers.showShared,
				'showSaved':markers.showSaved }
			)
	return render(request,'maps_app/index.html', { 'addrs':addrs,
		'markers':markers})
@login_required
def shared(request):
	return render(request,'maps_app/shared.html')
@login_required
def saved(request):
	return render(request,'maps_app/saved.html')
