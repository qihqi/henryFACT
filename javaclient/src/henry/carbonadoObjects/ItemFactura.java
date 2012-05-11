package henry.carbonadoObjects;

import java.math.BigDecimal;

import com.amazon.carbonado.AlternateKeys;
import com.amazon.carbonado.Automatic;
import com.amazon.carbonado.Storable;
import com.amazon.carbonado.Alias;
import com.amazon.carbonado.PrimaryKey;
import com.amazon.carbonado.Join;
import com.amazon.carbonado.FetchException;
import com.amazon.carbonado.Key;

import henry.carbonadoObjects.Factura;
import henry.carbonadoObjects.Producto;

@Alias("items_de_despacho")
@PrimaryKey("id")
@AlternateKeys(@Key({"codigoFactura", "itemNo"}))
public abstract class ItemFactura implements Storable<ItemFactura> {

	@Automatic
	public abstract int getId();
    public abstract void setId(int s);

    @Alias("desp_cod_id")
    public abstract long getCodigoFactura();
    public abstract void setCodigoFactura(long s);

    @Join(internal="codigoFactura",
          external="codigo")
    public abstract Factura getFactura() throws FetchException;
    public abstract void setFactura(Factura s);
   
    
    @Alias("producto_id")
    public abstract String getCodigoProd();
    public abstract void setCodigoProd(String s);

    @Alias("num")
    public abstract int getItemNo();
    public abstract void setItemNo(int s);

    @Join(internal="codigoProd", 
          external="codigo")
    public abstract Producto getProducto() throws FetchException;
    public abstract void setProducto(Producto s);

    public abstract int getCantidad();
    public abstract void setCantidad(int s);

    public abstract BigDecimal getPrecio();
    public abstract void setPrecio(BigDecimal s);
    
    @Alias("precio_modificado")
    public abstract boolean isModificado();
    public abstract void setModificado(boolean b);
}
