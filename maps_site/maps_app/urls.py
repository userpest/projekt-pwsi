from django.conf.urls import patterns, include, url

urlpatterns = patterns('maps_app.views',

                       url(r'^saved/$',
                           'saved',
			   name="maps_saved"),
                       url(r'^shared/$',
                           'shared',
                           name='maps_shared'),
                       url(r'^index/$',
                           'index',
                           name='maps_index'),
		     )
