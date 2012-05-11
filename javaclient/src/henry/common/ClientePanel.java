package henry.common;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import henry.carbonadoObjects.Cliente;
import static henry.common.Helper.*;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;

import com.amazon.carbonado.RepositoryException;

import net.miginfocom.swing.MigLayout;

public class ClientePanel extends JPanel {

	/**
	 * 
	 */
	private static final long serialVersionUID = 8993493064487143324L;
	private Cliente cliente = null;
	private JButton buscar;
	private JLabel label;
	private JTextField codigo;
	private JLabel nombre;
	private JCheckBox general;
	
	private void initUI() {
		buscar = new JButton();
		buscar.setText("Bus");
		buscar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e){
				SearchDialog dialog = new SearchDialog("Cliente", "Cliente");
				dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
				dialog.setVisible(true);
				
				cliente = (Cliente) dialog.result;
				nombre.setText(cliente.getApellidos() + " " + cliente.getNombres());
				codigo.setText(cliente.getCodigo());
				
			}
		});
		
		label = new JLabel();
		label.setText("Cliente");
		
		codigo = new JTextField();
		codigo.setText("");
		codigo.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				try {
					String code = e.getActionCommand();
					loadUI(code);
					general.setSelected(false);
				} catch(RepositoryException e1) {
					e1.printStackTrace();
				}
			}
		});
		
		nombre = new JLabel();
		nombre.setText("");
		
		general = new JCheckBox();
		general.setText("Cliente General");
		general.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				try {
					loadUI("general");
				} catch(RepositoryException e1) {
					e1.printStackTrace();
				}
			}
		});
		
		setLayout(new MigLayout("", "[][][][]", "[]"));
		
		add(label, "cell 0 0");
		add(codigo, "cell 1 0, width 50:200:");
		add(buscar, "cell 3 0,gapx unrelated");
		add(nombre, "cell 4 0, width 100:500:");
		add(general, "cell 1 1");
	}
	
	public ClientePanel() {
		initUI();
	}
	
	public void loadUI(String clientCode) throws RepositoryException 
	{
		
		
		if (clientCode == null || clientCode.equals("")) {
			throw new RuntimeException("no hat c"); 
		}
		 
		cliente = getClienteByCode(clientCode);
		nombre.setText(cliente.getApellidos() + " " + cliente.getNombres());
		
	}
	
	public Cliente getCliente() {
		return cliente;
	}
	
	public void clear() {
		codigo.setText("");

		//System.err.println("codigo es " + codigo.getText());
		nombre.setText("");
		cliente = null;
	}

	public void loadCliente(Cliente cliente2) {
		// TODO Auto-generated method stub
		cliente = cliente2;
		nombre.setText(cliente.getApellidos() + " " + cliente.getNombres());
		codigo.setText(cliente.getCodigo());
	}

}
