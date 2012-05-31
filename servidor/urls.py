from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

login_path = '/home/han/Documents/java/server/servidor/main/templates/login.html'

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^createuser$','main.views.createUserPage'),
    url(r'^login$','main.views.loginPage'),
    url(r'^config$', 'main.views.config_page'),
    url(r'^sequencia$', 'main.views.modificar_sequencia_page'),
    url(r'^cliente/', include('clientes.urls')),
    url(r'^producto/', include('productos.urls')),
    url(r'^ventas/', include('facturas.urls')),
    # url(r'^servidor/', include('servidor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
