/** Helper Fucntions */
package henry.common;

import static henry.carbonadoObjects.Usuario.getHashedPass;

import java.awt.Dialog;
import java.awt.KeyEventDispatcher;
import java.awt.KeyboardFocusManager;
import java.awt.event.KeyEvent;
import java.math.BigDecimal;

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
import com.amazon.carbonado.repo.jdbc.JDBCConnectionCapability;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

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
	
	//register hot key events
	//call in the main
	public static void registerHotkeys() {
		KeyboardFocusManager.getCurrentKeyboardFocusManager()
		  .addKeyEventDispatcher(new KeyEventDispatcher() {
		      private boolean called = false;
			  @Override
		      public boolean dispatchKeyEvent(KeyEvent e) {
		    	  if (called) {
		    		  called = false;
		    		  return false;
		    	  }
		    	  called = true;
				  switch(e.getKeyCode()) {
				      case KeyEvent.VK_F1:
				  		System.out.println("F1");
				  		break;
				      default:
		        	 return false;
		          }
				  
		          return false;
		      }
		});
	
	}
    public static List<ItemVenta> getItemVenta(long codigo) 
    		throws RepositoryException 
    {
    	int bodegaId = Integer.parseInt(Config.getConfig().getBodega());
    	Repository repo = MyRepository.getRepository();
		JDBCConnectionCapability cap = repo.getCapability(JDBCConnectionCapability.class);
		Connection con = cap.getConnection();
		String query = "select a.cantidad, b.nombre, c.* from items_de_venta as a " +
		        "inner join (productos as b, " +
		        "contenido_de_bodegas as c) on a.producto_id=b.codigo " +
		        "and a.producto_id=c.prod_id and c.bodega_id=" + bodegaId +
		        " where a.venta_cod_id = " + codigo + ";";
       	System.out.println(query);
		Statement stmt = null;
		List<ItemVenta> items = new ArrayList<ItemVenta>();
		try {
			stmt = con.createStatement();
			ResultSet set = stmt.executeQuery(query);
			while (set.next()) {
				ItemVenta item = getStorableFor(ItemVenta.class);
				Contenido cont = getStorableFor(Contenido.class);
				
				item.setCantidad(set.getBigDecimal("cantidad"));
				item.setCodigoProd(set.getString("prod_id"));
				cont.setBodegaId(set.getInt("bodega_id"));
				cont.setId(set.getInt("id"));
				cont.setCantidad(set.getBigDecimal("cant"));
				cont.setCantMayor(set.getInt("cant_mayorista"));
				cont.setPrecio(set.getBigDecimal("precio"));
				cont.setPrecio2(set.getBigDecimal("precio2"));
				//cont.setProdId(prodId);
				cont.setProdId(set.getString("prod_id"));
				cont.setNombreProd(set.getString("nombre"));
				item.setCont(cont);
				items.add(item);
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			throw new FetchException(e);
			
		}
		finally {
			try {
				stmt.close();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				throw new FetchException(e);
			}
			cap.yieldConnection(con);
		}
		return items;
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
    
 
    
    
    public static void saveFacturaItem(int num, Contenido prod, BigDecimal cantidad, long codigo) 
    		throws ConfigurationException, RepositoryException 
    {
    	if (prod == null)
    		return;
    	ItemFactura item = getStorableFor(ItemFactura.class);
    	item.setCodigoFactura(codigo);
    	item.setCodigoProd(prod.getProdId());
    	item.setItemNo(num);
    	item.setPrecio(prod.getPrecio());
    	item.setCantidad(cantidad);
    	item.insert();
    }

    public static void saveVentaItem(int num, Producto prod, BigDecimal cantidad, long codigo) 
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
  /*  
    public static Contenido fetchContenido(String prodId) 
    		throws RepositoryException 
    {
       	int bodegaId = Integer.parseInt(Config.getConfig().getBodega());
        
    	Storage<Contenido> sto = MyRepository.getRepository().storageFor(Contenido.class);
    	Query<Contenido> query = sto.query("prodId=? & bodegaId=?")
    			                    .with(prodId).with(bodegaId);
   
    	return query.loadOne();
    }
   */
    public static Contenido fetchContenido(String prodId) 
    		throws RepositoryException 
    {
    	
    	Repository repo = MyRepository.getRepository();
		JDBCConnectionCapability cap = repo.getCapability(JDBCConnectionCapability.class);
		Connection con = cap.getConnection();

       	int bodegaId = Integer.parseInt(Config.getConfig().getBodega());
        
		String query = "select a.*, b.nombre from contenido_de_bodegas as a " +
				        "inner join productos as b on a.prod_id=b.codigo" +
				        " where a.prod_id = '" + prodId
				       + "' and a.bodega_id= " + bodegaId + ";"; 
		System.out.println(query);
		Statement stmt = null;

		try {
			stmt = con.createStatement();
			ResultSet set = stmt.executeQuery(query);
			if (set.next()) {
				Contenido cont= getStorableFor(Contenido.class);
				cont.setBodegaId(set.getInt("bodega_id"));
				cont.setId(set.getInt("id"));
				cont.setCantidad(set.getBigDecimal("cant"));
				cont.setCantMayor(set.getInt("cant_mayorista"));
				cont.setPrecio(set.getBigDecimal("precio"));
				cont.setPrecio2(set.getBigDecimal("precio2"));
				cont.setProdId(prodId);
				cont.setNombreProd(set.getString("nombre"));
				return cont;
			}
			else {
				throw new FetchException("Producto no encontrado");
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			throw new FetchException(e);
			
		}
		finally {
			try {
				stmt.close();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				throw new FetchException(e);
			}
			cap.yieldConnection(con);
		}
		
   
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
    public static void alertnb(String s) {
    	
    	SimpleDialog d = (new SimpleDialog(s));
    			d.setModalityType(Dialog.ModalityType.MODELESS);
    			d.setVisible(true);
    }
  
}
