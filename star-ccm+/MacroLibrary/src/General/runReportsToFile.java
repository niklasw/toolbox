// STAR-CCM+ macro: t.java
package General;


import NCG_FAI.PostProcess.*;
import star.common.*;

import myFunctions.*;

public class runReportsToFile extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation SIM = getActiveSimulation();

    myPost myP = new myPost(SIM);

    myP.runAllReports(myP.fullPathNoExt()+".reports");
  }
}
