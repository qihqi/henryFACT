
var count=0;
function getRow() {
    var p = $("<p>");
    var codigo = $("<input name=\"codigo\">");
    var cant = $("<input name=\"cant\">");
    var nombre = $("<span id=\"here\"" + count + " name=\"nombre\">");
    p.append(codigo, cant, nombre);

    codigo.keypress(function(event) {
        if (event.which == 13){
            event.preventDefault();
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
    count++; 
    return p;
}
