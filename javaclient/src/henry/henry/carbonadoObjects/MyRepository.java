package henry.carbonadoObjects;

import com.amazon.carbonado.repo.jdbc.JDBCRepositoryBuilder;
import com.amazon.carbonado.Repository;
import com.amazon.carbonado.ConfigurationException;
import com.amazon.carbonado.RepositoryException;
import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;

public class MyRepository {
    
    private static Repository repo = null;
    
    private static String URL = null;
    private static String user = null;
    private static String password = null;
    private static String dbName = null;
    
    public static Repository getRepository() 
        throws ConfigurationException,
               RepositoryException
    {
    	
    	
        if (repo == null) {
        
        	if (URL == null ||
        	    user == null ||
        		password == null ||
        		dbName == null)
        	{
        		System.err.println(URL + " " + user + password + " " + dbName);
        		throw new ConfigurationException("unset parameters");
        	}
        	
        	JDBCRepositoryBuilder builder = new JDBCRepositoryBuilder();

            MysqlDataSource source = new MysqlDataSource();
            source.setURL(URL); //"jdbc:mysql://localhost/henry"
            System.out.println(URL);
            
            source.setUser(user);
            source.setPassword(password);
                
            builder.setDataSource(source);
            builder.setName(dbName);
            repo = builder.build();
        }
        
        return repo;
    }

    public static void close() {
        if (repo != null)
            repo.close();
    }

	public static void setURL(String URL) {
		MyRepository.URL = URL;
	}

	public static void setUser(String user) {
		MyRepository.user = user;
	}

	public static void setPassword(String password) {
		MyRepository.password = password;
	}

	public static void setDbName(String dbName) {
		MyRepository.dbName = dbName;
	}
}
