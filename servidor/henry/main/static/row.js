function is_number(b) {
    return b!=undefined && b!=null && (b - 0) == b;
}

function popup(){
    
	var newwindow=window.open("/static/buscar_producto.html",'name','height=700,width=500, scrollbars=yes');
    window.codigo_click = $(this).attr("id");
    if (window.focus) 
        newwindow.focus();
	return false;
}



var count=0;
function getRow() {
    var p = $("<tr>");
    var codigo_cell = $("<td>");
    var cant_cell = $("<td>");
    var nombre_cell = $("<td>");
    var buscar_cell = $("<td>");
    var trans_cell = $("<td>");
    var codigo = $("<input id=\"here"+ count + "\" name=\"codigo\" class=\"text_field\">");
    var cant = $("<input id=\"here"+ count + "\" name=\"cant\" class=\"text_field\">");
    var nombre = $("<span id=\"here"+ count + "\" name=\"nombre\" class=\"text_field\">");
    var buscar = $("<a id=\"here"+ count + "\" name=\"nombre\" href=\"\" class=\"text_field\" >");
   // var trans = $("<input id=\"here"+ count + "\" name=\"transform\" class=\"text_field\" type=\"checkbox\">");
    buscar.click(popup);
    buscar.html("buscar"); 
    codigo_cell.append(codigo);
    cant_cell.append(cant);
    nombre_cell.append(nombre);
    buscar_cell.append(buscar);
    //trans_cell.append(trans);
    p.append(buscar_cell, codigo_cell, cant_cell, nombre_cell);

    codigo.keypress(function(event) {
        if (event.which == 13){
            event.preventDefault();
            var id = $(this).attr("id");
            var codigo = $(this).val();
            var bodega = $("#id_bodega").val();
            var data = "codigo=" + codigo + "&bodega=" + bodega;
            $.ajax( {
                    url:"/r/producto/get_prod_cont", 
                    data : data,
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
            
            var number = $(this).val();
            if (! is_number(number))
            { 
                alert("cantidad debe ser numero");
                return;
            }

            var a = getRow();
            $("#insert").append(a);
            a.beginning.focus();

        }
    });
    count++;
    p.beginning = codigo;
    return p;
}
