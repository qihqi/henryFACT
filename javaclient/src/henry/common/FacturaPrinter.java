package henry.common;

import henry.carbonadoObjects.Cliente;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.print.PageFormat;
import java.awt.print.Printable;
import java.awt.print.PrinterException;
import java.awt.print.PrinterJob;
import java.math.BigDecimal;
import java.util.ArrayList;

import org.joda.time.DateTime;

public class FacturaPrinter implements Printable {

	private int totalPages;
	private int lines;
	
	private ArrayList<Item> items;
	private double [] spacing;
	
	private BigDecimal subtotal;
	private BigDecimal total;
	private BigDecimal iva;
	private Cliente client;
	
	class Item {
		public String cod;
		public int cant;
		public String desc;
		public BigDecimal total;
		public Item(String cod, int cant, String desc, BigDecimal total) {
			this.cod = cod;
			this.cant = cant;
			this.desc = desc;
			this.total = total;
		}
	}
	
	
	public FacturaPrinter(ArrayList<ItemPanel> items_, 
			              BigDecimal subt, 
			              BigDecimal tot,
			              Cliente c) 
	{
		lines = Config.getConfig().getLinesPerFactura();
		spacing = Config.getConfig().getContenidoSpacing();
		
		totalPages = ((items_.size() - 1) / lines) + 1;
	
		items = new ArrayList<Item>(); 
		
		//TODO not sure if deep copy is really necesary
		for (ItemPanel p : items_) {
			if (p.getProd() != null)
				this.items.add(
					new Item(p.getProd().getCodigo(),
							 p.getCantidad(),
							 p.getProd().getNombre(),
							 p.getTotal()
		            ));
		}
		
		subtotal = subt; 
		total = tot;
		iva = total.subtract(subtotal);
		
		client = c.copy();
		
	}
	
	public void printFactura() {
		PrinterJob job = PrinterJob.getPrinterJob();
		job.setPrintable(this);
		boolean ok = job.printDialog();
		if (ok) {
			try {
				job.print();
			} catch (PrinterException e) {
				e.printStackTrace();
			}
		}
	}
	
	@Override
	public int print(Graphics g, PageFormat fmt, int page)
			throws PrinterException 
	{
		if (page > totalPages )
			return NO_SUCH_PAGE;
	
		
		int lineWidth = g.getFontMetrics().getHeight();
		Graphics2D g2d = (Graphics2D)g;
        g2d.translate(fmt.getImageableX(), fmt.getImageableY());
		
        printClient(g2d);
        printContent(g2d, page, lineWidth);
        printValues(g2d);
        
       
		return PAGE_EXISTS;
	}
	
	private void printClient(Graphics2D g2d) {
		String [] titles = {"ruc", 
				            "cliente", 
				            "telf", 
				            "direccion",
				            "fecha",
				            //"remision",
		                    };
		
		for (String s : titles) {
			double [] pos = Config.getConfig().getImpresionPos(s);
			String value = null;
			if (s.equals("ruc"))
				value = client.getCodigo();
			else if (s.equals("cliente"))
				value = client.getApellidos() + " " + client.getNombres();
			else if (s.equals("telf"))
				value = client.getTelefono();
			else if (s.equals("direccion"))
				value = client.getDireccion();
			else if (s.equals("fecha"))
				value = DateTime.now().toDate().toString();
			
			if (value == null)
				value = "";
			
			g2d.drawString(value, (float) pos[0], (float) pos[1]);
		}
	}
	private void printContent(Graphics2D g2d, int page, int lineWidth) {
		int start = page * lines;
				
		int end = (start + lines > items.size()) ? items.size() : (start + lines);
		
		double [] pos = Config.getConfig().getImpresionPos("contenido");
		
		final double LEFT_EDGE = pos[0];
		
		for (int i = start; i < end; i++) {
			for (int j = 0; j < 4; j++) {
				g2d.drawString(getItemValue(j, items.get(i)), 
						       (float) pos[0], (float) pos[1]);
				pos[0] += spacing[0];
			}
			pos[0] = LEFT_EDGE;
			pos[1] += lineWidth;
		}
	}
	
	private static String getItemValue(int pos, Item v) {
		switch (pos) {
		case 0:
			return v.cod;
		case 1:
			return "" + v.cant;
		case 2:
			return v.desc;
		case 3:
			return v.total.toString();
		}
		return null;
	}
	
	private void printValues(Graphics2D g2d) {
		String [] titles = { "bruto", "neto", "iva", "total" };
		String [] values = { subtotal.toString(), subtotal.toString(),
				             iva.toString(), total.toString()};
		for (int i = 0; i < titles.length; i++) {
			double [] pos = Config.getConfig().getImpresionPos(titles[i]);
			g2d.drawString(values[i], (float) pos[0], (float) pos[1]); 
		}
		
	}
}
