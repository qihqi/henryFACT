
var count=0;
function getRow() {
    var p = $("<tr>");
    var codigo_cell = $("<td>");
    var cant_cell = $("<td>");
    var nombre_cell = $("<td>");

    var codigo = $("<input id=\"here"+ count + "\" name=\"codigo\" class=\"text_field\">");
    var cant = $("<input id=\"here"+ count + "\" name=\"cant\" class=\"text_field\">");
    var nombre = $("<span id=\"here"+ count + "\" name=\"nombre\" class=\"text_field\">");
    
    codigo_cell.append(codigo);
    cant_cell.append(cant);
    nombre_cell.append(nombre);
    p.append(codigo_cell, cant_cell, nombre_cell);

    codigo.keypress(function(event) {
        if (event.which == 13){
            event.preventDefault();
            var id = $(this).attr("id");
            var codigo = $(this).val();
            $.ajax( {
                    url:"/producto/get_nombre", 
                    data : "codigo="+codigo,
                    success:function(result){
                        if (result.status) {
                            $("span#"+id).html(result.nombre);
                            cant.focus();
                        }
                        else {
                            $("span#"+id).html("Codigo Equivocado");
                            $(this).select();
                        }
                    }
            });
        }
    });

    cant.keypress(function(event) {
        if (event.which == 13) {
            event.preventDefault();

            var a = getRow();
            $("#insert").append(a);
            a.beginning.focus();

        }
    });
    count++;
    p.beginning = codigo;
    return p;
}
