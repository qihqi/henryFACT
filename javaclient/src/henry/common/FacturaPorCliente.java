package henry.common;

import henry.carbonadoObjects.MyRepository;
import henry.carbonadoObjects.NotaDeVenta;
import static henry.common.Helper.*;

import java.awt.BorderLayout;
import java.awt.Dialog;
import java.awt.FlowLayout;
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

import com.amazon.carbonado.Cursor;
import com.amazon.carbonado.Query;
import com.amazon.carbonado.RepositoryException;
import com.amazon.carbonado.Storage;
import org.joda.time.DateTime;
import net.miginfocom.swing.MigLayout;

@SuppressWarnings("serial")
public class FacturaPorCliente extends JDialog {

	private final JPanel contentPanel = new JPanel();
	private JTextField searchInput;
	private DefaultListModel listContent;
	private JList display;
	
	ArrayList<NotaDeVenta> resultList;
	NotaDeVenta result;
	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		try {
			Config.bootstrap();
			FacturaPorCliente dialog = new FacturaPorCliente();
			dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
			dialog.setVisible(true);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * Create the dialog.
	 */
	public FacturaPorCliente() {
		super(null, Dialog.ModalityType.DOCUMENT_MODAL);
		initUI();
	}
	
	public void initUI() {
		setBounds(100, 100, 547, 543);

		getContentPane().setLayout(new BorderLayout());
		contentPanel.setLayout(new MigLayout());
		
		
		getContentPane().add(contentPanel, BorderLayout.CENTER);
	
		JLabel lblNewLabel = new JLabel("Apellidos");
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
				if (resultList.isEmpty()) {
					return;
				}
				System.err.println(display.getSelectedIndex() + " " + resultList.size());
				
				result = resultList.get(display.getSelectedIndex());
				System.err.println(result);
				dispose();
			}
		});
		contentPanel.add(new JScrollPane(display), "span, width :456:");

		
		searchInput.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				//do the search
				String criterium = e.getActionCommand();
				listContent.clear();

				try {
					resultList = buscar(criterium);
					if (resultList.isEmpty()){
						listContent.addElement("No ha podido encontrar la nota de pedido");
					}
					
					for (NotaDeVenta n : resultList) {
						listContent.addElement(n.getCodigo() + " " 
					                           + n.getCliente().getApellidos());
					}
				} catch (RepositoryException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
				
			}
		});
		
		JPanel buttonPane = new JPanel();
		buttonPane.setLayout(new FlowLayout(FlowLayout.RIGHT));
		getContentPane().add(buttonPane, BorderLayout.SOUTH);
		
	}
	
	ArrayList<NotaDeVenta> buscar(String apellidos) 
			throws RepositoryException
	{
		Storage<NotaDeVenta> notaStg = MyRepository.getRepository()
				                                 .storageFor(NotaDeVenta.class);
		
		String queryString = "cliente.apellidos >= ? & cliente.apellidos < ? " +
				             "& fecha >= ? & fecha < ?";
		DateTime today = DateTime.now().withTime(0,0,0,0);
		DateTime tomorrow = today.plusDays(1);
		Query<NotaDeVenta> notas = notaStg.query(queryString)
				                          .with(apellidos)
				                          .with(nextString(apellidos))
				                          .with(today)
				                          .with(tomorrow);
		ArrayList<NotaDeVenta> results = new ArrayList<NotaDeVenta>();
		for (Cursor<NotaDeVenta> cur = notas.fetch();
				cur.hasNext();)
		{
			results.add(cur.next());
		}
		return results;
	}
}
