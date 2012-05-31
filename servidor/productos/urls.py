from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('productos.views',
        url(r'create$', 'create_product_page'),
        url(r'get_nombre$','get_producto'),
        url(r'ingreso$','ingreso_producto_page'),
        url(r'createbodega$','create_bodega_page'),
        url(r'ver$','ver_producto_page'),
)
