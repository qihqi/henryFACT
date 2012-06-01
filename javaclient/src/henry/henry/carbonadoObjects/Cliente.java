package henry.carbonadoObjects;

import com.amazon.carbonado.Nullable;
import com.amazon.carbonado.Storable;
import com.amazon.carbonado.Alias;
import com.amazon.carbonado.PrimaryKey;

import org.joda.time.DateTime;

@Alias("clientes")
@PrimaryKey("codigo")
public abstract class Cliente implements Storable<Cliente> {

    public abstract String getCodigo();
    public abstract void setCodigo(String s);

    public abstract String getNombres();
    public abstract void setNombres(String s);

    public abstract String getApellidos();
    public abstract void setApellidos(String s);

    @Nullable
    public abstract String getDireccion();
    public abstract void setDireccion(String s);

    @Nullable
    public abstract String getCiudad();
    public abstract void setCiudad(String s);

    //esto debe ser un enum
    public abstract String getTipo();
    public abstract void setTipo(String s);

    @Alias("cliente_desde")
    public abstract DateTime getJoinedDate();
    public abstract void setJoinedDate(DateTime s);
    
    @Alias("telefono")
    @Nullable
    public abstract String getTelefono();
    public abstract void setTelefono(String s);

}

