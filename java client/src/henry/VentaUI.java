package henry;

import org.eclipse.swt.SWT;
import org.eclipse.swt.events.KeyAdapter;
import org.eclipse.swt.events.KeyEvent;
import org.eclipse.swt.events.MouseAdapter;
import org.eclipse.swt.events.MouseEvent;
import org.eclipse.swt.layout.FormAttachment;
import org.eclipse.swt.layout.FormData;
import org.eclipse.swt.layout.FormLayout;
import org.eclipse.swt.widgets.DirectoryDialog;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Shell;
import org.eclipse.swt.widgets.Text;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.layout.GridData;

import henry.common.ItemUI;
import henry.common.Venta;
/**
 * ZetCode Java SWT tutorial
 *
 * This program shows the List
 * widget
 *
 * @author jan bodnar
 * website zetcode.com
 * last modified June 2009
 */


public class VentaUI { 

    Shell shell;

    public VentaUI(Display display) {

        shell = new Shell(display);

        shell.setText("List");

        initUI();

        shell.setSize(300, 250);
        shell.setLocation(300, 300);

        shell.open();

        while (!shell.isDisposed()) {
          if (!display.readAndDispatch()) {
            display.sleep();
          }
        }
    }


    public void initUI() {


        GridLayout gl = new GridLayout(4, true);
        gl.horizontalSpacing = 4;
        gl.verticalSpacing = 4;
        gl.marginBottom = 5;
        gl.marginTop = 5;
        shell.setLayout(gl);


        String[] buttons = {
            "Cls", "Bck", "", "Close", "7", "8", "9", "/", "4",
            "5", "6", "*", "1", "2", "3", "-", "0", ".", "=", "+"
        };


        Text display = new Text(shell, SWT.SINGLE);
        GridData gridData = new GridData();
        gridData.horizontalSpan = 4;
        gridData.horizontalAlignment = GridData.FILL;
        display.setLayoutData(gridData);

        for (int i = 0; i < buttons.length; i++) {

            if (i == 2) {
                Label lbl = new Label(shell, SWT.CENTER);
                GridData gd = new GridData(SWT.FILL, SWT.FILL, false, false);
                lbl.setLayoutData(gd);
            } else {
               Text btn = new Text(shell, SWT.SINGLE);
               btn.setText(buttons[i]);
               GridData gd = new GridData(SWT.FILL, SWT.FILL, false, false);
               gd.widthHint = 50;
               gd.heightHint = 30;
               btn.setLayoutData(gd);
            }
        }



    }



    	public static void main (String [] args) {
    		Display display = new Display ();
    		//new VentaUI(display);
    		Shell shell = new Shell(display);
    		//ItemUI item = new ItemUI(shell);
    		   shell.setSize(300, 250);
    	        shell.setLocation(300, 300);

    	        GridLayout gl = new GridLayout(4, true);
    	        gl.horizontalSpacing = 4;
    	        gl.verticalSpacing = 4;
    	        gl.marginBottom = 5;
    	        gl.marginTop = 5;
    	        shell.setLayout(gl);
    	        
    	        Text btn = new Text(shell, SWT.SINGLE);
                btn.setText("puta barata");
                GridData gd = new GridData(SWT.FILL, SWT.FILL, false, false);
                gd.widthHint = 50;
                gd.heightHint = 30;
                btn.setLayoutData(gd);
    	        shell.open();

    	        while (!shell.isDisposed()) {
    	          if (!display.readAndDispatch()) {
    	            display.sleep();
    	          }
    	        }
    		display.dispose ();
    	}
     
    
    
}
