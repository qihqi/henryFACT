package henry.test;

import static org.junit.Assert.*;

import org.junit.Test;

import com.amazon.carbonado.ConfigurationException;
import com.amazon.carbonado.Cursor;
import com.amazon.carbonado.Query;
import com.amazon.carbonado.Repository;
import com.amazon.carbonado.RepositoryException;

import henry.carbonadoObjects.*;
import henry.common.Config;
import static henry.common.Helper.*;

public class DBtest {

	@Test
	public void test() throws RepositoryException {
		Config.bootstrap();
		Repository repo = MyRepository.getRepository();
		Class [] tests = { 
				Cliente.class,
				Factura.class,
				ItemFactura.class,
				ItemVenta.class,
				NotaDeVenta.class,
				Producto.class,
				Usuario.class,
				Contenido.class,
				Bodega.class
				
		};
		try {
			for (Class c : tests) {
				repo.storageFor(c);
			}
		} catch(Exception e) {
			e.printStackTrace();
			fail(e.getStackTrace().toString());
		}
		finally {
			//repo.close();
		}
		
	
	}
	
	@Test
	public void loadContentTest() throws RepositoryException {
		Config.bootstrap();
		Repository repo = MyRepository.getRepository();
		try { 
			
			ItemVenta fa = getStorableFor(ItemVenta.class);
			fa.setCodigoVenta(7);
			fa.setItemNo(0);
		//	fa.load();
			System.out.println(fa);
			
			Query<Contenido> q = repo.storageFor(Contenido.class)
					                 .query("bodegaId=? & prodId=?").with(1).with("00");
			Cursor<Contenido> cur = q.fetch();
			while (cur.hasNext()) {
				System.out.println("mira " + cur.next());
			}
			
			Contenido c = getStorableFor(Contenido.class);
			//c.setId(1);
			c.setBodegaId(1);
			c.setProdId("00");
			
			System.out.println(c);
			c.load();
		}
		catch (Exception e) {
			e.printStackTrace();
			fail(e.getStackTrace().toString());
		}
		finally {
			repo.close();
		}
	}
	

}
