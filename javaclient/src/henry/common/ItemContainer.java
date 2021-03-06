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
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JViewport;

import net.miginfocom.swing.MigLayout;
import javax.swing.JTextField;

import org.joda.time.DateTime;

import com.amazon.carbonado.ConfigurationException;
import com.amazon.carbonado.PersistException;
import com.amazon.carbonado.RepositoryException;
import com.amazon.carbonado.Transaction;

@SuppressWarnings("serial")
public class ItemContainer extends JPanel {

	/** Tiene arreglo de itemPanel, representa los contenidos
	 *  de una factura/nota
	 * 
	 */
	
	private static final int DEFAULT_IVA = 12; 
	
	private static final int VIEWABLE_ROW_COUNT = 6;
	
	private int current; // the current selected item
	private ArrayList<ItemPanel> items;
	private Map<ItemPanel, Integer> reverseItem; 
	
	private JPanel content;
	
	private JLabel lCod;
	private JLabel lCant;
	private JLabel lNombre;
	private JLabel lPre;
	private JLabel lSub;
	private JScrollPane scroll;
	
	private JTextField ivaPorciento;
	private JTextField ivaValor;
	private JTextField totalValor;
	private JTextField descValor;
	
	private BigDecimal total;
	private BigDecimal subtotal;
	private BigDecimal descuento;

	private JTextField subValor;
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
				
		scroll = new JScrollPane(content);
		
		add(scroll, BorderLayout.CENTER);
		
		//---------TOTAL---------------------------
		JPanel totales = new JPanel();
		
		add(totales, BorderLayout.PAGE_END);
		totales.setLayout(new MigLayout("", "400[right][30][][100]","[][][][][]"));
		
		JLabel ivaLabel = new JLabel("IVA: ");	
		JLabel totalLabel = new JLabel("Total: ");
		JLabel porciento = new JLabel("%");
		JLabel netLabel = new JLabel("Valor Neto: ");
		JLabel descLabel = new JLabel("Descuento: ");
		JLabel subLabel = new JLabel("Valor Bruto: ");
		
		
		
		ivaPorciento = new JTextField("" + DEFAULT_IVA);
		ivaValor = new JTextField();
		ivaValor.setEditable(false);
		
		ivaPorciento.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				updateIVA();
			}
		});

		
		totales.add(subLabel, "cell 0 0");
		
		subValor = new JTextField();
		subValor.setEditable(false);

		
		totales.add(subValor, "cell 3 0,width :100:");

		descValor = new JTextField();
		descValor.setEditable(false);
		
		totales.add(descLabel, "cell 0 1");
		totales.add(descValor, "cell 3 1, width :100:");
		
		subtotalValor = new JTextField();
		subtotalValor.setEditable(false);
				
		totales.add(netLabel, "cell 0 2");
		totales.add(subtotalValor, "cell 3 2, width :100:");
				
		totales.add(ivaLabel, "cell 0 3");
		totales.add(ivaPorciento, "cell 1 3,width :30:");
		totales.add(porciento, "cell 2 3");
		totales.add(ivaValor, "cell 3 3,width :100:");
		
		totales.add(totalLabel, "cell 0 4" );
		totalValor = new JTextField();
		totalValor.setEditable(false);
		totales.add(totalValor, "cell 3 4,width :100:");
	}
	
	public void scrollDown() {
		
		JViewport vp = scroll.getViewport();
		Rectangle rect = vp.getBounds();
			
		rect.setLocation((int) rect.getX(),(int) rect.getY() + 100);
		
		vp.scrollRectToVisible(rect);
	}
	public void scrollUp() {
		
		JViewport vp = scroll.getViewport();
		Rectangle rect = vp.getBounds();
			
		//System.out.printf("%d %d", rect.getX(), rect.getY());
		rect.setLocation((int) rect.getX(),0);
		
		vp.scrollRectToVisible(rect);
	}


	/*
	 *  Do the event when shift is updated. ie update the total
	 *  and change the cursor to next line
	 */
	public void shiftEvent() {
		//move the cursor to next one
		//update the total
		updateSubtotal(); //also update descuento
		
		getFocus();
	}
	
	public void getFocus() {
		int threshold = items.size() - 1;
		if (current < threshold) {
		//dont need to make new one
			System.out.println("didnt add new");
			ItemPanel next = items.get(++current);
			next.focus();
		} 
		else if (current == threshold && items.get(threshold).getProdCont() == null) {
			items.get(threshold).focus();
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
		BigDecimal desc = new BigDecimal(0);
		for (ItemPanel item : items) {	
			currentTotal = currentTotal.add(item.getTotal());
			desc = desc.add(item.getDescuento());
		}
		descuento = desc;
		descValor.setText(descuento.toString());
		subValor.setText(currentTotal.toString());
		subtotal = currentTotal.subtract(descuento);
		
		subtotalValor.setText(subtotal.toString());
		
		if (!ivaPorciento.getText().equals(""))
			updateIVA();
	}
	
	public void updateIVA() {
		int percent = 0;
		try {
			percent = Integer.parseInt(ivaPorciento.getText());
		} catch (NumberFormatException e) {}
		
		BigDecimal iva = subtotal.multiply(new BigDecimal(percent))
		        .divide(new BigDecimal(100)).setScale(2, RoundingMode.HALF_UP);
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
	
	
	public long saveFact(String forma)  {
		//get codigo de factura
		long codigoFact = usuario.getLastFactura();
		//guardar la factura
		int bId = Integer.parseInt(Config.getConfig().getBodega());
		
		

		Transaction txn = null; 
		try {
			txn = MyRepository.getRepository().enterTransaction();
			boolean modificado = false;
			Factura factura = getStorableFor(Factura.class);
			factura.setCodigo(codigoFact);
			factura.setVendedor(usuario);
			factura.setCliente(cliente);
			factura.setFecha(DateTime.now());
			factura.setBodegaId(bId);
			factura.setFormaPago(forma);
			factura.setTotal(total);
			factura.setModificado(false);
			factura.setEliminado(false);
			factura.insert();
			
			int i = 0;
			for (ItemPanel v : items) {
				v.saveFacturaItem(i, factura.getId());
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
			txn.exit();
			return 0;
		} catch (Exception e) {
			
				try {
					if (txn != null)
						txn.exit();
				} catch (PersistException e1) {
					e1.printStackTrace();
				}
			e.printStackTrace();
			return -1;
			
		}
			
		//hacer la resta de inventario
		
		
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
			txn.exit();
			throw new PersistException(e);
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
		subValor.setText("");
		descValor.setText("");
		
		cliente = null;
		
		scrollUp();
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
		//clear();
		
		cliente = laNota.getCliente();
		List<ItemVenta> itemQuery = getItemVenta(laNota.getCodigo());
			
		//int currentUpdated = 0;
		for (ItemVenta i : itemQuery) {
			items.get(current).loadItem(i);
			shiftEvent();
			//currentUpdated++;
		}
				
	}

	public BigDecimal getDescuento() {
		if (descuento == null)
			return BigDecimal.ZERO;
		return descuento;
	}

	public void search() {
		items.get(current).buscarProd();
	}
	
	
}
