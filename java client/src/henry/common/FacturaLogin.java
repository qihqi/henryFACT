package henry.common;

import henry.carbonadoObjects.Usuario;

import java.awt.EventQueue;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;

@SuppressWarnings("serial")
public class FacturaLogin extends JFrame {

	private LoginPane contentPane;
	JPasswordField pass;
	JTextField user;
	JLabel message;
	Usuario usuario = null;
	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Config.bootstrap();
					FacturaLogin frame = new FacturaLogin();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	
	/**
	 * Create the frame.
	 */
	public FacturaLogin() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 393, 172);
		contentPane = new LoginPane(new Runnable () {
			public void run() {
				FacturaVentana ventana = new FacturaVentana(getUsuario());
				ventana.setVisible(true);
				setVisible(false);
				dispose();
			}
		});
		
		//aqui le puse el listener
		setContentPane(contentPane);
	}
	
	
	public Usuario getUsuario() {
		return contentPane.getUsuario();
	}
	


}

