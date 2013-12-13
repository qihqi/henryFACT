
function getRow() {
    alert("called");
    var codigo = $("<input name=\"codigo\">");
    var cant = $("<input name=\"cant\">");
    var nombre = $("<span name=\"nombre\">");
    
    codigo.keypress(function(event) {
        if (event.which == 13){
            event.preventDefault();
            //ajax load

            cant.focus();
        }
    });

    cant.keypress(function(event) {
        if (event.which == 13) {
            event.preventDefault();
            var a = getRow();
            for (var i = 0; i < 3; i++)
                $(this).parent().append(a[i]);
        }
    });
    
    return new Array(codigo, cant, nombre);
}
