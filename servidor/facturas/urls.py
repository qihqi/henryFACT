from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('facturas.views',
        url(r'resumen$', 'resumen_request_page'),
)
