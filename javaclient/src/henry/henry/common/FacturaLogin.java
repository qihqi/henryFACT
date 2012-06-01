package henry.common;

import henry.carbonadoObjects.MyRepository;
import henry.carbonadoObjects.Usuario;
import static henry.common.Helper.mapEnterToActionEvent;

import java.awt.EventQueue;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
//test
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
					mapEnterToActionEvent();
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
				ventana.addWindowListener(new WindowAdapter() {
					@Override 
					public void windowClosing(WindowEvent e) {
						MyRepository.close();
					} 
				});
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

