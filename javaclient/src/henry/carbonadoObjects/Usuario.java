package henry.carbonadoObjects;

import java.math.BigInteger;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import com.amazon.carbonado.Storable;
import com.amazon.carbonado.Alias;
import com.amazon.carbonado.PrimaryKey;
import com.amazon.carbonado.adapter.TrueFalseAdapter;

@Alias("usuarios")
@PrimaryKey("username")
public abstract class Usuario implements Storable<Usuario> {

    public abstract String getUsername();
    public abstract void setUsername(String s);

    public abstract String getPassword();
    public abstract void setPassword(String s);

    @Alias("is_staff")
    @TrueFalseAdapter
    public abstract boolean isStaff();
    public abstract void setStaff(boolean s);

    @Alias("nivel")
    public abstract int getNivel();
    public abstract void setNivel(int s);
    
    @Alias("last_factura")
    public abstract long getLastFactura();
    public abstract void setLastFactura(long s);
    
    public static String getHashedPass(String s) {
    	byte [] ch = s.getBytes();
    	try {
			MessageDigest cript = MessageDigest.getInstance("SHA-1");
			cript.reset();
			cript.update(ch);
			
			String result = new BigInteger(1, cript.digest()).toString(16);
			return result;
    	} catch (NoSuchAlgorithmException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
    	}

    
    }
}
