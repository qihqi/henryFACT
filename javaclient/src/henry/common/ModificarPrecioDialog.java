package henry.common;

import java.awt.BorderLayout;
import java.awt.Dialog;
import java.math.BigDecimal;

import javax.swing.JDialog;

@SuppressWarnings("serial")
public class ModificarPrecioDialog extends JDialog {

	private final LoginPane contentPanel;

	private BigDecimal precio;
	public boolean isAccepted;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		try {
			Config.bootstrap();
			ModificarPrecioDialog dialog = new ModificarPrecioDialog();
			dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
			dialog.setVisible(true);
			System.err.println(dialog.getNuevoPrecio());
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * Create the dialog.
	 */
	public ModificarPrecioDialog() {
		super(null, Dialog.ModalityType.DOCUMENT_MODAL);
		setBounds(100, 100, 350, 128);
		getContentPane().setLayout(new BorderLayout());
		
		Runnable run = new Runnable() {
			public void run() {
				ModificarPrecio mod = new ModificarPrecio(contentPanel.getUsuario());
				mod.setVisible(true);
				precio = mod.getPrecio();
				isAccepted = mod.isAccepted();
				dispose();
			}
		};
		contentPanel = new LoginPane(run);
		
		getContentPane().add(contentPanel, BorderLayout.CENTER);
	}

	public BigDecimal getNuevoPrecio() {
		System.err.println("returning " + precio);
		return precio;
	}
}
