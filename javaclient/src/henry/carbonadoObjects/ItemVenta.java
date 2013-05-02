package henry.carbonadoObjects;

import java.math.BigDecimal;

import com.amazon.carbonado.AlternateKeys;
import com.amazon.carbonado.Automatic;
import com.amazon.carbonado.Key;
import com.amazon.carbonado.Nullable;
import com.amazon.carbonado.Storable;
import com.amazon.carbonado.Alias;
import com.amazon.carbonado.PrimaryKey;
import com.amazon.carbonado.Join;
import com.amazon.carbonado.FetchException;

import henry.carbonadoObjects.NotaDeVenta;
import henry.carbonadoObjects.Producto;


@Alias("items_de_venta")
@AlternateKeys(@Key({"codigoVenta", "itemNo"}))
@PrimaryKey("id")
public abstract class ItemVenta implements Storable<ItemVenta> {

	@Automatic 
	public abstract long getId();
	public abstract void setId(long s);
	

    @Alias("venta_cod_id")
    public abstract long getCodigoVenta();
    public abstract void setCodigoVenta(long s);

    @Alias("num")
    public abstract int getItemNo();
    public abstract void setItemNo(int s);

    @Alias("producto_id")
    public abstract String getCodigoProd();
    public abstract void setCodigoProd(String s);

    public abstract BigDecimal getCantidad();
    public abstract void setCantidad(BigDecimal s);

    @Join(internal="codigoVenta",
          external="codigo")
    public abstract NotaDeVenta getNotaDeVenta() throws FetchException;
    public abstract void setNotaDeVenta(NotaDeVenta s);


    @Join(internal="codigoProd", 
          external="codigo")
    public abstract Producto getProducto() throws FetchException;
    public abstract void setProducto(Producto s);

    @Nullable
    @Alias("nuevo_precio")
    public abstract BigDecimal getNuevoPrecio();
    public abstract void setNuevoPrecio(BigDecimal s);
	private Contenido contenido= null;
    public void setCont(Contenido cont) {
		contenido = cont;
		
	}
    public Contenido getCont() {
    	return contenido;
    }
}
