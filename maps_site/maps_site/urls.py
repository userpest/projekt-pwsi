from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'maps_site.views.home', name='home'),
    # url(r'^maps_site/', include('maps_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^$', include('maps_app.urls')),
     url(r'^accounts/', include('register.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
     url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True})
)
urlpatterns += staticfiles_urlpatterns()
