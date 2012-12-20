from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register 
from django.utils import simplejson
import random
from geopy import geocoders
from django.contrib.auth import get_user
from models import *
from django.template.loader import render_to_string
from dajaxice.utils import deserialize_form
from django.contrib.auth.models import User
from forms import UserList , MarkersForm
from django.db.models import Q


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

	markers =UsersMarkerOptions.objects.get(user=usr)
	print markers.window
	if markers.window != 0:
		return dajax.json()


	location_entry = render_to_string('maps_app/saved_location_node.html',{'addr': location })

	options = UsersMarkerOptions.objects.get(user=usr)

	if options.showSaved==True:
		mtitle = str(location.addr)
		marker_id = "saved_entry_"+str(location.id)
		points = {'lat':location.lat,'lng':location.lng,'mtitle':mtitle, 'marker_id' : marker_id } 
		dajax.add_data(points,'add_marker')

			

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
		SharedInfo.objects.filter(addr=addr).delete()


		options = UsersMarkerOptions.objects.get(user=usr)

		if options.showSaved==True:
			marker_id = "saved_entry_"+str(addr.id)
			points = {'marker_id' : marker_id } 
			dajax.add_data(points, 'remove_marker')
		addr.delete()

	except Address.DoesNotExist:
		return dajax.json()

	return dajax.json()

@dajaxice_register
def share_saved_entry(request,container,e_id):
	dajax = Dajax()
	usr = get_user(request)
	usrs = User.objects.filter(~Q(id=usr.id))

	try:
		entry = Address.objects.get(owner=usr, id=e_id)
		dajax.clear('#'+str(container), 'innerHTML')

		shared = SharedInfo.objects.filter(addr=entry)
		init= [] 

		for i in shared:
			init.append(i.shared_user.id)

		print init

		form = UserList(users = usrs, initial={'users': init})
		html = render_to_string( 'maps_app/share_saved_entry.html', 
				{'e_id':e_id,'form':form})
		dajax.append('#'+str(container),'innerHTML',html) 


	except Address.DoesNotExist:
		print "exception"

	return dajax.json()

@dajaxice_register
def save_share_options(request, container,e_id,input_form):
	dajax = Dajax()
	usr = get_user(request)

	try:
		#we are also validating the request permissions so i think
		#this logic should be out of the form

		entry = Address.objects.get(owner=usr, id=e_id)
		usrs = User.objects.filter(~Q(id=usr.id))
		form = UserList(usrs,deserialize_form(input_form))
		if form.is_valid():
			form.save(entry)	

	except Address.DoesNotExist:
		pass

	dajax.clear('#'+str(container), 'innerHTML')
	addrs = Address.objects.filter(owner=usr)
	html = render_to_string('maps_app/saved_locations.html',{'addrs': addrs})
	dajax.append('#'+str(container), 'innerHTML', html)
	return dajax.json()


def saved_loc_show(request,container):
	dajax = Dajax()
	usr = get_user(request)
	dajax.clear('#'+str(container), 'innerHTML')
	addrs = Address.objects.filter(owner=usr)
	html = render_to_string('maps_app/saved_locations.html',{'addrs': addrs})
	dajax.append('#'+str(container), 'innerHTML', html)
	return dajax.json()

@dajaxice_register
def show_saved_locations(request,container):
	return saved_loc_show(request,container)

def shared_loc_show(request,container):
	dajax=Dajax()
	dajax.clear('#'+str(container), 'innerHTML')

	usr = get_user(request)
	shared = SharedInfo.objects.filter(shared_user = usr)

	addrs = [] 

	for i in shared:
		addrs.append(i.addr)

	html = render_to_string('maps_app/shared_locations.html', {'addrs' : addrs } )
	dajax.append('#'+str(container), 'innerHTML', html)
	return dajax.json()


@dajaxice_register
def show_shared_locations(request,container):
	return shared_loc_show(request,container)	

