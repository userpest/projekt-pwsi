from django.conf.urls import patterns, include, url

urlpatterns = patterns('maps_app.views',

                       url(r'^$',
                           'index',
                           name='maps_index'),
		     )
