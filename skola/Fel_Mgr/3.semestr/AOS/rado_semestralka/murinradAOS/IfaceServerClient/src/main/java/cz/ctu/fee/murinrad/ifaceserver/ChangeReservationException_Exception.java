
package cz.ctu.fee.murinrad.ifaceserver;

import javax.xml.ws.WebFault;


/**
 * This class was generated by Apache CXF 2.3.1
 * Sun Dec 09 23:32:36 CET 2012
 * Generated source version: 2.3.1
 * 
 */

@WebFault(name = "ChangeReservationException", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/")
public class ChangeReservationException_Exception extends Exception {
    public static final long serialVersionUID = 20121209233236L;
    
    private cz.ctu.fee.murinrad.ifaceserver.ChangeReservationException changeReservationException;

    public ChangeReservationException_Exception() {
        super();
    }
    
    public ChangeReservationException_Exception(String message) {
        super(message);
    }
    
    public ChangeReservationException_Exception(String message, Throwable cause) {
        super(message, cause);
    }

    public ChangeReservationException_Exception(String message, cz.ctu.fee.murinrad.ifaceserver.ChangeReservationException changeReservationException) {
        super(message);
        this.changeReservationException = changeReservationException;
    }

    public ChangeReservationException_Exception(String message, cz.ctu.fee.murinrad.ifaceserver.ChangeReservationException changeReservationException, Throwable cause) {
        super(message, cause);
        this.changeReservationException = changeReservationException;
    }

    public cz.ctu.fee.murinrad.ifaceserver.ChangeReservationException getFaultInfo() {
        return this.changeReservationException;
    }
}
