
package cz.ctu.fee.murinrad.ifaceserver;

import javax.xml.ws.WebFault;


/**
 * This class was generated by Apache CXF 2.3.1
 * Sun Dec 09 23:32:37 CET 2012
 * Generated source version: 2.3.1
 * 
 */

@WebFault(name = "CancelReservationException", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/")
public class CancelReservationException_Exception extends Exception {
    public static final long serialVersionUID = 20121209233237L;
    
    private cz.ctu.fee.murinrad.ifaceserver.CancelReservationException cancelReservationException;

    public CancelReservationException_Exception() {
        super();
    }
    
    public CancelReservationException_Exception(String message) {
        super(message);
    }
    
    public CancelReservationException_Exception(String message, Throwable cause) {
        super(message, cause);
    }

    public CancelReservationException_Exception(String message, cz.ctu.fee.murinrad.ifaceserver.CancelReservationException cancelReservationException) {
        super(message);
        this.cancelReservationException = cancelReservationException;
    }

    public CancelReservationException_Exception(String message, cz.ctu.fee.murinrad.ifaceserver.CancelReservationException cancelReservationException, Throwable cause) {
        super(message, cause);
        this.cancelReservationException = cancelReservationException;
    }

    public cz.ctu.fee.murinrad.ifaceserver.CancelReservationException getFaultInfo() {
        return this.cancelReservationException;
    }
}
