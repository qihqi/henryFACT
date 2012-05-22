package henry.common;

import henry.carbonadoObjects.MyRepository;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import org.xml.sax.SAXException;

import com.amazon.carbonado.RepositoryException;

import java.io.File;
import java.io.IOException;

/**
 * Esta clase es un parser de configuraciones
 * @author han
 *
 */
public final class Config {
	
	private Boolean isFactura;
	private String connection;
	private String user;
	//final string password 
	private String password = "no jodas";
	private String dbName;
	private String bodega;
	
	private Node printNode; 
	
	
	
	static private Config config = null;
	
	private Config(/*String filename*/) 
			throws ParserConfigurationException, SAXException, IOException 
	{

		File fXmlFile = new File("config.xml");
		DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
		DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
		Document doc = dBuilder.parse(fXmlFile);
		doc.getDocumentElement().normalize();
		
		System.out.println("Root element :" + doc.getDocumentElement().getNodeName());
		Node nList = doc.getElementsByTagName("config").item(0);
		System.out.println("-----------------------");
		
		connection = getTagValue("database", (Element) nList);
		user = getTagValue("usuario", (Element) nList);
		isFactura = new Boolean(getTagValue("factura", (Element) nList));
		bodega = getTagValue("bodega", (Element) nList);
		dbName = getTagValue("databasename", (Element) nList);
		//System.out.println(connection + user + isFactura);
		
		//cargar impresion
		printNode = doc.getElementsByTagName("impresion").item(0);
	
	}
	
	public static void bootstrap() throws RepositoryException {
		getConfig();
		MyRepository.setDbName(config.getDBName());
		MyRepository.setURL(config.getConnection());
		MyRepository.setPassword(config.getPassword());
		MyRepository.setUser(config.getDBUser());
		MyRepository.getRepository();
	}
	
	public static Config getConfig() {
		try {
		  	allocate();
		  }catch (Exception e) {
		  	return null;
		  }
		return config;
	}
	 
	  private static String getTagValue(String sTag, Element eElement) {
		NodeList nlList = eElement.getElementsByTagName(sTag).item(0).getChildNodes();
	 
	    Node nValue = (Node) nlList.item(0);
	 
		return nValue.getNodeValue();
	  }
	
	  private static void allocate() 
			  throws ParserConfigurationException, SAXException, IOException
	 {
		  if (config == null)
			  config = new Config();
	 }
	
	  public String getConnection() {
		  try {
		  	allocate();
		  }catch (Exception e) {
		  	return null;
		  }
		  return "jdbc:mysql://" + connection + "/" + dbName;
	  }
	  
	  public Boolean isFactura() {
		  try {
		  	allocate();
		  }catch (Exception e) {
		  	return null;
		  }
		  return isFactura;
	  }
	  public String getPassword() {
		  return password;
	  }
	  public String getDBUser() {
		  try {
		  	allocate();
		  }catch (Exception e) {
		  	return null;
		  }
		  return user;
	  }
	  
	  public String getBodega() {
		  try {
		  	allocate();
		  }catch (Exception e) {
		  	return null;
		  }
		  return bodega;
	  }
	  public String getDBName() {
		  try {
		  	allocate();
		  }catch (Exception e) {
		  	return null;
		  }
		  return dbName;
	  }
	  
	  public static void main(String [] s) throws Exception { 
		//new Config();
		  double [] res = Config.getConfig().getContenidoSpacing();
		 System.out.printf("%f, %f, %f", res[0], res[1], res[2]);
		 System.out.println(Config.getConfig().getLinesPerFactura());
	  }
	  
	
	  double [] getImpresionPos(String s) {
   		Node node = ((Element) printNode)
				   .getElementsByTagName(s).item(0);
   		  
   		double x =  Double.parseDouble(getTagValue("x", (Element) node));
   		double y =  Double.parseDouble(getTagValue("y", (Element) node));
   			  
   		return makePos(x, y);
	  }
	  
	  double [] getContenidoSpacing() {
			Node node = ((Element) printNode)
					   .getElementsByTagName("contenido").item(0);
			
			NodeList nlList = ((Element) node)
					           .getElementsByTagName("sp");
			 
		    double [] res = new double [4];
		    for (int i = 0; i < 4; i++) {
		    	String value = nlList.item(i).getChildNodes().item(0).getNodeValue();
		    	res[i] = Double.parseDouble(value);
		    }
		    return res;
			
	  }
	  double getContenidoVsp() {
		  return 0;
	  }
	  
	  int getLinesPerFactura() {
			
	   		return Integer.parseInt(getTagValue("lineas", (Element) printNode));
	  }
	  
	  double [] makePos(double x, double y) {
		  double [] pos = new double[2];
		  pos[0] = x;
		  pos[1] = y;
		  return pos;
	  }
	
}
