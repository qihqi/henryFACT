package henry.carbonadoObjects;

import java.math.BigDecimal;

import com.amazon.carbonado.Alias;
import com.amazon.carbonado.AlternateKeys;
import com.amazon.carbonado.Automatic;
import com.amazon.carbonado.FetchException;
import com.amazon.carbonado.Join;
import com.amazon.carbonado.PrimaryKey;
import com.amazon.carbonado.Key;

import com.amazon.carbonado.Storable;


@Alias("contenido_de_bodegas")
@PrimaryKey("id")
@AlternateKeys(@Key({"bodegaId", "prodId"}))
public abstract class Contenido implements Storable<Contenido>{
	
    @Alias("id")
    @Automatic 
    public abstract int getId();
    public abstract void setId(int id);

    @Alias("bodega_id")
    public abstract int getBodegaId();
    public abstract void setBodegaId(int s);
    
    @Alias("prod_id")
    public abstract String getProdId();
    public abstract void setProdId(String s);
    
    @Alias("cant")
    public abstract int getCantidad();
    public abstract void setCantidad(int s);
    
    @Join(internal="prodId",
          external="codigo")
    public abstract Producto getProducto() throws FetchException;
    public abstract void setProducto(Producto p);
	
    @Join(internal="bodegaId",
          external="id")
    public abstract Bodega getBodega() throws FetchException;
    public abstract void setBodega(Bodega p);
    
    @Alias("precio")
    public abstract BigDecimal getPrecio();
    public abstract void setPrecio(BigDecimal s);

    @Alias("precio2")
    public abstract BigDecimal getPrecio2();
    public abstract void setPrecio2(BigDecimal s);

    public BigDecimal getDescuento() {
		return getPrecio().subtract(getPrecio2());
	}

}
