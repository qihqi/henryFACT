package henry.common;

import static henry.common.Helper.*;
import henry.carbonadoObjects.Cliente;
import henry.carbonadoObjects.NotaDeVenta;
import henry.carbonadoObjects.Usuario;
import henry.printer.GenericPrinter;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

import com.amazon.carbonado.RepositoryException;

import net.miginfocom.swing.MigLayout;

@SuppressWarnings("serial")
public class VentaVentana extends JFrame implements Ventana{

	private JPanel panel;
	private JLabel display;
	private ItemContainer contenido;
	private ClientePanel cliente;
	private long codigo;
	
	/**
	 * Create the application.
	 */
	public VentaVentana(Usuario user) {

		panel = new JPanel();
		display = new JLabel();
		getContentPane().add(panel);
		panel.setLayout(new MigLayout("", "[][][][]",""));
		
		
		JButton buscarPorCliente = new JButton("Buscar por Cliente");
		buscarPorCliente.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				FacturaPorCliente dialog = new FacturaPorCliente();
				dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
				dialog.setVisible(true);
				
				NotaDeVenta nota = dialog.result;
				Cliente cl;
				try {
					cl = nota.getCliente();
					cliente.loadCliente(cl);
					contenido.loadNota(nota);
				} catch (RepositoryException e1) {
					e1.printStackTrace();
				}
			}
			
		});
		
		JTextField pedidoField = new JTextField();
		pedidoField.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				try {
					String codigoNota = e.getActionCommand();
					NotaDeVenta nota = getStorableFor(NotaDeVenta.class);
					nota.setCodigo(Long.parseLong(codigoNota));
					nota.load();
					Cliente cl = nota.getCliente();
					cliente.loadCliente(cl);
					contenido.loadNota(nota);
					
				}
				catch (NumberFormatException e2) {
					alert("Codigo de Nota de Venta incorrecta!!");
					e2.printStackTrace();
				
				}
				catch (RepositoryException e1) {
					alert("Codigo de Nota de Venta incorrecta!!");
					e1.printStackTrace();
				}
			}
		});
		
		//poner llamador de nota de pedido
		panel.add(new JLabel("No. de Pedido:"));
		panel.add(pedidoField, "width :300:");
		
		//poner boton q busca por cliente
		panel.add(buscarPorCliente);
		
		panel.add(new JLabel(), "wrap, width :200:");
		
		contenido = new ItemContainer(user, false);
		
		cliente = new ClientePanel(contenido);
		panel.add(cliente, "wrap, span");
		panel.add(contenido, "wrap, span");
		JButton aceptar = new JButton("aceptar");
		aceptar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				aceptar();
			}
		});
		JButton cancelar = new JButton("cancelar");
		cancelar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				clear();
				
			}
		});
		panel.add(display, "width :300:");
		panel.add(aceptar, "width :100:");
		panel.add(cancelar, "width :100:, wrap");
		
		JLabel hotkeys = new JLabel("F5=Buscar Cliente  F6=Buscar Producto " +
				"F7=Pagar  F8=Aceptar  F9=Cancelar");
		panel.add(hotkeys, "span");
		
		
		setTitle("Nota de Pedido");
		setBounds(100, 100, 741, 655);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
	
	/* Guardar la nota de venta */
	
	public boolean save() throws RepositoryException {
		Cliente theCliente = cliente.getCliente();
		if (theCliente == null) {
			alert("Ingrese Cliente");
			return false;
		}
		contenido.setCliente(theCliente);
		codigo = contenido.saveNota();
		
		alertnb("El codigo es: " + codigo);
		display.setText("El codigo pasado era :" + codigo);
		
		
		return true;
	}
	/*Borrar el contenido */
	@Override
	public void clear(){
		contenido.clear();
		cliente.clear();
	}

	@Override
	public ItemContainer getItemContainer() {
		return contenido;
	}

	@Override
	public ClientePanel getClientePanel() {
		// TODO Auto-generated method stub
		return cliente;
	}
	
	@Override 
	public void aceptar() {
		try {
			if (save()) {
				if (Config.getConfig().getFacturaBlanco())
					print();
				clear();
			}
		} catch (RepositoryException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}
	
	public void print() {
		GenericPrinter printer = GenericPrinter.makePrinter(contenido.getItems(),
				contenido.getSubtotal(),
                contenido.getTotal(),
                contenido.getDescuento(),
                cliente.getCliente(),
                codigo);
		printer.printFactura();
	}
	@Override
	public void pagar() {
		// TODO Auto-generated method stub
		
	}
}
