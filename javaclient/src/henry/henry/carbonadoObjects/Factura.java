package henry.carbonadoObjects;

import java.math.BigDecimal;
import com.amazon.carbonado.Storable;
import com.amazon.carbonado.Alias;
import com.amazon.carbonado.PrimaryKey;
import com.amazon.carbonado.Join;
import com.amazon.carbonado.Query;
import com.amazon.carbonado.FetchException;


import henry.carbonadoObjects.Usuario;
import henry.carbonadoObjects.Cliente;
import henry.carbonadoObjects.ItemFactura;

import org.joda.time.DateTime;

@Alias("ordenes_de_despacho")
@PrimaryKey("codigo")
public abstract class Factura implements Storable<Factura> {
	
	/*formas de pagos*/
	public static final String EFECTIVO = "E";
	public static final String TARGETA_CREDITO = "T";
	public static final String CHEQUE = "C";
	public static final String DEPOSITO = "D";
	//END forma de pago
	
    public abstract BigDecimal getTotal();
    public abstract void setTotal(BigDecimal x);
	
    public abstract long getCodigo();
    public abstract void setCodigo(long s);

    @Alias("fecha")
    public abstract DateTime getFecha();
    public abstract void setFecha(DateTime s);

    @Alias("cliente_id")
    public abstract String getClienteCod();
    public abstract void setClienteCod(String s);

    @Alias("vendedor_id")
    public abstract String getVendedorCod();
    public abstract void setVendedorCod(String s);

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
          external="codigoFactura")
    public abstract Query<ItemFactura> getItems() throws FetchException;
   

    //hay q cambiar a enum
    @Alias("pago")
    public abstract String getFormaPago();
    public abstract void setFormaPago(String s);
    
    @Alias("precio_modificado")
    public abstract boolean isModificado();
    public abstract void setModificado(boolean x);
    
    
    public abstract boolean isEliminado();
    public abstract void setEliminado(boolean x);

}
