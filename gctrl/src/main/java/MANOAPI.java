import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Random;
import java.net.HttpURLConnection;
/**
 * @author couedrao on 27/11/2019.
 * @project gctrl
 */
class MANOAPI {
/*
    String deploy_gw(Map<String, String> vnfinfos) {
        String ip = "192.168.0." + (new Random().nextInt(253) + 1);
        Main.logger(this.getClass().getSimpleName(), "Deploying VNF ...");

        //printing
        for (Entry<String, String> e : vnfinfos.entrySet()) {
            Main.logger(this.getClass().getSimpleName(), "\t" + e.getKey() + " : " + e.getValue());
        }
        //TODO

        return ip;
    }
*/
    String deploy_lb() {
        
        String status = "OK";
        try{
        //deploy lb
        URL url = new URL("http://127.0.0.1:5001/restapi/compute/dc1/lb");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("PUT");
        connection.setDoOutput(true);
        connection.setRequestProperty("Content-Type", "application/json");
        OutputStreamWriter osw = new OutputStreamWriter(connection.getOutputStream());
        osw.write("{\"image\":\"vnf:lb\", \"network\":\"(id=test,ip=10.0.0.206/24)\"}");
        osw.flush();
        osw.close();
        }
        catch (IOException e){
            e.printStackTrace();
            status="KO";
        }
        
        return status;
    }
        String deploy_gw() {
        
        String status = "OK";
        try{
        //deploy virtual gi
        URL url = new URL("http://127.0.0.1:5001/restapi/compute/dc1/virtualgi");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("PUT");
        connection.setDoOutput(true);
        connection.setRequestProperty("Content-Type", "application/json");
        OutputStreamWriter osw = new OutputStreamWriter(connection.getOutputStream());
        osw.write("{\"image\":\"vnf:gi\", \"network\":\"(id=test,ip=10.0.0.205/24)\"}");
        osw.flush();
        osw.close();
        }
        catch (IOException e){
            e.printStackTrace();
            status="KO";
        }
        
        return status;
    }

}
