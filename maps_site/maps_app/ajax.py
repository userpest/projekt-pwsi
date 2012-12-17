from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register 
from django.utils import simplejson
import random
from geopy import geocoders
from django.contrib.auth import get_user
from models import *
from django.template.loader import render_to_string


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
def save_location(request,addr,container):
	dajax = Dajax()
	usr = get_user(request)
	loc, (lat,lng) = get_coords(addr)	
	location = Address(owner =usr,
			lat = lat ,
			lng = lng,
			addr = addr)
	location.save()
	location_entry = render_to_string('maps_app/saved_location_node.html',{'addr': location })
	dajax.append('#'+str(container),'innerHTML',location_entry) 
	return dajax.json()

@dajaxice_register
def show_saved_entry(request, e_id):
	dajax = Dajax()
	usr = get_user(request)
	try:
			addr =  Address.objects.get(id=e_id, owner=usr)
			points = { 'lat' : addr.lat, 'lng':addr.lng}
			dajax.add_data(points,'set_location')

	except Address.DoesNotExist:
		return dajax.json()

	return dajax.json()

@dajaxice_register
def remove_saved_entry(request,e_id):
	dajax = Dajax()
	usr = get_user(request)
	try:
			addr =  Address.objects.get(id=e_id, owner=usr)
			dajax.remove('#saved_entry_'+str(addr.id))			
			addr.delete()

	except Address.DoesNotExist:
		return dajax.json()

	return dajax.json()


