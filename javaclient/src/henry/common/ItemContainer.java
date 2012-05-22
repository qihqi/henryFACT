package henry.common;

import henry.carbonadoObjects.Cliente;
import henry.carbonadoObjects.Factura;
import henry.carbonadoObjects.ItemVenta;
import henry.carbonadoObjects.MyRepository;
import henry.carbonadoObjects.NotaDeVenta;
import henry.carbonadoObjects.Usuario;
import static henry.common.Helper.*;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.math.BigDecimal;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;

import net.miginfocom.swing.MigLayout;
import javax.swing.JTextField;

import org.joda.time.DateTime;

import com.amazon.carbonado.ConfigurationException;
import com.amazon.carbonado.Cursor;
import com.amazon.carbonado.PersistException;
import com.amazon.carbonado.Query;
import com.amazon.carbonado.RepositoryException;
import com.amazon.carbonado.Transaction;

@SuppressWarnings("serial")
public class ItemContainer extends JPanel {

	/** Tiene arreglo de itemPanel, representa los contenidos
	 *  de una factura/nota
	 * 
	 */
	
	private static final int DEFAULT_IVA = 12; 
	
	private int current; // the current selected item
	private ArrayList<ItemPanel> items;
	private Map<ItemPanel, Integer> reverseItem; 
	
	private JPanel content;
	
	private JLabel lCod;
	private JLabel lCant;
	private JLabel lNombre;
	private JLabel lPre;
	private JLabel lSub;
	
	private JTextField ivaPorciento;
	private JTextField ivaValor;
	private JTextField totalValor;
	
	
	private BigDecimal total;
	private BigDecimal subtotal;
	
	private JTextField subtotalValor;
	
	Cliente cliente;
	Usuario usuario;
	
//-------------------------------------------------------------------------------	
	public ItemContainer(Usuario u, boolean fact) {
		super(new BorderLayout());
		usuario = u;
		
		items = new ArrayList<ItemPanel>();
		current = 0;
		reverseItem = new HashMap<ItemPanel, Integer>();
		initUI();
		
	}
	
