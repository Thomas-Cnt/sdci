import java.util.List;

/**
 * @author couedrao on 27/11/2019.
 * @project gctrl
 */
class SDNCtrlAPI {

    String redirect_traffic(String olddestip, String newdestip) {
        String status = "OK";
        Main.logger(this.getClass().getSimpleName(), "olddestip = " + olddestip + "; newdestip = " + newdestip);
        //TODO

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
