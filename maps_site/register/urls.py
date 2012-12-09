from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
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
