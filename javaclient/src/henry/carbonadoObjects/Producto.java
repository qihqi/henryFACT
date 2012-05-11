package henry.carbonadoObjects;

import java.math.BigDecimal;

import com.amazon.carbonado.Storable;
import com.amazon.carbonado.Alias;
import com.amazon.carbonado.PrimaryKey;
import com.amazon.carbonado.Join;
import com.amazon.carbonado.FetchException;
import com.amazon.carbonado.Query;

import henry.carbonadoObjects.ItemFactura;
import henry.carbonadoObjects.ItemVenta;

@Alias("productos")
@PrimaryKey("codigo")
public abstract class Producto implements Storable<Producto> {

    @Alias("codigo")
    public abstract String getCodigo();
    public abstract void setCodigo(String s);

    @Alias("precio")
    public abstract BigDecimal getPrecio();
    public abstract void setPrecio(BigDecimal s);

    @Alias("nombre")
    public abstract String getNombre();
    public abstract void setNombre(String s);

     
    @Join(internal="codigo",
          external="codigoProd")
    public abstract Query<ItemVenta> getItemsVenta() throws FetchException;

    @Join(internal="codigo",
          external="codigoProd")
    public abstract Query<ItemFactura> getItemsFactura() throws FetchException;
    
}
