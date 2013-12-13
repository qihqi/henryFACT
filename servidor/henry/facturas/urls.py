from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('facturas.views',
        url(r'resumen$', 'resumen_request_page'),
        url(r'ver_totales$', 'get_totales_form'),
        url(r'ver_resumen_total$', 'ver_resumen_total'),
        url(r'resumen_generado$', 'generar_resumen_page'),
        url(r'eliminar$', 'testPage'),
        url(r'ver_doc$', 'ver_doc_page'),
        url(r'show_doc$', 'show_doc_page'),
)
