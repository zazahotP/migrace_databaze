package timetable.converter;

import java.util.logging.Level;
import java.util.logging.Logger;
import javax.faces.component.UIComponent;
import javax.faces.context.FacesContext;
import javax.faces.convert.Converter;
import javax.faces.convert.ConverterException;
import javax.faces.convert.FacesConverter;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import timetable.model.LinkType;
import timetable.sb.TimetableCenterLocal;

/**
 *
 * @author valekfra
 */
@FacesConverter(value = "linkTypeConv")
public class LinkTypeConverter implements Converter {
    TimetableCenterLocal tc = lookupSchoolCenterLocal();

    @Override
    public Object getAsObject(FacesContext context, UIComponent component, String value) {
        try {
            return tc.getLinkTypeById(Integer.parseInt(value));
        } catch (NumberFormatException ex) {
            Logger.getLogger(getClass().getName()).log(Level.SEVERE, "exception caught", ex);
            throw new ConverterException(ex);
        }
    }

    @Override
    public String getAsString(FacesContext context, UIComponent component, Object value) {
        return String.valueOf(((LinkType) value).getId());
    }

    private TimetableCenterLocal lookupSchoolCenterLocal() {
        try {
            Context c = new InitialContext();
            return (TimetableCenterLocal) c.lookup("java:global/Timetable/Timetable-ejb/TimetableCenter!timetable.sb.TimetableCenterLocal");
        } catch (NamingException ne) {
            Logger.getLogger(getClass().getName()).log(Level.SEVERE, "exception caught", ne);
            throw new RuntimeException(ne);
        }
    }


}
