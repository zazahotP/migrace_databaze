
package cz.ctu.fee.murinrad.paymentserver;

import javax.xml.ws.WebFault;


/**
 * This class was generated by the JAX-WS RI.
 * JAX-WS RI 2.2.6b21 
 * Generated source version: 2.2
 * 
 */
@WebFault(name = "PaymentException", targetNamespace = "http://paymentserver.murinrad.fee.ctu.cz/")
public class PaymentException_Exception
    extends Exception
{

    /**
     * Java type that goes as soapenv:Fault detail element.
     * 
     */
    private PaymentException faultInfo;

    /**
     * 
     * @param message
     * @param faultInfo
     */
    public PaymentException_Exception(String message, PaymentException faultInfo) {
        super(message);
        this.faultInfo = faultInfo;
    }

    /**
     * 
     * @param message
     * @param faultInfo
     * @param cause
     */
    public PaymentException_Exception(String message, PaymentException faultInfo, Throwable cause) {
        super(message, cause);
        this.faultInfo = faultInfo;
    }

    /**
     * 
     * @return
     *     returns fault bean: cz.ctu.fee.murinrad.paymentserver.PaymentException
     */
    public PaymentException getFaultInfo() {
        return faultInfo;
    }

}
