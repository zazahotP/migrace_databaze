package cz.ctu.fee.murinrad.ifaceserver;

import javax.jws.WebMethod;
import javax.jws.WebParam;
import javax.jws.WebResult;
import javax.jws.WebService;
import javax.xml.bind.annotation.XmlSeeAlso;
import javax.xml.ws.Action;
import javax.xml.ws.FaultAction;
import javax.xml.ws.RequestWrapper;
import javax.xml.ws.ResponseWrapper;

/**
 * This class was generated by Apache CXF 2.3.1
 * Sun Dec 09 23:32:37 CET 2012
 * Generated source version: 2.3.1
 * 
 */
 
@WebService(targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", name = "InterfaceServiceIface")
@XmlSeeAlso({ObjectFactory.class})
public interface InterfaceServiceIface {

    @WebResult(name = "return", targetNamespace = "")
    @Action(input = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/printTicketRequest", output = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/printTicketResponse", fault = {@FaultAction(className = PrintingException_Exception.class, value = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/printTicket/Fault/PrintingException")})
    @RequestWrapper(localName = "printTicket", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.PrintTicket")
    @WebMethod
    @ResponseWrapper(localName = "printTicketResponse", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.PrintTicketResponse")
    public byte[] printTicket(
        @WebParam(name = "TicketID", targetNamespace = "")
        java.lang.Integer ticketID
    ) throws PrintingException_Exception;

    @WebResult(name = "return", targetNamespace = "")
    @Action(input = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/findFlightRequest", output = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/findFlightResponse", fault = {@FaultAction(className = SearchException_Exception.class, value = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/findFlight/Fault/SearchException")})
    @RequestWrapper(localName = "findFlight", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.FindFlight")
    @WebMethod
    @ResponseWrapper(localName = "findFlightResponse", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.FindFlightResponse")
    public cz.ctu.fee.murinrad.ifaceserver.FlightCollection findFlight(
        @WebParam(name = "arrivalAPT", targetNamespace = "")
        java.lang.String arrivalAPT,
        @WebParam(name = "departureAPT", targetNamespace = "")
        java.lang.String departureAPT,
        @WebParam(name = "arrivalTime", targetNamespace = "")
        java.lang.Long arrivalTime,
        @WebParam(name = "departureTime", targetNamespace = "")
        java.lang.Long departureTime
    ) throws SearchException_Exception;

    @WebResult(name = "return", targetNamespace = "")
    @Action(input = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/getTicketsPerPassengerRequest", output = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/getTicketsPerPassengerResponse", fault = {@FaultAction(className = SearchException_Exception.class, value = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/getTicketsPerPassenger/Fault/SearchException")})
    @RequestWrapper(localName = "getTicketsPerPassenger", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.GetTicketsPerPassenger")
    @WebMethod
    @ResponseWrapper(localName = "getTicketsPerPassengerResponse", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.GetTicketsPerPassengerResponse")
    public cz.ctu.fee.murinrad.ifaceserver.TicketPackage getTicketsPerPassenger(
        @WebParam(name = "passengerIDDocument", targetNamespace = "")
        java.lang.String passengerIDDocument
    ) throws SearchException_Exception;

    @WebResult(name = "return", targetNamespace = "")
    @Action(input = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/changeReservationRequest", output = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/changeReservationResponse", fault = {@FaultAction(className = ChangeReservationException_Exception.class, value = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/changeReservation/Fault/ChangeReservationException")})
    @RequestWrapper(localName = "changeReservation", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.ChangeReservation")
    @WebMethod
    @ResponseWrapper(localName = "changeReservationResponse", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.ChangeReservationResponse")
    public cz.ctu.fee.murinrad.ifaceserver.Ticket changeReservation(
        @WebParam(name = "ticketID", targetNamespace = "")
        java.lang.Integer ticketID,
        @WebParam(name = "newFlightID", targetNamespace = "")
        java.lang.Integer newFlightID,
        @WebParam(name = "newSeatID", targetNamespace = "")
        java.lang.Integer newSeatID
    ) throws ChangeReservationException_Exception;

    @WebResult(name = "return", targetNamespace = "")
    @Action(input = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/getFreeSeatsForFlightRequest", output = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/getFreeSeatsForFlightResponse", fault = {@FaultAction(className = SearchException_Exception.class, value = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/getFreeSeatsForFlight/Fault/SearchException")})
    @RequestWrapper(localName = "getFreeSeatsForFlight", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.GetFreeSeatsForFlight")
    @WebMethod
    @ResponseWrapper(localName = "getFreeSeatsForFlightResponse", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.GetFreeSeatsForFlightResponse")
    public cz.ctu.fee.murinrad.ifaceserver.SeatCollection getFreeSeatsForFlight(
        @WebParam(name = "flightID", targetNamespace = "")
        java.lang.Integer flightID
    ) throws SearchException_Exception;

    @WebResult(name = "return", targetNamespace = "")
    @Action(input = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/bookFlightRequest", output = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/bookFlightResponse", fault = {@FaultAction(className = ReservationException_Exception.class, value = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/bookFlight/Fault/ReservationException")})
    @RequestWrapper(localName = "bookFlight", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.BookFlight")
    @WebMethod
    @ResponseWrapper(localName = "bookFlightResponse", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.BookFlightResponse")
    public cz.ctu.fee.murinrad.ifaceserver.Ticket bookFlight(
        @WebParam(name = "passenger", targetNamespace = "")
        cz.ctu.fee.murinrad.ifaceserver.Passenger passenger,
        @WebParam(name = "seatNumber", targetNamespace = "")
        java.lang.Integer seatNumber,
        @WebParam(name = "flightID", targetNamespace = "")
        java.lang.Integer flightID
    ) throws ReservationException_Exception;

    @WebResult(name = "return", targetNamespace = "")
    @Action(input = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/payForAReservationCashRequest", output = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/payForAReservationCashResponse", fault = {@FaultAction(className = PaymentException_Exception.class, value = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/payForAReservationCash/Fault/PaymentException")})
    @RequestWrapper(localName = "payForAReservationCash", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.PayForAReservationCash")
    @WebMethod
    @ResponseWrapper(localName = "payForAReservationCashResponse", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.PayForAReservationCashResponse")
    public cz.ctu.fee.murinrad.ifaceserver.CashPayment payForAReservationCash(
        @WebParam(name = "ticketID", targetNamespace = "")
        java.lang.Integer ticketID,
        @WebParam(name = "amountDue", targetNamespace = "")
        java.lang.Double amountDue
    ) throws PaymentException_Exception;

    @WebResult(name = "return", targetNamespace = "")
    @Action(input = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/payForAReservationCardRequest", output = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/payForAReservationCardResponse", fault = {@FaultAction(className = PaymentException_Exception.class, value = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/payForAReservationCard/Fault/PaymentException")})
    @RequestWrapper(localName = "payForAReservationCard", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.PayForAReservationCard")
    @WebMethod
    @ResponseWrapper(localName = "payForAReservationCardResponse", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.PayForAReservationCardResponse")
    public cz.ctu.fee.murinrad.ifaceserver.CardPayment payForAReservationCard(
        @WebParam(name = "ticketID", targetNamespace = "")
        java.lang.Integer ticketID,
        @WebParam(name = "amountDue", targetNamespace = "")
        java.lang.Double amountDue,
        @WebParam(name = "cardData", targetNamespace = "")
        cz.ctu.fee.murinrad.ifaceserver.CardData cardData
    ) throws PaymentException_Exception;

    @Action(input = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/cancelReservationRequest", output = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/cancelReservationResponse", fault = {@FaultAction(className = CancelReservationException_Exception.class, value = "http://interfaceserver.murinrad.fee.ctu.cz/InterfaceServiceIface/cancelReservation/Fault/CancelReservationException")})
    @RequestWrapper(localName = "cancelReservation", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.CancelReservation")
    @WebMethod
    @ResponseWrapper(localName = "cancelReservationResponse", targetNamespace = "http://interfaceserver.murinrad.fee.ctu.cz/", className = "cz.ctu.fee.murinrad.ifaceserver.CancelReservationResponse")
    public void cancelReservation(
        @WebParam(name = "passengerIDDocNumber", targetNamespace = "")
        java.lang.String passengerIDDocNumber,
        @WebParam(name = "TicketID", targetNamespace = "")
        java.lang.Integer ticketID
    ) throws CancelReservationException_Exception;
}
