package henry.common;

import henry.carbonadoObjects.ItemFactura;
import henry.carbonadoObjects.ItemVenta;
import henry.carbonadoObjects.Producto;
import static henry.common.Helper.*;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.math.BigDecimal;

import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

import com.amazon.carbonado.ConfigurationException;
import com.amazon.carbonado.RepositoryException;

import net.miginfocom.swing.MigLayout;

import java.awt.Color;
import java.awt.Font;

@SuppressWarnings("serial")
public class ItemPanel extends JPanel {

	/** This Class represents a row in a nota de venta o factura
	 *  
	 *  TODO:
	 *  	-Make them navigable with tab/shift tab
	 *  	
	 */
	private Producto prod = null;
	
	private JTextField codigo;
	private JTextField cantidad;
	private JTextField nombre;
	private JTextField precio;
	private JTextField subtotal;
	
	private ItemContainer parent;
	
	private JButton buscar;

	private BigDecimal total;
	private BigDecimal nuevoPrecio = null;
	
	public ItemPanel(ItemContainer parent_) {
		initUI();
		parent = parent_;
		
	}
	
	//this class notifies the parent about currently selected item
	class ReFocusListener extends MouseAdapter {
		private ItemPanel thisPanel;
		public ReFocusListener(ItemPanel panel) {
			thisPanel  = panel;
		}
		@Override
		public void  mouseClicked(MouseEvent e) {
			System.err.println("Called");
			parent.setCurrent(thisPanel);
		}
	}
	
	//This class gives TextField ability to select all text 
	//when gain focus
	class HighlightFocusListener extends FocusAdapter {
		private JTextField text;
		public HighlightFocusListener(JTextField t) {
			text = t;
		}
		@Override
		public void focusGained(FocusEvent e) {
			SwingUtilities.invokeLater(new Runnable() {
				@Override
				public void run() {
					text.selectAll();
				}
			});
		}
	}
	
