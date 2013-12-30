from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^contab$', 'libros.views.index', name='index'),
    url(r'^login/', 'cheque.helper.loginPage'),
    url(r'^cheque/', include('cheque.urls')),
    url(r'^contab/', include('libros.urls')),
    url(r'^contab/$', 'libros.views.index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^c/login/', 'cheque.helper.loginPage'),
    url(r'^c/cheque/', include('cheque.urls')),
    url(r'^c/contab/', include('libros.urls')),
    url(r'^c/contab/$', 'libros.views.index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
