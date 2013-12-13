from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('cheque.views',
        url(r'create_cheque$', 'create_cheque'),
        url(r'create_banco$', 'create_banco'),
        url(r'ver_cheque$', 'ver_cheque'),
        url(r'ver_cheque_ingresado$', 'ver_cheques_ingresados'),
        url(r'ver_cheque_deposito$', 'ver_cheques_deposito'),
        url(r'ver_cheque_dep$', 'ver_cheque_depositados'),
        url(r'ver_cheque_dep_form$', 'ver_cheque_dep_form'),
        url(r'eliminar$', 'ver_cheques_deposito'),
        url(r'editar/(?P<id>\d+)$', 'editar_cheque'),
        url(r'eliminar/(?P<id>\d+)$', 'eliminar_cheque'),
        url(r'depositar$', 'depositar'),
        url(r'buscar$', 'buscar_cheque_form'),
        url(r'result$', 'buscar_cheque'),
        url(r'$', 'index')
)