	public void initUI() {
		codigo = new JTextField();
		cantidad = new JTextField();
		nombre = new JTextField();
		nombre.setEditable(false);
		precio = new JTextField();
		precio.setEditable(false);
		subtotal = new JTextField();
		subtotal.setEditable(false);
		
		buscar = new JButton("Bus");
		buscar.setFont(new Font("Dialog", Font.BOLD, 10));
		buscar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				SearchDialog dialog = new SearchDialog("Producto", "Producto");
				dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
				dialog.setVisible(true);
				
				prod = (Producto) dialog.result;

				if (prod == null) //producto no encontrado, no haces nada
					return;
				
				codigo.setText(prod.getCodigo());
				try {
					loadProduct();
				} catch (RepositoryException e1) {
					//this should never run
					e1.printStackTrace();
				}
			}
		});
		
		codigo.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					loadProduct();
					cantidad.requestFocusInWindow();
				} catch (RepositoryException ex) {
					cantidad.requestFocusInWindow();
					codigo.requestFocusInWindow();
				}
					
			}
		});
		
		
		codigo.addMouseListener(new ReFocusListener(this));
		codigo.addFocusListener(new HighlightFocusListener(codigo));
		
		cantidad.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					loadCantidad();
					parent.shiftEvent();
			
				}
				catch (NullPointerException n) {
					//the product is not loaded
					codigo.requestFocusInWindow();					
				}
				catch (NumberFormatException n) {
					codigo.requestFocusInWindow();
					cantidad.requestFocusInWindow();
				}
			}
		});
		cantidad.addMouseListener(new ReFocusListener(this));
		cantidad.addFocusListener(new HighlightFocusListener(cantidad));

		final JButton newPrice = new JButton();
		newPrice.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				if (prod == null) {
					(new SimpleDialog("Selecciona producto primero!")).setVisible(true);
				}
					
				ModificarPrecioDialog dialog = new ModificarPrecioDialog();
				
				dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
				dialog.setVisible(true);
				
				if (dialog.isAccepted) {
					setNuevoPrecio(dialog.getNuevoPrecio());
				}
			}
		});
		
		setLayout(new MigLayout());
		
		add(buscar, "width :30:");
		add(codigo, "width :100:");
		add(cantidad, "width :80:");
		add(nombre, "width :200:");
		add(precio, "width :80: ");
		add(subtotal, "width :100:");
		add(newPrice, "width :15:,height :20:");
		
	
		
	}
	
	public void loadProduct() throws RepositoryException {
		String code = codigo.getText();
		if (prod == null || !prod.getCodigo().equals(code)) {
			//load new product
			prod = getProducto(code);
		}
		//update gui
		nombre.setText(prod.getNombre());
		precio.setText(prod.getPrecio().toString());
	}
	
	public void loadCantidad() {
		if (prod == null)
			throw new NullPointerException();
		//this throws NumberFormatException
		BigDecimal cant = new BigDecimal(cantidad.getText());
		BigDecimal precio = (nuevoPrecio == null) ?
			             prod.getPrecio() : nuevoPrecio;
	
		total = precio.multiply(cant);
	    subtotal.setText(total.toString());
	
	}

	/** Load the item give producto, cantidad, and modified precio 
	 * 
	 * @param producto
	 * @param cant
	 * @param np -  modified price, can be null
	 * @throws RepositoryException
	 */
	public void loadItem(ItemVenta item) 
			throws RepositoryException
	{
		codigo.setText(item.getCodigoProd());
		cantidad.setText("" + item.getCantidad());
		prod = item.getProducto();
		
		loadProduct();
		
		setNuevoPrecio(item.getNuevoPrecio());
		
		loadCantidad();
	}
	public void setNuevoPrecio(BigDecimal np) {
		if (prod == null)
			return;
		nuevoPrecio = np;
		if (np != null) {
			precio.setText(np.toString());
			precio.setBackground(Color.YELLOW);
		}
		else {
			precio.setText(prod.getPrecio().toString());
			precio.setBackground(null);
		}
		loadCantidad();
	}
	public void focus() {
		codigo.requestFocusInWindow();
	}
	
	public BigDecimal getTotal() {
		if (total == null)
			total = new BigDecimal(0);
		
		return total;
	}
	
	public Producto getProd() {
		return prod;
	}
	
	public int getCantidad() {
		String s = cantidad.getText();
		if (s.equals(""))
			return 0;
		return Integer.parseInt(cantidad.getText());
	}
	
	public void clear() {
		prod = null;
		total = new BigDecimal(0);
		codigo.setText("");
		cantidad.setText("");
		nombre.setText("");
		precio.setText("");
		precio.setBackground(null);
		subtotal.setText("");
	}
	
    public void saveFacturaItem(int num, long codigo) 
    		throws ConfigurationException, RepositoryException 
    {
    	if (prod == null)
    		return;
    	ItemFactura item = getStorableFor(ItemFactura.class);
    	item.setCodigoFactura(codigo);
    	item.setProducto(prod);
    	item.setItemNo(num);
    	
    	//usar precio cambiado si se ha cambiado
    	if (nuevoPrecio == null) {
    		item.setPrecio(prod.getPrecio());
    		item.setModificado(false);
    	} 
    	else {
    		item.setPrecio(nuevoPrecio);
    		item.setModificado(true);
    	}
    	  
    	item.setCantidad(getCantidad());
    	
    	item.insert();
    }

    public void saveVentaItem(int num, long codigo) 
    		throws ConfigurationException, RepositoryException 
    //requires: prod not null
    {
    	if (prod == null)
    		return;
    	ItemVenta item = getStorableFor(ItemVenta.class);
    	item.setCodigoVenta(codigo);
    	item.setProducto(prod);
    	item.setItemNo(num);
    	item.setCantidad(getCantidad());
    	item.setNuevoPrecio(nuevoPrecio);
    	
    	item.insert();
    }
	
    public boolean precioModificado() {
    	return nuevoPrecio != null;
    }
    
    
	
}
