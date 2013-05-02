package henry.common;

import static henry.common.Helper.*;
import henry.carbonadoObjects.MyRepository;
import henry.carbonadoObjects.Usuario;

import java.awt.EventQueue;
import java.awt.KeyboardFocusManager;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;

/*
 * This is the program!!
 * hola
 * 
 */
@SuppressWarnings("serial")
public class LoginVentana extends JFrame {

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
				//	registerHotkeys();
					LoginVentana frame = new LoginVentana();
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
	public LoginVentana() {
		setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		setBounds(100, 100, 393, 172);
		contentPane = new LoginPane(new Runnable () {
			public void run() {
				VentaVentana ventana = new VentaVentana(getUsuario());
				ventana.addWindowListener(new WindowAdapter() {
					@Override 
					public void windowClosing(WindowEvent e) {
						MyRepository.close();
					} 
				});
				ventana.setVisible(true);
				KeyboardFocusManager.getCurrentKeyboardFocusManager()
				  .addKeyEventDispatcher(new HotKeyEventDispatcher(ventana) );
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
