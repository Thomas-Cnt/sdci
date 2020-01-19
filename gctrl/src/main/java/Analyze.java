import java.util.List;

//

//* @author couedrao on 25/11/2019.

//* @project gctrl

//

//
//* 1)Perform complex data analysis and reasoning on the symptoms provided by the monitor function.
//* 2)Influenced by stored knowledge data.
//* 3)If changes are required, a change request is logically passed to the plan function.
//*
@SuppressWarnings({"SameParameterValue", "SynchronizeOnNonFinalField"})
class Analyze {
    public String gw_current_RFC = "";
    private static int i;

    void start() {
        Main.logger(this.getClass().getSimpleName(), "Start Analyzing");

        while (Main.run) {

            String current_symptom = get_symptom();
            //Main.logger(this.getClass().getSimpleName(), "Received Symptom : " + current_symptom);

            update_rfc(rfc_generator(current_symptom));
        }
    }

    //Symptom Receiver
    private String get_symptom() {
        synchronized (Main.monitor.gw_current_SYMP) {
            try {
                Main.monitor.gw_current_SYMP.wait();
            } catch (InterruptedException ex) {
                ex.printStackTrace();
            }
        }
        return Main.monitor.gw_current_SYMP;
    }

    //Rule-based RFC Generator
    private String rfc_generator(String symptom) {
        List<String> symptoms = Main.shared_knowledge.get_symptoms();
        List<String> rfcs = Main.shared_knowledge.get_rfc();

        if (symptom.contentEquals(symptoms.get(0)) || symptom.contentEquals(symptoms.get(2))) {
            Main.logger(this.getClass().getSimpleName(), "RFC --> To plan : " + rfcs.get(0));
            i = 0;
            return rfcs.get(0);
        } else if (symptom.contentEquals(symptoms.get(1))) {
            i++;
            if (i < 3) {
                Main.logger(this.getClass().getSimpleName(), "RFC --> To plan : " + rfcs.get(1));
                return rfcs.get(1);
            } else {
                Main.logger(this.getClass().getSimpleName(), "RFC --> To plan : " + "YourPlansDoNotWork");
                return "YourPlansDoNotWork";
            }
        } else
            return null;

    }


    private void update_rfc(String rfc) {

        synchronized (gw_current_RFC) {
            gw_current_RFC.notify();
            gw_current_RFC = rfc;

        }
    }

}