@dajaxice_register
def show_shared_location(request,e_id):
	dajax=Dajax()
	usr = get_user(request)

	try:
		addr = Address.objects.get(id=e_id)
		shared = SharedInfo.objects.get(addr=addr, shared_user=usr)
		points = { 'lat' : addr.lat, 'lng':addr.lng}
		dajax.add_data(points,'set_location')

	except SharedInfo.DoesNotExist:
		pass
	except Address.DoesNotExist:
		pass

	return dajax.json()

@dajaxice_register
def delete_shared_location(request,e_id):
	dajax=Dajax()
	usr = get_user(request)

	try:
		addr = Address.objects.get(id=e_id)

		shared = SharedInfo.objects.get(addr=addr, shared_user=usr).delete()
		dajax.remove('#shared_entry_'+str(addr.id))			
		options = UsersMarkerOptions.objects.get(user=usr)

		if options.showShared==True:
			marker_id = "shared_entry_"+str(addr.id)
			print marker_id
			points = {'marker_id' : marker_id } 
			dajax.add_data(points, 'remove_marker')

	except SharedInfo.DoesNotExist:
		pass
	except Address.DoesNotExist:
		pass
	return dajax.json()


def show_marker_options(request,container):
	dajax=Dajax()
	dajax.clear('#'+str(container), 'innerHTML')
	
	usr = get_user(request)
	markers =UsersMarkerOptions.objects.get(user=usr)
	markers_form = MarkersForm(
			initial = { 'showShared': markers.showShared,
				'showSaved':markers.showSaved }
			)

	html = render_to_string('maps_app/options.html', {'markers_form' : markers_form } )
	dajax.append('#'+str(container), 'innerHTML', html)
	return dajax.json()


@dajaxice_register
def choose_showed_locations(request, option, container):
	usr = get_user(request)
	markers =UsersMarkerOptions.objects.get(user=usr)

	if int(option) == 0:
		markers.window=0 
		ret =  saved_loc_show(request,container)
	elif int(option) == 1: 
		markers.window=1
		ret = shared_loc_show(request, container)
	elif int(option) == 2:
		markers.window=2
		ret = show_marker_options(request,container)

	markers.save()
	print markers.window
	return ret

@dajaxice_register
def saved_checked(request,change):
	dajax = Dajax()
	usr = get_user(request)
	addrs = Address.objects.filter(owner=usr)
	options = UsersMarkerOptions.objects.get(user=usr)

	if options.showSaved==False:
		print "showing"	
		for i in addrs:
			mtitle = str(i.addr)
			marker_id = "saved_entry_"+str(i.id)
			points = {'lat':i.lat,'lng':i.lng,'mtitle':mtitle, 'marker_id' : marker_id } 
			dajax.add_data(points,'add_marker')

	else:
		print "hiding"
		for i in addrs:
			marker_id = "saved_entry_"+str(i.id)
			print marker_id
			points = {'marker_id' : marker_id } 
			dajax.add_data(points, 'remove_marker')


	if int(change)==1:
		options.showSaved = not options.showSaved
		options.save()
	return dajax.json()

@dajaxice_register
def shared_checked(request,change):
	dajax = Dajax()
	usr = get_user(request)
	shared = SharedInfo.objects.filter(shared_user=usr)
	options = UsersMarkerOptions.objects.get(user=usr)
	shrd =  shared.values_list('addr',flat=True)

	addrs = Address.objects.filter(id__in=shrd)
	for i in addrs:
		print str(i.id)

	if options.showShared==False:
		print "showing"	
		for i in addrs:
			mtitle = str(i.addr)
			marker_id = "shared_entry_"+str(i.id)
			points = {'lat':i.lat,'lng':i.lng,'mtitle':mtitle, 'marker_id' : marker_id } 
			dajax.add_data(points,'add_marker')

	else:
		print "hiding"
		for i in addrs:
			marker_id = "shared_entry_"+str(i.id)
			print marker_id
			points = {'marker_id' : marker_id } 
			dajax.add_data(points, 'remove_marker')


	if int(change)==1:
		options.showShared = not options.showShared
		options.save()
	return dajax.json()


