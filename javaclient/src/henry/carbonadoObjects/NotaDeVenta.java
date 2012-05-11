package henry.carbonadoObjects;

import com.amazon.carbonado.Storable;
import com.amazon.carbonado.Alias;
import com.amazon.carbonado.PrimaryKey;
import com.amazon.carbonado.Join;
import com.amazon.carbonado.Query;
import com.amazon.carbonado.FetchException;
import com.amazon.carbonado.Automatic;


import henry.carbonadoObjects.Usuario;
import henry.carbonadoObjects.Cliente;
import henry.carbonadoObjects.ItemVenta;

import org.joda.time.DateTime;

@Alias("notas_de_venta")
@PrimaryKey("codigo")
public abstract class NotaDeVenta implements Storable<NotaDeVenta> {

    @Automatic
    @Alias("id")
    public abstract long getCodigo();
    public abstract void setCodigo(long s);

    @Alias("fecha")
    public abstract DateTime getFecha();
    public abstract void setFecha(DateTime s);

    @Alias("vendedor_id")
    public abstract String getVendedorCod();
    public abstract void setVendedorCod(String s);

    @Alias("cliente_id")
    public abstract String getClienteCod();
    public abstract void setClienteCod(String s);

    @Alias("bodega_id")
    public abstract int getBodegaId();
    public abstract void setBodegaId(int s);

    @Join(internal="bodegaId", 
    	  external="id")
    public abstract Bodega getBodega() throws FetchException;
    public abstract void setBodega(Bodega s);
    
    @Join(internal="clienteCod", 
          external="codigo")
    public abstract Cliente getCliente() throws FetchException;
    public abstract void setCliente(Cliente s);

    @Join(internal="vendedorCod", 
          external="username")
    public abstract Usuario getVendedor() throws FetchException;
    public abstract void setVendedor(Usuario s);

    @Join(internal="codigo",
          external="codigoVenta")
    public abstract Query<ItemVenta> getItems() throws FetchException;

    @Alias("precio_modificado")
    public abstract boolean isModificado();
    public abstract void setModificado(boolean x);

}
