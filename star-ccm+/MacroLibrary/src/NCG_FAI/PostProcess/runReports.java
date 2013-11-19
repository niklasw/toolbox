// STAR-CCM+ macro: t.java
package NCG_FAI.PostProcess;


import star.common.*;

import myFunctions.*;

public class runReports extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation SIM = getActiveSimulation();

    myPost myP = new myPost(SIM);

    Region inletRegion = SIM.getRegionManager().getRegion("Region 1");
    double inletBMAP = myP.surfaceMassFlowAverage("Inlet bma total pressure", myP.getBoundaries(inletRegion, "inlet"), "TotalPressure");
    double ambienceBMAP = myP.surfaceMassFlowAverage("Inlet bma total pressure", myP.getBoundaries(inletRegion, "ambien"), "TotalPressure");

    myP.runAllReports();
  }
}
