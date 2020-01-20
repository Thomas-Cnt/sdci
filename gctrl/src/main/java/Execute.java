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
                    case "UC2":   //deploy LB
                        Main.logger(this.getClass().getSimpleName(), "Deploying LB");
                        status = manoapi.deploy_lb();
                        Main.logger(this.getClass().getSimpleName(), status);
                        break;
                    case "UC3":   // deploy GW
                        Main.logger(this.getClass().getSimpleName(), "Deploying GW");
                        status = manoapi.deploy_gw();
                        Main.logger(this.getClass().getSimpleName(), status);
                        break;
                    case "UC4":   // redirect traffic : everything that was going to GI goes to LB
                        Main.logger(this.getClass().getSimpleName(), "Redirecting Traffic to LB");
                        String status = sdnctlrapi.redirect_traffic();
                        Main.logger(this.getClass().getSimpleName(), status);
                        break;
                    case "UC5":   // redirect traffic : everything that was coming from Virtual_GI pretends to come from GI
                        Main.logger(this.getClass().getSimpleName(), "Virtual GI pretends to be GI");
                        String status = sdnctlrapi.virtualGI_pretends_GI();
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
        } /*else if (plan.contentEquals(plans.get(2))) {
            return workflow_lists.get(2).split("/");            //only 2 plan : A(nothing) and B(gw lb + redirect)
        }*/ else
            return null;
    }
}
