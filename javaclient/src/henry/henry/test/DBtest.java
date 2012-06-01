package henry.test;

import static org.junit.Assert.*;

import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;

import org.junit.Test;

import com.amazon.carbonado.ConfigurationException;
import com.amazon.carbonado.Cursor;
import com.amazon.carbonado.Query;
import com.amazon.carbonado.Repository;
import com.amazon.carbonado.RepositoryException;
import com.amazon.carbonado.Storage;
import java.sql.*;

import java.sql.Connection;

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
				Bodega.class,
				Descuento.class,
				Contenido.class
				
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
			Contenido cont = getStorableFor(Contenido.class);
	    	Query<Contenido> query = repo.storageFor(Contenido.class).query();
	    	Contenido cc = null;
	    	for (Cursor<Contenido> c = query.fetch(); c.hasNext(); ){
	    		cc = c.next();
	    		System.out.println(cc.getBodegaId());
	    		System.out.println(cc.getProdId());
	    	}
			cont.setBodegaId(cc.getBodegaId());
	    	cont.setProdId(cc.getProdId());
	    	cont.load();
	    	System.out.println(cont.getPrecio());
	    		
			}
		catch (Exception e) {
			e.printStackTrace();
			fail(e.getStackTrace().toString());
		}
		finally {
			repo.close();
		}
	}
	
	//@Test 
	public void javaDBTest() throws Exception {
		Connection con = null;
		String url = Config.getConfig().getConnection();
		String userid = "henry";
		String password = "no jodas";
		String query = "SELECT * FROM productos";
		String query2 = "select * from ordenes_de_despacho";

		try {
			con = DriverManager.getConnection(url,
				 userid, password);
			Statement stmt = con.createStatement();
			ResultSet set = stmt.executeQuery(query);
			while(set.next()) {
				System.out.println(set.getString("codigo") + " " + set.getString("nombre"));
			}
			
			set = stmt.executeQuery(query2);
			while(set.next()) {
				System.out.println(set.getString("codigo") + " " + set.getString("total"));
			}
			
			
			stmt.close();
		} catch(SQLException ex) {
			System.err.println("SQLException: " + ex.getMessage());
		}
		finally {
			con.close();
		}
		
		
	
	}
}
