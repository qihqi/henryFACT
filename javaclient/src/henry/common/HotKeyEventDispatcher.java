package henry.common;

import java.awt.KeyEventDispatcher;
import java.awt.event.KeyEvent;

public class HotKeyEventDispatcher implements KeyEventDispatcher {

	
	private boolean called; //to ensure the function only run once istead of twice
	private Ventana ventana;
	
	public HotKeyEventDispatcher(Ventana vent) {
		ventana = vent;
		called = false;
	}
	@Override
	public boolean dispatchKeyEvent(KeyEvent e) {
		if (called) {
			called = false;
			return false;
		}
		called = true;
		
		switch (e.getKeyCode()) {
		case KeyEvent.VK_F6:
			//search producto
			ventana.getItemContainer().search();
			break;
		case KeyEvent.VK_F7:
			ventana.pagar();
			break;
		case KeyEvent.VK_F8:
			//aceptar
			ventana.aceptar();
			break;
		case KeyEvent.VK_F9:
			//cancelar
			ventana.clear();
			break;
		case KeyEvent.VK_F5:
			//buscar cliente
			ventana.getClientePanel().search();
			break;
		}
		return false;
	}

}
