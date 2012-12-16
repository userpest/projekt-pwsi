from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register 
from django.utils import simplejson
import random
from geopy import geocoders
from django.contrib.auth import get_user
from models import *


#@dajaxice_register
#def save_coords(request):
#	dajax = Dajax()
#	dajax.alert('it works')
#	return dajax.json()

@dajaxice_register
def save_coords(request,lat,lng,zoom):
	dajax = Dajax()
	msg = "%s %s %s" % (lat,lng,zoom)
	dajax.alert(msg)
	return dajax.json()

def get_coords(addr):
	g = geocoders.Google()
	return g.geocode(addr)

@dajaxice_register
def go_to_location(request,addr):
	dajax = Dajax()
	loc,(lat,lng) = get_coords(addr)
	points = {'lat':lat,'lng':lng } 
	dajax.add_data(points,'set_location')
	return dajax.json()

@dajaxice_register
def save_location(request,addr):
	dajax = Dajax()
	usr = get_user(request)
	loc, (lat,lng) = get_coords(addr)	
	location = Address(owner =usr,
			lat = lat ,
			lng = lng)
	location.save()
	return dajax.json()
