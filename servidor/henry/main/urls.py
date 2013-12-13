from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('clientes.views',
        url(r'create$', 'create_client_page'),
        url(r'search$', 'search_client_page'),
        url(r'display$', 'display_client_page'),
)
