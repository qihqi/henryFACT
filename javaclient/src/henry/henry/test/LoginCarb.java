package henry.test;

import com.amazon.carbonado.RepositoryException;

import henry.carbonadoObjects.MyRepository;
import henry.common.Config;
import henry.common.Helper;

public class LoginCarb {

		public static void main(String [] s) throws RepositoryException {
			Config.bootstrap();
			henry.carbonadoObjects.Usuario u = Helper.getUsuario("hola");
			System.out.println(u.getPassword());
			MyRepository.close();
		
		}

}
