from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from push.views import HomeView
from push.views import LogoutView
from push.views import SignupView
from push.views import RegIdSubmitView

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # Examples:
    url(r'^$', login_required(HomeView.as_view()), name='home'),
    url(r'^home$', login_required(HomeView.as_view()), name='home'),
    url(r'^signup$', SignupView.as_view(), name='SignUp'),
    url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^submitregid$', login_required(RegIdSubmitView.as_view()), name='test-regidsubmit'),

    # url(r'^pushit/', include('pushit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
