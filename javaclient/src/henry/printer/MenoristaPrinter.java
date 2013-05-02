package henry.printer;

import henry.carbonadoObjects.Cliente;
import henry.common.Config;
import henry.common.ItemPanel;

import java.math.BigDecimal;
import java.util.ArrayList;
import javax.print.Doc;
import javax.print.DocFlavor;
import javax.print.DocPrintJob;
import javax.print.PrintException;
import javax.print.PrintService;
import javax.print.PrintServiceLookup;
import javax.print.SimpleDoc;

import org.joda.time.DateTime;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;

public class MenoristaPrinter extends GenericPrinter {

	private int lines;
	
	private ArrayList<Item> items;
	private double [] spacing;
	
	private BigDecimal subtotal;
	private BigDecimal total;
	private BigDecimal desc;
	
	private Cliente client;
    
    private boolean facturaBlanco;
    private char [][] data;
    
	public class Item {
		public String cod;
		public BigDecimal cant;
		public String desc;
		public BigDecimal total;
		public BigDecimal precio;
		public boolean modificado;
		public Item(String cod, BigDecimal cant, 
				    String desc, BigDecimal precio, 
				    BigDecimal total, boolean modificado) {
			this.cod = cod;
			this.cant = cant;
			this.desc = desc;
			this.precio = precio;
			this.total = total;
			this.modificado = modificado;
		}
	}
	
	
	public MenoristaPrinter(ArrayList<ItemPanel> items_, 
			              BigDecimal subt, 
			              BigDecimal tot,
			              BigDecimal descuento,
			              Cliente c,
			              long codigo_) 
	{
		lines = Config.getConfig().getLinesPerFactura();
		spacing = Config.getConfig().getContenidoSpacing();
			
		items = new ArrayList<Item>(); 
		
		//TODO not sure if deep copy is really necesary
		for (ItemPanel p : items_) {
			if (p.getProdCont() != null)
				this.items.add(
					new Item(p.getProdCont().getProdId(),
							 p.getCantidad(),
							 p.getNombreProd(),
							 p.getPrecio(),
							 p.getTotal(),
							 p.precioModificado()
		            ));
		}
		
		subtotal = subt; 
		total = tot;
		desc = descuento;
		client = c.copy();

        facturaBlanco = Config.getConfig().getFacturaBlanco();
        Config.getConfig().getLibre();
        
        double [] pos = Config.getConfig().getImpresionPos("tamano");
        data = new char[(int) pos[1]][(int) pos[0]];
	}
	
	@Override
	public void printFactura() {
		PrintService defaultprinter = PrintServiceLookup.lookupDefaultPrintService();  
        DocPrintJob job = defaultprinter.createPrintJob();  
        DocFlavor  flavour = DocFlavor.BYTE_ARRAY.AUTOSENSE;  

        byte[] b = makePrintBytes();  

        Doc doc = new SimpleDoc( b, flavour, null);  
        try {  
                job.print(doc, null);  
        } catch (PrintException e1) {  
                // TODO Auto-generated catch block  
                e1.printStackTrace();  
        }  
	}
	
	private void initialize() {
		for (int i = 0; i < data.length; i++)
			for (int j = 0; j < data[i].length;j ++) 
				data[i][j] = ' ';
	}
	
	private byte[] makePrintBytes() {
		String content = "";
		initialize();
		printClient();
		printContent();
		printValues();
		
		for (char [] c : data) {
			content += new String(c);
			content += '\n';
		}
		
		//System.out.println(content);
		
		return content.getBytes();
	}

	
	
