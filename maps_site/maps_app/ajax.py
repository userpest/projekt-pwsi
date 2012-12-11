from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register 
from django.utils import simplejson
import random

@dajaxice_register
def msg(request):
    return simplejson.dumps({'message':'Hello from Python!'})

@dajaxice_register
def randomize(request):
	dajax = Dajax()
	dajax.assign('#result', 'value', random.randint(1, 10))
	dajax.alert('hhmf')
	return dajax.json()


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


