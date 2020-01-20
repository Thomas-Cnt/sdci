import java.util.List;

//

//* @author couedrao on 25/11/2019.

//* @project gctrl

//

//
//* Changes the behavior of the managed resource using effectors Changes the behavior of the managed resource using effectors, based on the actions recommended by the plan function.
//*
@SuppressWarnings({"SameParameterValue", "SynchronizeOnNonFinalField"})
class Execute {
    private static List<String> workflow_lists;
    private static final MANOAPI manoapi = new MANOAPI();
    private static final SDNCtrlAPI sdnctlrapi = new SDNCtrlAPI();

    void start() throws InterruptedException {
        Main.logger(this.getClass().getSimpleName(), "Start Execution");
        workflow_lists = Main.shared_knowledge.get_worklow_lists();

        while (Main.run) {
            String current_plan = get_plan();

            // Main.logger(this.getClass().getSimpleName(), "Received Plan : " + current_plan);
            String[] workflow = workflow_generator(current_plan);
            for (int i = 0; i < workflow.length; i++) {
                Main.logger(this.getClass().getSimpleName(), "workflow [" + i + "] : " + workflow[i]);

            }

            for (String w : workflow) {
                Main.logger(this.getClass().getSimpleName(), "UC : " + w);
                switch (w) {
                    case "UC1":
                        Main.logger(this.getClass().getSimpleName(), "Nothing to do");
                        break;
                    case "UC2":
                        Main.logger(this.getClass().getSimpleName(), "Deploying LB+GW");
                        List<String> newgwsip = manoapi.deploy_multi_gws_and_lb();
                        Main.shared_knowledge.setLbip(newgwsip.get(0));
                        Main.shared_knowledge.setNewgwsip(newgwsip.subList(1, newgwsip.size()));
                        Main.logger(this.getClass().getSimpleName(), "Redirecting Traffic");
                        String status = sdnctlrapi.redirect_traffic();
                        Main.logger(this.getClass().getSimpleName(), status);
                        break;
                    default:
                }
                Thread.sleep(2000);
                continue;


            }

        }
    }

    //Plan Receiver
    private String get_plan() {
        synchronized (Main.plan.gw_PLAN) {
            try {
                Main.plan.gw_PLAN.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        return Main.plan.gw_PLAN;
    }

    //Rule-based Workflow Generator
    private String[] workflow_generator(String plan) {
        List<String> plans = Main.shared_knowledge.get_plans();
        if (plan.contentEquals(plans.get(0))) {
            return workflow_lists.get(0).split("/");
        } else if (plan.contentEquals(plans.get(1))) {
            return workflow_lists.get(1).split("/");
        } else if (plan.contentEquals(plans.get(2))) {
            return workflow_lists.get(2).split("/");
        } else
            return null;
    }
}
