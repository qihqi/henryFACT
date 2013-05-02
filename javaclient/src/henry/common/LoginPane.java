package henry.common;

import henry.carbonadoObjects.Usuario;

import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;

import com.amazon.carbonado.RepositoryException;

import net.miginfocom.swing.MigLayout;

import static henry.common.Helper.*;

@SuppressWarnings("serial")
public class LoginPane extends JPanel implements ActionListener{

	private JLabel message;
	private JTextField user;
	private JPasswordField pass;
	private Usuario usuario;
	private Runnable nextWindow;
	/**
	 * Create the panel.
	 */
	public LoginPane(Runnable next) {
		nextWindow = next;
		
		setBorder(new EmptyBorder(5, 5, 5, 5));
		setLayout(new MigLayout("", "[100][200]", ""));
		
		message = new JLabel();
		
		JLabel userLabel = new JLabel("Usuario: ");
		JLabel passLabel = new JLabel("Clave: ");
		
		user = new JTextField();
		pass = new JPasswordField();
		
		add(userLabel);
		add(user, "wrap, width :200:");
		add(passLabel);
		add(pass, "wrap, width :200:");
		
		JButton login = new JButton("Ingresar");
		add(login);
		add(message);
		
		//aqui le puse el listener
		login.addActionListener(this);

	}
	
	public boolean validateUsuario() {
		String username = user.getText();
		String password = new String(pass.getPassword());
		if (username.equals("") || password.equals("")) 
			return false;
		
		try {
			System.out.println("here");
					
			usuario = authenticate(username, password);
		} catch (RepositoryException e) {
			return false;
		}
		return true;
	}
	@Override 
	public void actionPerformed(ActionEvent e) {
		if (!validateUsuario()) {
			message.setText("Usuario o clave equivocado");
			user.setText("");
			pass.setText("");
			return;
		}
			
		EventQueue.invokeLater(nextWindow);
	}

	public Usuario getUsuario() {
		if (usuario == null) {
			if (!validateUsuario())
				return null;
		}
		System.err.println(usuario);
		return usuario;
	}
	
	public void setMessage(String s) {
		message.setText(s);
	}
}
