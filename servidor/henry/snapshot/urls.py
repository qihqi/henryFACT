from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('snapshot',
        url(r'revision$','views.revisar_inventario'),
        url(r'ver_most_prod$','views.revisar_estado_cant'),
        url(r'ver_most_val$','views.revisar_estado_value'),
        url(r'image_cant/(?P<codigo>.*)/(?P<bodega>[0-9])/(?P<desde>.*)/(?P<hasta>.*)/(?P<row>.*)$', 'imaging.prod_date_sale'),
        url(r'hist/(?P<codigo>.*)/(?P<bodega>[0-9])$', 'views.ver_prod_hist'),
)
