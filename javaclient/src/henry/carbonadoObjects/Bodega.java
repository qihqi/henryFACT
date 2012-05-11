package henry.carbonadoObjects;

import com.amazon.carbonado.Alias;
import com.amazon.carbonado.Automatic;
import com.amazon.carbonado.PrimaryKey;
import com.amazon.carbonado.Storable;

@PrimaryKey("id")
@Alias("bodegas")
public abstract class Bodega implements Storable<Bodega> {
    @Alias("id")
    @Automatic 
    public abstract int getId();
    public abstract void setId(int id);

    
    public abstract String getNombre();
    public abstract void setNombre(String s);
}
