import com.amazon.carbonado.repo.jdbc.JDBCRepositoryBuilder;
import com.amazon.carbonado.Repository;
import com.amazon.carbonado.ConfigurationException;
import com.amazon.carbonado.RepositoryException;
import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;

public class Test {
    private static String [] endpoints = {"localhost"};

    private static final String URL_PATTERN = "jdbc:mysql://%s/henry";

    private static Repository getRepository(String endpoint, String user, String password) throws Exception {
        String url = String.format(URL_PATTERN, endpoint);
        System.err.println(URL_PATTERN);
        System.err.println(url);
        JDBCRepositoryBuilder builder = new JDBCRepositoryBuilder();
        MysqlDataSource source = new MysqlDataSource();

        source.setURL(url); //"jdbc:mysql://localhost/henry"
        source.setUser(user);
        source.setPassword(password);

        builder.setDataSource(source);
        builder.setName(endpoint);
        Repository repo = builder.build();
        return repo;
    }
    
    private static void getProduct() {

    }

    public static void main(String [] s) {
        String user = "root";
        String password = "";

        for (String endpoint : endpoints) {
            Repository r = null;
            try {
                long start = System.nanoTime();
                r = getRepository(endpoint, user, password);
                long end = System.nanoTime();
                System.out.println(String.format("Host %s: %.3f milli", endpoint, (end - start) / 1000000.0f));
            } 
            catch (Exception e) {
                e.printStackTrace();
            }
            finally {
                if (r != null) {
                    r.close();
                }
            }
        }
    }
}


