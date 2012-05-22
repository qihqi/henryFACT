package henry.common;

import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import henry.carbonadoObjects.Cliente;
import henry.carbonadoObjects.Factura;
import henry.carbonadoObjects.NotaDeVenta;
import henry.carbonadoObjects.Usuario;
import static henry.common.Helper.*;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.math.BigDecimal;

import javax.swing.JButton;
import javax.swing.JTextField;

import com.amazon.carbonado.RepositoryException;

import net.miginfocom.swing.MigLayout;

@SuppressWarnings("serial")
public class FacturaVentana extends JFrame {

	private JPanel panel;
	
	private ItemContainer contenido;
	private ClientePanel cliente;
	private JLabel numeroLabel;
	private JTextField pago;
	private JTextField pedidoField;
	
	private long numero;
	private static final String FORMA_DE_PAGO = Factura.EFECTIVO;

	/**
	 * Create the application.
	 */
	public FacturaVentana(Usuario user) {
		panel = new JPanel();
		getContentPane().add(panel);
		panel.setLayout(new MigLayout("", "[][][][]",""));
		
		//mostrador de numero de factura;
		
		numero = user.getLastFactura();
		numeroLabel = new JLabel("" + numero);
		
		
		contenido = new ItemContainer(user, true);
		
		cliente = new ClientePanel();
		
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
		
		pedidoField = new JTextField();
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
		
		//poner numero de factura
		panel.add(new JLabel("No. de Factura: "));
		panel.add(numeroLabel, "cell 3 0, wrap, width :100:");
		
		panel.add(cliente, "wrap, span");
		panel.add(contenido, "wrap, span");
		JButton aceptar = new JButton("aceptar");
		aceptar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					save();
					print();
					clear();
				} catch (RepositoryException e1) {
					
					e1.printStackTrace();
				}
			}
		});
		JButton cancelar = new JButton("cancelar");
		cancelar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				clear();
				
			}
		});
		
		
		JLabel label = new JLabel("A Pagar");
		pago = new JTextField();
		
		panel.add(label, "width :100:");
		panel.add(pago, "width :300:");
		panel.add(aceptar, "width :100:");
		panel.add(cancelar, "width :100:");
		
		
		
		
		setBounds(100, 100, 735, 655);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
	
	/* Guardar la nota de venta */
	public void save() throws RepositoryException {
		
		try {
			String pagado = pago.getText();
			BigDecimal pagoValor = new BigDecimal(pagado);
			
			BigDecimal cambio = pagoValor.subtract(contenido.getTotal());
			if (cambio.compareTo(new BigDecimal(0)) < 0){
				new SimpleDialog("Ingrese un valor \npagado mayor al total").setVisible(true);
				return;
			}
			
			Cliente theCliente = cliente.getCliente();
			contenido.setCliente(theCliente);
			contenido.saveFact(FORMA_DE_PAGO);
			
			
			//pop up con el cambio
			numero++;
			numeroLabel.setText("" + numero);
			
			new SimpleDialog("El cambio es " + cambio).setVisible(true);
			
		}
		catch (NumberFormatException e) {
			new SimpleDialog("Ingrese el valor pagado").setVisible(true);
		}
		
	}
	/*Borrar el contenido */
	public void clear(){
		alert("HERE");
		pago.setText("");
		contenido.clear();
		cliente.clear();
		pedidoField.setText("");
	}

	public void print() {
		FacturaPrinter printer = new FacturaPrinter(contenido.getItems(),
													contenido.getSubtotal(),
				                                    contenido.getTotal(),
				                                    cliente.getCliente());
		printer.printFactura();
	}
}
