from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

login_path = '/home/han/Documents/java/server/servidor/main/templates/login.html'

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^createuser$','main.views.createUserPage'),
    url(r'^createuserx$','main.views.createUserPageX'),
    url(r'^login$','main.views.loginPage'),
    url(r'^config$', 'main.views.config_page'),
    url(r'^sequencia$', 'main.views.modificar_sequencia_page'),
    url(r'^migracion$', 'main.views.migration'),
    url(r'^cliente/', include('clientes.urls')),
    url(r'^producto/', include('productos.urls')),
    url(r'^ventas/', include('facturas.urls')),
    url(r'^snapshot/', include('snapshot.urls')),
    url(r'^r/?$', 'main.views.index'),
    url(r'^r/createuser$','main.views.createUserPage'),
    url(r'^r/createuserx$','main.views.createUserPageX'),
    url(r'^r/login$','main.views.loginPage'),
    url(r'^r/config$', 'main.views.config_page'),
    url(r'^r/sequencia$', 'main.views.modificar_sequencia_page'),
    url(r'^r/migracion$', 'main.views.migration'),
    url(r'^r/cliente/', include('clientes.urls')),
    url(r'^r/producto/', include('productos.urls')),
    url(r'^r/ventas/', include('facturas.urls')),
    url(r'^r/snapshot/', include('snapshot.urls')),
    # url(r'^servidor/', include('servidor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
