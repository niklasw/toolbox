// STAR-CCM+ macro: t.java
package General;


import star.common.*;
import myFunctions.*;

public class makePartFeatures extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {
    Simulation simulation = getActiveSimulation();

    myMeshing myM = new myMeshing(simulation);

    myM.createFeaturelinesOnParts(45);
  }

}
