package henry.carbonadoObjects;

import com.amazon.carbonado.Alias;
import com.amazon.carbonado.Nullable;
import com.amazon.carbonado.PrimaryKey;
import com.amazon.carbonado.Storable;

@Alias("descuentos")
@PrimaryKey("param")
public abstract class Descuento implements Storable<Descuento> {
	
	public abstract String getParam();
	public abstract void setParam(String s);
	
	@Nullable
	public abstract Integer getValue();
	public abstract void setValue(Integer s);
}
