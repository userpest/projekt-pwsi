from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register 
from django.utils import simplejson
import random
import maps_app
from geopy import geocoders



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

@dajaxice_register
def go_to_location(request,addr):
	dajax = Dajax()
	g = geocoders.Google()
	loc,(lat,lng) = g.geocode(addr)
	points = {'lat':lat,'lng':lng } 
	dajax.add_data(points,'set_location')
	return dajax.json()
