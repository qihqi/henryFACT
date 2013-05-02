package henry.common;

import henry.carbonadoObjects.Descuento;
import henry.carbonadoObjects.MyRepository;
import static henry.common.Helper.*;

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
	private Boolean facturaBlanco;
	private String connection;
	private String user;
	//final string password 
	private String password = "";
	private String dbName;
	private String bodega;
	private String libre;
	private String fontFamily;
	private int fontSize;
	private double [] disp; //displacement
	
	private Node printNode; 
	
	private int descuentoDesde = -1;
	private int globalDesc = -1;
	private int maxDesc;
	private int maxCliente;
	
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
		facturaBlanco = new Boolean(getTagValue("factura_blanco", (Element) nList));
		bodega = getTagValue("bodega", (Element) nList);
		dbName = getTagValue("databasename", (Element) nList);
		libre = getTagValue("libre", (Element) nList);
		
		fontSize = Integer.parseInt(getTagValue("fontsize", (Element) nList));
		fontFamily = getTagValue("fontfamily", (Element) nList);
		//System.out.println(connection + user + isFactura);
		
		//cargar impresion
		printNode = doc.getElementsByTagName("impresion").item(0);
		disp = getRawImpresionPos("disp");
		
		maxDesc = Integer.parseInt(getTagValue("max_desc", (Element) nList));
		maxCliente = Integer.parseInt(getTagValue("max_cliente", (Element) nList));
		
		
		}
	
	public static void bootstrap() throws RepositoryException {
		getConfig();
		MyRepository.setDbName(config.getDBName());
		MyRepository.setURL(config.getConnection());
		MyRepository.setPassword(config.getPassword());
		MyRepository.setUser(config.getDBUser());
		MyRepository.getRepository();
	}
	/*
	public static void bootstrap2() throws SQLException {
		getConfig();
		henry.beans.MyRepository.setDbName(config.getDBName());
		henry.beans.MyRepository.setURL(config.getConnection());
		henry.beans.MyRepository.setPassword(config.getPassword());
		henry.beans.MyRepository.setUser(config.getDBUser());
		henry.beans.MyRepository.getConnection();
	}*/
	
	public static Config getConfig() {
		try {
		  	allocate();
		  }catch (Exception e) {
			   e.printStackTrace();
			  
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
	
	  public float getLibre() {
		  try {
		  	allocate();
            return Float.parseFloat(libre);
		  }catch (Exception e) {
		  	return 0;
		  }
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
	  public boolean getFacturaBlanco() {
		  try {
		  	allocate();
		  }catch (Exception e) {
		  	return false;
		  }
		  return facturaBlanco.booleanValue();
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
		 double [] res = Config.getConfig().getImpresionPos("title");
		 System.out.printf("%f, %f", res[0], res[1]);
		 System.out.println(Config.getConfig().getLinesPerFactura());
	  }
	  
	
	  public double [] getImpresionPos(String s) {
		  double [] pos = getRawImpresionPos(s);
		  pos[0] += disp[0];
		  pos[1] += disp[1];
		  return pos;
	  }
	  
	  public double [] getRawImpresionPos(String s) {
	   		Node node = ((Element) printNode)
					   .getElementsByTagName(s).item(0);
	   		  
	   		double x =  Double.parseDouble(getTagValue("x", (Element) node));
	   		double y =  Double.parseDouble(getTagValue("y", (Element) node));
	   			  
	   		return makePos(x, y);
	  }
	  
	  
	  public  double [] getContenidoSpacing() {
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
	  public double getContenidoVsp() {
		  return 0;
	  }
	  
	  public int getLinesPerFactura() {
			
	   		return Integer.parseInt(getTagValue("lineas", (Element) printNode));
	  }
	  
	  public double [] makePos(double x, double y) {
		  double [] pos = new double[2];
		  pos[0] = x;
		  pos[1] = y;
		  return pos;
	  }
	  
	  public int getFontSize() {
		  return fontSize;
	  }
	  
	  public String getFontFamily() {
		  return fontFamily;
	  }
	  
	  public int getGlobalDesc() {
		  if (globalDesc < 0)
			  globalDesc = getDescuentoProperty("global");
	  
		  return globalDesc;
	  }
	  
	  public int getDescCount() {
		  if (descuentoDesde < 0)
			  descuentoDesde = getDescuentoProperty("descuento_desde");
		  if (descuentoDesde == 0)
			  return Integer.MAX_VALUE;
		  
		  return descuentoDesde;
	  }
	  
	public int getDescuentoProperty(String s) {
		  try {
			  Descuento desc = getStorableFor(Descuento.class); 
			  desc.setParam(s);
			  desc.load();
			  Integer val = desc.getValue();
			  if (val != null) {
				  int value = val.intValue();
				  if (value >= 0 )
					  return value;
			  }
		  }
		  catch (Exception e) {
			  return 0;
		  }
		  return 0;
	  }

	public int getMaxDesc() {
		// TODO Auto-generated method stub
		return maxDesc;
	}
	public int getMaxCliente() {
		return maxCliente;
	}
	  
}