	public void initUI() {
		
		JPanel header = new JPanel(new MigLayout("",
				                       "90[]10[][][][]",""));
		
		lCod = new JLabel();
		lCod.setText("Codigo");
		
		lCant = new JLabel();
		lCant.setText("Cantidad");
		
		lNombre = new JLabel();
		lNombre.setText("Nombre del Producto");
		
		lPre = new JLabel();
		lPre.setText("Precio");
		
		lSub = new JLabel();
		lSub.setText("Subtotal");
		
		header.add(lCod, "width :100:");
		header.add(lCant, "width :80:");
		header.add(lNombre, "width :200:");
		header.add(lPre, "width :80:");
		header.add(lSub, "width :100:");
		setPreferredSize(new Dimension(792, 570));

		add(header, BorderLayout.PAGE_START);

		//-----------------CONTENT--------------------------------
		content = new JPanel(new MigLayout());
		
		ItemPanel first = new ItemPanel(this);
		items.add(first);
		reverseItem.put(first, 0);
		
		content.add(first, "wrap");
		//content.add(new ItemPanel(this), "wrap");
				
		JScrollPane scroll = new JScrollPane(content);
		
		add(scroll, BorderLayout.CENTER);
		
		//---------TOTAL---------------------------
		JPanel totales = new JPanel();
		
		add(totales, BorderLayout.PAGE_END);
		totales.setLayout(new MigLayout("", "350[right][80][][100]","[][][]"));
		
		JLabel ivaLabel = new JLabel("IVA: ");	
		JLabel totalLabel = new JLabel("Total: ");
		JLabel porciento = new JLabel("%");
		JLabel subLabel = new JLabel("Subtotal :");
		new JLabel("Descuento :");
		
		ivaPorciento = new JTextField("" + DEFAULT_IVA);
		ivaValor = new JTextField();
		ivaValor.setEditable(false);
		
		ivaPorciento.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				updateIVA();
			}
		});
		
		totales.add(subLabel, "cell 0 0");
		
		subtotalValor = new JTextField();
		subtotalValor.setEditable(false);
		totales.add(subtotalValor, "cell 3 0,width :100:");

		totales.add(ivaLabel, "cell 0 1");
		totales.add(ivaPorciento, "cell 1 1,width :80:");
		totales.add(porciento, "cell 2 1");
		totales.add(ivaValor, "cell 3 1,width :100:");
		
		totales.add(totalLabel, "cell 0 2" );
		totalValor = new JTextField();
		totalValor.setEditable(false);
		totales.add(totalValor, "cell 3 2,width :100:");
	}
	
	


	/*
	 *  Do the event when shift is updated. ie update the total
	 *  and change the cursor to next line
	 */
	public void shiftEvent() {
		//move the cursor to next one
		//update the total
		updateSubtotal();
		if (current < items.size() - 1) {
		//dont need to make new one
			System.out.println("didnt add new");
			ItemPanel next = items.get(++current);
			next.focus();
		} 
		else {
			//allocate new ones
			ItemPanel newOne = new ItemPanel(this);
			items.add(newOne);
			content.add(newOne, "wrap");
			content.revalidate();
			current++;
			reverseItem.put(newOne, current);
			newOne.focus();
			
		}
	}
		
	public void updateSubtotal() {
		BigDecimal currentTotal = new BigDecimal(0);
		for (ItemPanel item : items) {	
			currentTotal = currentTotal.add(item.getTotal());
		}
		subtotal = currentTotal;
		subtotalValor.setText(subtotal.toString());
		if (!ivaPorciento.getText().equals(""))
			updateIVA();
	}
	
	public void updateIVA() {
		int percent = Integer.parseInt(ivaPorciento.getText());
		
		BigDecimal iva = subtotal.multiply(new BigDecimal(percent))
		        .divide(new BigDecimal(100)
		 );
		ivaValor.setText(iva.toString());
		total = iva.add(subtotal);
		totalValor.setText(total.toString());
		
		
	}
	
	public void setCurrent(ItemPanel item) {
		current = reverseItem.get(item).intValue();
	}
	public ArrayList<ItemPanel> getItems() {
    	return items;
    }
	
	
	public long saveFact(String forma) throws ConfigurationException, RepositoryException {
		//get codigo de factura
		long codigoFact = usuario.getLastFactura();
		//guardar la factura
	
		int bodegaId = Integer.parseInt(Config.getConfig().getBodega());
		
		Transaction txn = MyRepository.getRepository().enterTransaction();
		try {
			boolean modificado = false;
			Factura factura = getStorableFor(Factura.class);
			factura.setCodigo(codigoFact);
			factura.setVendedor(usuario);
			factura.setCliente(cliente);
			factura.setFecha(new DateTime());
			int bId = Integer.parseInt(Config.getConfig().getBodega());
			factura.setBodegaId(bId);
			factura.setFormaPago(forma);
			factura.setTotal(total);
			factura.setModificado(false);
			
			
			factura.insert();
			
			int i = 0;
			for (ItemPanel v : items) {
				v.saveFacturaItem(i, codigoFact);
				substractProd(v.getProd(), v.getCantidad(), bodegaId);
				if (v.precioModificado())
					modificado = true;
				i++;
			} 
			if (modificado) {
				factura.setModificado(true);
				factura.update();
			}
			usuario.setLastFactura(codigoFact + 1);
			usuario.update();
			
			txn.commit();
		} catch (RepositoryException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
		} finally {
			txn.exit();
		}
			
		//hacer la resta de inventario
		
		
		return 0;
	}
	

	public long saveNota() throws PersistException {
		Transaction txn = null;
		long codigo = 0;
	
		try {
			boolean modificado = false;
			txn = MyRepository.getRepository().enterTransaction();
			NotaDeVenta nota = getStorableFor(NotaDeVenta.class);
			nota.setVendedor(usuario);
			nota.setCliente(cliente);
			nota.setFecha(new DateTime());
			int bId = Integer.parseInt(Config.getConfig().getBodega());
			nota.setBodegaId(bId);
			nota.setModificado(false);
			nota.insert();
			
			codigo = nota.getCodigo();
			int i = 0;
			for (ItemPanel v : items) {
				v.saveVentaItem(i, codigo);
				if (v.precioModificado())
					modificado = true;
				i++;
			}
			if (modificado) {
				nota.setModificado(true);
				nota.update();
			}
			txn.commit();
		} catch (RepositoryException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			txn.exit();
		}
		
		return codigo;
	}
	
	public void clear() {
		//save the first itemPanel
		ItemPanel first = items.get(0);
		first.clear();
		//for (int i = 1; i < items.size(); i++)
			//items.get(i)first;
		//update new content
		content.removeAll();
		content.repaint();
		content.add(first, "wrap");
		//update the records
		items.clear();
		items.add(first);
		reverseItem.clear();
		reverseItem.put(first, 0);
		
		//update new total etc//
		current = 0;
		total = null;
		subtotal = null;
		
		//ivaPorciento.setText("");
		ivaValor.setText("");
		totalValor.setText("");
		subtotalValor.setText("");
		
		cliente = null;
	}
	
	public void setCliente(Cliente cliente) {
		this.cliente = cliente;
	}
	
	public BigDecimal getTotal() {
		return total;
	}

	public BigDecimal getSubtotal() {
		return subtotal;
	}
	public void loadNota(NotaDeVenta laNota) throws RepositoryException {
		clear();
		
		cliente = laNota.getCliente();
		Query<ItemVenta> itemQuery = laNota.getItems();
		Cursor<ItemVenta> cur = itemQuery.fetch();
			
		int currentUpdated = 0;
		while (cur.hasNext()) {
			ItemVenta curItem = cur.next();
		
			items.get(currentUpdated).loadItem(curItem);
			shiftEvent();
			currentUpdated++;
		}
				
	}
	
}
