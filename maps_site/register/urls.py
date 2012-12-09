from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template
from register import views

urlpatterns = patterns('',
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^login/$',
                           'django.contrib.auth.views.login',
			   {'template_name': 'register/login.html' },
			   name="login"),
                       url(r'^logout/$',
                           'django.contrib.auth.views.logout',
                           {'template_name': 'register/logout.html'},
                           name='logout'),
                       url(r'^register/$',
                           'register.views.register',
                           name='register'),
                       url(r'^register/complete/$',
                           'django.views.generic.simple.direct_to_template',
                           {'template': 'registration/registration_complete.html'},
                           name='registration_complete'),
                       )
