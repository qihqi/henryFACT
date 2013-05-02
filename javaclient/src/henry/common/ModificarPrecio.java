package henry.common;

import henry.carbonadoObjects.Usuario;

import java.awt.BorderLayout;
import java.awt.Dialog;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.math.BigDecimal;

import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JTextField;
import net.miginfocom.swing.MigLayout;

@SuppressWarnings("serial")
public class ModificarPrecio extends JDialog {

	private final JPanel contentPanel = new JPanel();
	
	private JRadioButton modified;
	private JRadioButton unmodified;
	private ButtonGroup group;
	
	private JTextField nuevoPrecio;

	private boolean is_modified = true;
	private boolean is_accepted = false;
	
	private BigDecimal precio;
	
	/**
	 * Create the dialog.
	 * @param usuario 
	 */
	public ModificarPrecio(Usuario usuario) {
		super(null, Dialog.ModalityType.APPLICATION_MODAL);
		setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
		if (usuario.getNivel() < 2) {
			SimpleDialog dia = new SimpleDialog("No tiene privilegios suficientes");
			dia.setSize(400, 200);
			dia.setVisible(true);
			dispose();
			return;
		}
		initUI();
	}
	
	public void initUI() {
		setBounds(100, 100, 229, 129);

		getContentPane().setLayout(new BorderLayout());
		contentPanel.setLayout(new MigLayout());
		
		
		getContentPane().add(contentPanel, BorderLayout.CENTER);
	
		modified =  new JRadioButton("Modificar", true);
		modified.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				is_modified = true;
				nuevoPrecio.setEditable(true);
			}
		});
		
		unmodified = new JRadioButton("Restaurar", false);
		unmodified.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				is_modified = false;
				nuevoPrecio.setText("");
				nuevoPrecio.setEditable(false);
			}
		});
		
		group = new ButtonGroup();
		group.add(modified); 
		group.add(unmodified);
		
		contentPanel.add(modified);
		contentPanel.add(unmodified, "wrap");
		
		nuevoPrecio = new JTextField();
		
		contentPanel.add(new JLabel("Precio: "));
		contentPanel.add(nuevoPrecio, "width :100:");
		

		JPanel buttonPane = new JPanel();
		buttonPane.setLayout(new FlowLayout(FlowLayout.RIGHT));
		JButton accept = new JButton("Aceptar");
		accept.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					precio = new BigDecimal(nuevoPrecio.getText());
					is_accepted = true;
					dispose();
				} 
				catch (NumberFormatException e1) {
					nuevoPrecio.requestFocusInWindow();
				}
			}
		});
		buttonPane.add(accept);
		getContentPane().add(buttonPane, BorderLayout.SOUTH);
		
	}
	
	public boolean isModified() {
		return is_modified;
	}
	
	public BigDecimal getPrecio() {
		if (!is_modified)
			return null;
		return precio;
	}

	public boolean isAccepted() {
		return is_accepted;
	}
}
