/** Helper Fucntions */
package henry.common;

import static henry.carbonadoObjects.Usuario.getHashedPass;

import javax.swing.InputMap;
import javax.swing.KeyStroke;
import javax.swing.UIManager;

import henry.carbonadoObjects.Cliente;
import henry.carbonadoObjects.Contenido;
import henry.carbonadoObjects.Factura;
import henry.carbonadoObjects.ItemFactura;
import henry.carbonadoObjects.ItemVenta;
import henry.carbonadoObjects.Producto;
import henry.carbonadoObjects.Usuario;
import henry.carbonadoObjects.MyRepository;

import com.amazon.carbonado.ConfigurationException;
import com.amazon.carbonado.Cursor;
import com.amazon.carbonado.FetchException;
import com.amazon.carbonado.Query;
import com.amazon.carbonado.Repository;
import com.amazon.carbonado.RepositoryException;
import com.amazon.carbonado.Storable;
import com.amazon.carbonado.Storage;

public class Helper {
	
	//call this before starting application
	//will overide the action event of space to enter
	public static void mapEnterToActionEvent() {
		 InputMap im = (InputMap) UIManager.getDefaults().get("Button.focusInputMap");
	        Object pressedAction = im.get(KeyStroke.getKeyStroke("pressed SPACE"));
	        Object releasedAction = im.get(KeyStroke.getKeyStroke("released SPACE"));

	        im.put(KeyStroke.getKeyStroke("pressed ENTER"), pressedAction);
	        im.put(KeyStroke.getKeyStroke("released ENTER"), releasedAction);
	}
    
    public static Cliente getClienteByCode(String codigo) 
        throws RepositoryException
    {
        
        Cliente s = getStorableFor(Cliente.class);
        s.setCodigo(codigo);
        s.load();
        return s;
    }
    public static Usuario getUsuario(String codigo) 
        throws RepositoryException
    {
        Usuario s = getStorableFor(Usuario.class);
        s.setUsername(codigo);
        s.load();
        return s;
    }
    
    public static Producto getProducto(String codigo) 
            throws RepositoryException
        {
            Producto s = getStorableFor(Producto.class);
            s.setCodigo(codigo);
            s.load();
            return s;
        }
    
    public static void saveFacturaItem(int num, Producto prod, int cantidad, long codigo) 
    		throws ConfigurationException, RepositoryException 
    {
    	if (prod == null)
    		return;
    	ItemFactura item = getStorableFor(ItemFactura.class);
    	item.setCodigoFactura(codigo);
    	item.setProducto(prod);
    	item.setItemNo(num);
    	item.setPrecio(prod.getPrecio());
    	item.setCantidad(cantidad);
    	item.insert();
    }

    public static void saveVentaItem(int num, Producto prod, int cantidad, long codigo) 
    		throws ConfigurationException, RepositoryException 
    //requires: prod not null
    {
    	if (prod == null)
    		return;
    	ItemVenta item = getStorableFor(ItemVenta.class);
    	item.setCodigoVenta(codigo);
    	item.setProducto(prod);
    	item.setItemNo(num);
    	item.setCantidad(cantidad);
    	
    	item.insert();
    }
    
    public static Contenido fetchContenido(Producto prod, int bodegaId) 
    		throws RepositoryException 
    {
       	Storage<Contenido> sto = MyRepository.getRepository().storageFor(Contenido.class);
    	Query<Contenido> query = sto.query("prodId=? & bodegaId=?")
    			                    .with(prod.getCodigo()).with(bodegaId);
    	Cursor<Contenido> c = query.fetch();
    	if (!c.hasNext()) {
    		throw new FetchException("cannot fetch Contenido with " + prod + " and " + bodegaId);
    	}
    	return c.next();
    }
    
    public static void substractProd(Producto prod, int cantidad, int bodegaId) 
    		throws RepositoryException 
    {
		if (prod == null)
			return;
		
    	Contenido contenido = fetchContenido(prod, bodegaId);
		
		int nuevoContenido = contenido.getCantidad() - cantidad;
		if (nuevoContenido < 0)
			throw new RepositoryException("no hay tantos marcaderia " + prod.getNombre());
		
		contenido.setCantidad(nuevoContenido);
		contenido.update();
    }
    
    public static Factura getFactura(long num) 
    		throws ConfigurationException, RepositoryException
    {
        Factura factura = getStorableFor(Factura.class);
        factura.setCodigo(num);
        return factura;
    }
    public static <S extends Storable<S>> S getStorableFor(Class<S> theClass) 
    		throws ConfigurationException, RepositoryException 
    {
    	Repository repo = MyRepository.getRepository();
    	Storage<S> sto = repo.storageFor(theClass);
    	return sto.prepare();
    }
    
    public static Usuario authenticate(String username, String password) 
    		throws ConfigurationException, RepositoryException
    {
    	Usuario user;
    	user = getStorableFor(Usuario.class);
    	
    	System.err.println("I am here");
	    	
    	user.setUsername(username);
    	user.load();
    	
    	
    	String pass = user.getPassword();
    	String hashed = getHashedPass(password);
    	
    	System.out.printf("pass %s, hashed %s", pass, hashed);
    	if (!pass.equals(hashed))
    		throw new ConfigurationException("Wrong password");
    	return user;
    }
    
    //returns the string that is one bigger than arg
    //i.e abc maps to abd
    public static String nextString(String arg ) {
    	char [] argcontent = arg.toCharArray();
		int last = arg.length();
		argcontent[last - 1] += 1;
		String next = new String(argcontent);
		return next;
    }
    
    static final int MAX_ALERT_LENGTH = 23;
    
    public static void alert(String s) {
    	
    	(new SimpleDialog(s)).setVisible(true);
    }
    
  
}
