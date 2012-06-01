package henry.common;

import henry.carbonadoObjects.Cliente;

import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.print.Book;
import java.awt.print.PageFormat;
import java.awt.print.Paper;
import java.awt.print.Printable;
import java.awt.print.PrinterException;
import java.awt.print.PrinterJob;
import java.math.BigDecimal;
import java.util.ArrayList;

import org.joda.time.DateTime;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;

public class FacturaPrinter implements Printable {

	private int totalPages;
	private int lines;
	
	private ArrayList<Item> items;
	private double [] spacing;
	
	private BigDecimal subtotal;
	private BigDecimal total;
	private BigDecimal desc;
	
	private Cliente client;
	
	class Item {
		public String cod;
		public int cant;
		public String desc;
		public BigDecimal total;
		public BigDecimal precio;
		public boolean modificado;
		public Item(String cod, int cant, 
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
	
	
	public FacturaPrinter(ArrayList<ItemPanel> items_, 
			              BigDecimal subt, 
			              BigDecimal tot,
			              BigDecimal descuento,
			              Cliente c) 
	{
		lines = Config.getConfig().getLinesPerFactura();
		spacing = Config.getConfig().getContenidoSpacing();
		
		totalPages = ((items_.size() - 1) / lines) + 1;
	
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
		
	}
	
	public void printFactura() {
		PrinterJob job = PrinterJob.getPrinterJob();
		job.setPrintable(this);
		boolean ok = job.printDialog();
		if (ok) {
			try {
				setPaperSize(job);
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
		if (page >= totalPages ) //>= porq es 0 indexed
			return NO_SUCH_PAGE;
		
		
		Font font = new Font(Config.getConfig().getFontFamily(),
				             Font.PLAIN, 
				             Config.getConfig().getFontSize());
		
		g.setFont(font);
		int lineWidth = g.getFontMetrics(font).getHeight();
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
			else if (s.equals("fecha")) {
				DateTimeFormatter fmt = DateTimeFormat.forPattern("dd/MM/yy");
				value = fmt.print(DateTime.now());
			}
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
		System.out.println(lineWidth);
		for (int i = start; i < end; i++) {
			for (int j = 0; j < 5; j++) {
				g2d.drawString(getItemValue(j, items.get(i)), 
						       (float) pos[0], (float) pos[1]);
				if (j < 4)
					pos[0] += spacing[j];
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
			if (v.modificado)
				return v.precio.toString() + "*";
			else
				return v.precio.toString();
		case 4:
			return v.total.toString();
		}
		return null;
	}
	
	private void printValues(Graphics2D g2d) {
		String [] titles = { "bruto", "neto", "desc", "iva", "total" };
		String [] values = { subtotal.subtract(desc).toString(), //valor bruto = neto - desc 
				             subtotal.toString(),
				             desc.toString(), subtotal.toString(), 
				             total.subtract(subtotal).toString(), //iva = total - subtotal
				             total.toString()};
		for (int i = 0; i < titles.length; i++) {
			double [] pos = Config.getConfig().getImpresionPos(titles[i]);
			g2d.drawString(values[i], (float) pos[0], (float) pos[1]); 
		}
		
	}
	
	public void setPaperSize(PrinterJob job) {
		double [] size = Config.getConfig().getImpresionPos("tamano");
		PageFormat fmt = job.defaultPage();
		Paper paper = fmt.getPaper();
		paper.setImageableArea(0, 0, (float) size[0], size[1]);
		fmt.setPaper(paper);
		//fmt = job.pageDialog(fmt);
		Book book = new Book();
		book.append(this, fmt);
		job.setPageable(book);
	
	}
}
