package henry.common;

import static henry.common.Helper.*;
import java.util.ArrayList;
import com.amazon.carbonado.Storable;

import com.amazon.carbonado.Cursor;
import com.amazon.carbonado.Query;
import com.amazon.carbonado.RepositoryException;
import com.amazon.carbonado.Storage;

import henry.carbonadoObjects.MyRepository;
import henry.carbonadoObjects.Producto;

public class Searchable {
	
	public static final String CLIENTE = "apellidos >= ? & apellidos < ?";
	public static final String PRODUCTO = "nombre >= ? & nombre < ?";
	
	public <C extends Storable<C>> ArrayList<C> search(String arg, Class<C> dummy) {
		try {
			Storage<C> clientStg = MyRepository.getRepository()
                                               .storageFor(dummy);
			
			
			
			String next = nextString(arg);
			Query<C> result;
			if (dummy.equals(Producto.class))
				result = clientStg.query(PRODUCTO).with(arg).with(next);
			else 
				result = clientStg.query(CLIENTE).with(arg).with(next);
				
			
			ArrayList<C> list = new ArrayList<C>();
			for (Cursor<C> cur = result.fetch();
					cur.hasNext();) 
			{
				list.add(cur.next());
			}
			
			return list;
			
			
		} catch (RepositoryException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;

		}
	}

}
