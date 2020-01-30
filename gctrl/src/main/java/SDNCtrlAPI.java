import java.util.List;
import java.io.IOException;
import java.io.OutputStream;
import java.net.MalformedURLException;
import java.util.List;
import java.net.URL;
import java.net.HttpURLConnection;

/**
 * @author couedrao on 27/11/2019.
 * @project gctrl
 */
class SDNCtrlAPI {

    String redirect_traffic() {
        String status = "OK";
        Main.logger(this.getClass().getSimpleName(), "olddestip = 10.0.0.201 ; newdestip = 10.0.0.206");
        //TODO - DONE
        try 
        {
            URL url = new URL("http://localhost:8080/stats/flowentry/add");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            OutputStream os = conn.getOutputStream();
            os.write("{\"dpid\":2,\"match\": {\"ipv4_dest\":\"10.0.0.1\",\"eth_type\": 2048},\"actions:[{\"type\":\"SET_NW_DST\",\"nw_dst\":\"10.0.0.101\"}]}");
            os.flush();
        } 
        catch (IOException e) 
        { 
            e.printStackTrace(); 
            status = "KO"; 
        }

        return status;
    }
      
       

    String insert_a_loadbalancer(String oldgwip, String lbip, List<String> newgwsip) {
        String status = "OK";
        Main.logger(this.getClass().getSimpleName(), "oldgwip = " + oldgwip + "; lbip = " + lbip + "; newgwsip = " + newgwsip);
        //TODO

        return status;
    }

    String remove_less_important_traffic(String importantsrcip) {
        String status = "OK";
        Main.logger(this.getClass().getSimpleName(), "importantsrcip = " + importantsrcip);
        //TODO

        return status;
    }


}
