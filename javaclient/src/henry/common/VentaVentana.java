package henry.common;

import henry.carbonadoObjects.Cliente;
import henry.carbonadoObjects.Usuario;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

import com.amazon.carbonado.RepositoryException;

import net.miginfocom.swing.MigLayout;

@SuppressWarnings("serial")
public class VentaVentana extends JFrame {

	private JPanel panel;
	private JLabel display;
	private ItemContainer contenido;
	private ClientePanel cliente;
	
	/**
	 * Create the application.
	 */
	public VentaVentana(Usuario user) {

		panel = new JPanel();
		display = new JLabel();
		getContentPane().add(panel);
		panel.setLayout(new MigLayout("", "[][][]",""));
		
		contenido = new ItemContainer(user, false);
		
		cliente = new ClientePanel();
		panel.add(cliente, "wrap, span");
		panel.add(contenido, "wrap, span");
		JButton aceptar = new JButton("aceptar");
		aceptar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					save();
				} catch (RepositoryException e1) {
					// TODO Auto-generated catch block
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
		panel.add(display, "width :300:");
		panel.add(aceptar, "width :100:");
		panel.add(cancelar, "width :100:");
		
		
		
		
		setBounds(100, 100, 741, 655);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
	
	/* Guardar la nota de venta */
	public void save() throws RepositoryException {
		Cliente theCliente = cliente.getCliente();
		contenido.setCliente(theCliente);
		long codigo = contenido.saveNota();
		new SimpleDialog("El codigo es: " + codigo).setVisible(true);
		display.setText("El codigo pasado era :" + codigo);
		
		clear();
	}
	/*Borrar el contenido */
	public void clear(){
		contenido.clear();
		cliente.clear();
	}
	

}
