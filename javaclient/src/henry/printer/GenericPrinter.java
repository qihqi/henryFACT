package henry.printer;

import henry.carbonadoObjects.Cliente;
import henry.common.Config;
import henry.common.ItemPanel;

import java.math.BigDecimal;
import java.util.ArrayList;

public abstract class GenericPrinter {

	public abstract void printFactura();

	public static GenericPrinter makePrinter(ArrayList<ItemPanel> items,
			BigDecimal subtotal, BigDecimal total, BigDecimal descuento,
			Cliente cliente, long codigo)
	{
		if (Config.getConfig().getFacturaBlanco()) {
			return new FacturaPrinter(items,
				                  subtotal, 
				                  total,
				                  descuento,
				                  cliente, 
				                  codigo);
		}
		else {

			return new MenoristaPrinter(items,
			                  subtotal, 
			                  total,
			                  descuento,
			                  cliente, 
			                  codigo);
		}
	}

}