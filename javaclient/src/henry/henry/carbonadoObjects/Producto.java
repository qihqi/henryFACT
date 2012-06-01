package henry.carbonadoObjects;

import java.math.BigDecimal;

import com.amazon.carbonado.AlternateKeys;
import com.amazon.carbonado.Nullable;
import com.amazon.carbonado.Storable;
import com.amazon.carbonado.Alias;
import com.amazon.carbonado.PrimaryKey;
import com.amazon.carbonado.Join;
import com.amazon.carbonado.FetchException;
import com.amazon.carbonado.Query;
import com.amazon.carbonado.Key;

import henry.carbonadoObjects.ItemFactura;
import henry.carbonadoObjects.ItemVenta;

@Alias("productos")
@PrimaryKey("codigo")
public abstract class Producto implements Storable<Producto> {

    @Alias("codigo")
    public abstract String getCodigo();
    public abstract void setCodigo(String s);


    @Alias("nombre")
    public abstract String getNombre();
    public abstract void setNombre(String s);

    @Alias("codigo_barra")
    @Nullable
    public abstract Integer getCodigoBarra();
    public abstract void setCodigoBarra(Integer s);
    
    
    
    @Join(internal="codigo",
          external="codigoProd")
    public abstract Query<ItemVenta> getItemsVenta() throws FetchException;

    @Join(internal="codigo",
          external="codigoProd")
    public abstract Query<ItemFactura> getItemsFactura() throws FetchException;
    
}