	private void printClient() {
		String [] titles = {"ruc", 
				            "cliente", 
				            "telf", 
				            "direccion",
				            "fecha",
				            //"remision",
		                    };
		
		for (String s : titles) {
			double [] pos = Config.getConfig().getImpresionPos(s);
			int x = (int) pos[0];
			int y = (int) pos[1];
			char [] content = getHeaderValue(s).toCharArray();
			printToData(content, x, y);
		}
		
		
	}
	private String shorterName(String name, String last) {
		if (name != null && !name.replaceAll("\\s", "").equals(""))
		// name is not empty. assume its a ppl name
		{
			return last.split("[ ]+")[0] + " " + name.split("[ ]+")[0];
		}
		else
			return last;
	}
	private String getHeaderValue(String s) {
		String value = null;
		if (s.equals("ruc"))
			value = client.getCodigo();
		else if (s.equals("cliente")) {
			 value = client.getApellidos() + " " + client.getNombres();
			if (value.length() > Config.getConfig().getMaxCliente())
				value = shorterName(client.getApellidos(), client.getNombres());
		}
		else if (s.equals("telf"))
			value = client.getTelefono();
		else if (s.equals("direccion")){
			value = client.getDireccion();
			if (value == null)
				value = "";
			if (value.length() > 20)
				value = value.substring(0, 20);
		}
		else if (s.equals("fecha")) {
			DateTimeFormatter fmt = DateTimeFormat.forPattern("yyyy-MM-dd");
			value = fmt.print(DateTime.now());
		} 
		else {
			System.out.println("fail");
		}
		if (value == null) 
			value = "";
		return value;
	}
	private void printContent() {
		int start = 0;
		int end = lines;
	
		if (end > items.size()) 
			end = items.size();
		double [] pos = Config.getConfig().getImpresionPos("contenido");
		
		final int LEFT_EDGE = (int) pos[0];
		for (int i = start; i < end; i++) {
			for (int j = 0; j < 5; j++) {
				int x = (int) pos[0];
				int y = (int) pos[1];
				char [] content = getItemValue(j, items.get(i)).toCharArray();
				printToData(content, x, y);
				if (j < 4)
					pos[0] += spacing[j];
			}
			pos[0] = LEFT_EDGE;
			pos[1] += 1;
			
		}
	}
	
	private static String getItemValue(int pos, Item v) {
		switch (pos) {
		case 0:
			if (v.cod.length() >= 6)
				return v.cod.substring(0, 6);
			else 
				return v.cod;
		case 1:
			return v.cant.setScale(1, BigDecimal.ROUND_HALF_UP).toString();
		case 2:
			if (v.desc.length() > Config.getConfig().getMaxDesc())
				return shorten(v.desc);
			return v.desc;
		case 3:
			if (v.modificado)
				return v.precio.toString() + "*";
			else
				return v.precio.toString();
		case 4:
			return v.total.toString();
		}
		return null;
	}
	
	private static String shorten(String s) {
		String [] words = s.split("[ ]+");
		String result = "";
		for (String w : words) {
			if (w.length() > 4)
				result += w.substring(0, 3);
			else 
				result += w;
			result += ' ';
	}
		return result;
	}
	
	private void printValues() {
		String [] titles = { "bruto", "neto", "desc", "iva", "total" };
		String [] values = { subtotal.add(desc).toString(), //valor bruto = neto + desc 
				             subtotal.toString(),
				             desc.toString(),
				             total.subtract(subtotal).toString(), //iva = total - subtotal
				             total.toString()};
		
		
		for (int i = 0; i < titles.length; i++) {
			double [] pos;
			pos = Config.getConfig().getImpresionPos(titles[i]);
			int x = (int) pos[0];
			int y = (int) pos[1];
			char [] content = values[i].toCharArray();
			printToData(content, x, y);
			 
		}
	}
	
	private void printToData(char [] content, int x, int y) {
		if ( y >= data.length)
			y = data.length - 1;
		int length = ( content.length + x >= data[y].length) ? 
				      data[y].length - x - 1 : content.length;
		
	    //System.out.println(new String(content) + "   " + new String(data[y]));
		System.arraycopy(content, 0, data[y], x, length);
	}
	
	
}