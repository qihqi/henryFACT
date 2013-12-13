from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('libros.views',
        url(r'create_record$', 'create_record_page'),
        url(r'create_cuenta$', 'create_cuenta_page'),
        url(r'ver_cuenta$', 'ver_cuenta'),
        url(r'ver_diario_form$', 'ver_libro_diario_form_page'),
        url(r'ver_diario/(?P<impresion>\d)$', 'ver_libro_diario_page'),
        url(r'ver_mayor_form$', 'ver_libro_mayor_form'),
        url(r'ver_mayor$', 'ver_libro_mayor_page'),
        url(r'editar_cuenta$', 'editar_cuenta'),
        url(r'editar/(?P<id>\d+)$', 'editar_record_page'),
        url(r'eliminar/(?P<id>\d+)$', 'eliminar_record_page'),
)
