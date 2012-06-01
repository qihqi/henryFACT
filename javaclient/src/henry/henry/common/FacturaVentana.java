package henry.common;

import javax.swing.ButtonGroup;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;

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
	private static final String []
			PAGO_LABEL = {"efectivo", "tarjeta"};
	private static final String [] 
			FORMAS_DE_PAGO = {Factura.EFECTIVO,
		                      Factura.TARGETA_CREDITO};
	private String formaPago = Factura.EFECTIVO;
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
		
		cliente = new ClientePanel(contenido);
		
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
					contenido.setCliente(cliente.getCliente());
					if (save()){
						print();
						clear();
					}
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
		
		
		//Formas de Pago
		ButtonGroup group = new ButtonGroup();
		JPanel buttons = new JPanel();
		buttons.setLayout(new MigLayout());
		for (int i = 0; i < FORMAS_DE_PAGO.length; i++) {
			JRadioButton rad = new JRadioButton(PAGO_LABEL[i]);
			if (i == 0) 
				rad.setSelected(true);
			final int index = i;
			rad.addActionListener(new ActionListener() {
				@Override
				public void actionPerformed(ActionEvent arg0) {
					formaPago = FORMAS_DE_PAGO[index];
				}
			});
			
			buttons.add(rad);
			group.add(rad);
		}
		
		JLabel label = new JLabel("A Pagar");
		pago = new JTextField();
		
		panel.add(label, "width :100:");
		panel.add(pago, "width :300:");
		panel.add(aceptar, "width :100:");
		panel.add(cancelar, "width :100:, wrap");
		panel.add(buttons, "span");
		
		setBounds(100, 100, 735, 655);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
	
	/* Guardar la nota de venta */
	public boolean save() throws RepositoryException {
		
		try {
			BigDecimal cambio = null;
			if (formaPago == Factura.EFECTIVO) {
				String pagado = pago.getText();
				BigDecimal pagoValor = new BigDecimal(pagado);
				
				cambio = pagoValor.subtract(contenido.getTotal());
				if (cambio.compareTo(new BigDecimal(0)) < 0){
					new SimpleDialog("Ingrese un valor \npagado mayor al total").setVisible(true);
					return false;
				}
			}
			Cliente theCliente = cliente.getCliente();
			contenido.setCliente(theCliente);
			contenido.saveFact(formaPago);
			
			
			//pop up con el cambio
			numero++;
			numeroLabel.setText("" + numero);
			
			if (formaPago == Factura.EFECTIVO)
				new SimpleDialog("El cambio es " + cambio).setVisible(true);
			return true;
		}
		catch (NumberFormatException e) {
			new SimpleDialog("Ingrese el valor pagado").setVisible(true);
			return false;
		}
		
	}
	/*Borrar el contenido */
	public void clear(){

		pago.setText("");
		contenido.clear();
		cliente.clear();
		pedidoField.setText("");
	}

	public void print() {
		FacturaPrinter printer = new FacturaPrinter(contenido.getItems(),
													contenido.getSubtotal(),
				                                    contenido.getTotal(),
				                                    contenido.getDescuento(),
				                                    cliente.getCliente());
		printer.printFactura();
	}
}
