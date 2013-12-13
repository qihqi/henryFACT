
function setup() {
    $("input#id_codigo").keypress(function(event) {
        if (event.which == 13){
            event.preventDefault();
            var codigo = $(this).val();
            var bodega = $("#id_bodega").val();
            var data = "codigo=" + escape(codigo)+ "&bodega=" + bodega;
            $.ajax( {
                    url:"/r/producto/get_prod_cont", 
                    data : data,
                    success:function(result){
                        if (result.status) {
                            $("input#id_nombre").val(result.nombre);
                            $("input#id_precio").val(result.precio);
                            $("input#id_precio2").val(result.precio2);
                            $("input#id_cantidad_mayorista").val(result.cant_mayorista);
                        }
                        else {
                            $("input#id_nombre").val("Codigo Equivocado");
                            $(this).select();
                        }
                    }
            });
          }
     });
}
