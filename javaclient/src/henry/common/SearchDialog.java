package henry.common;

import henry.carbonadoObjects.Cliente;
import henry.carbonadoObjects.Producto;

import java.awt.BorderLayout;
import java.awt.Dialog;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import javax.swing.DefaultListModel;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.ListSelectionModel;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import com.amazon.carbonado.Storable;

import net.miginfocom.swing.MigLayout;

@SuppressWarnings("serial")
public class SearchDialog extends JDialog {


	
	
	//TextArea for searching
	private JTextField searchInput;
	private JList display;
	private DefaultListModel listContent; 
	
	public Object result;
	
	private String searchType;
	private Searchable engine; 
	
	ArrayList<? extends Storable<?>> resultList;
	/**
	 * Launch the application.
	 */

	private final JPanel contentPanel = new JPanel();

	/**
	 * Launch the application.
	 */
	static class Box {
		public Object obj;
	}
	public static void main(String[] args) {
		try {
			Config.bootstrap();

			final Box box = new Box();
			
			SearchDialog dialog = new SearchDialog("Producto", "Producto");
			dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
			dialog.setVisible(true);
			
			System.err.println( ((Producto) box.obj).getNombre());
			

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * Create the dialog.
	 */
	public SearchDialog(String s, String type) {
		super(null, Dialog.ModalityType.APPLICATION_MODAL);
		searchType = type;
		engine = new Searchable();
		initUI(s);
	}
	public void initUI(String s) {
		setBounds(100, 100, 502, 255);

		getContentPane().setLayout(new BorderLayout());
		contentPanel.setLayout(new MigLayout());
		
		
		getContentPane().add(contentPanel, BorderLayout.CENTER);
	
		JLabel lblNewLabel = new JLabel(s);
		lblNewLabel.setFont(new Font("Dialog", Font.BOLD, 13));
		contentPanel.add(lblNewLabel);

		searchInput = new JTextField();
		contentPanel.add(searchInput, "wrap, width :400:");
		
		listContent = new DefaultListModel();
		display = new JList(listContent);
		display.setVisibleRowCount(10);
		display.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);

		display.addListSelectionListener(new ListSelectionListener() {
			@Override
			public void valueChanged(ListSelectionEvent e) {
				if (resultList.isEmpty())
					return;
				result = resultList.get(display.getSelectedIndex());
				dispose();
			}
		});
		contentPanel.add(new JScrollPane(display), "span, width :456:");

		
		searchInput.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String criteria = e.getActionCommand();
				
				listContent.clear();
				if (searchType.equals("Cliente")) {
					ArrayList<Cliente> list = engine.search(criteria, Cliente.class);
					listContent.clear();
					
					if (list.isEmpty()) 
						listContent.addElement("No ha podido encontrar el cliente");
					
					for ( Cliente c : list) {
						listContent.addElement(c.getApellidos() + " " + c.getNombres());
					}
					resultList = list;
				}
				else if (searchType.equals("Producto")) {
					ArrayList<Producto> list = engine.search(criteria, Producto.class);
					listContent.clear();
					
					if (list.isEmpty()) 
						listContent.addElement("No ha podido encontrar el producto");
					
					for ( Producto c : list) {
						listContent.addElement(c.getNombre());
					}
					resultList = list;
				}
			}
		});
		
		


	
	}

}
