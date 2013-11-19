// STAR-CCM+ macro: t.java
package Truck_Exhaust;


import NCG_FAI.PreProcess.*;
import star.common.*;

import myFunctions.*;

public class setLocalMeshValues extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation = getActiveSimulation();

    myMeshing myF = new myMeshing(simulation);

    String CWD = myF.pwd();
    String simDirName = myF.dirname();
    simulation.println("WKN --> "+CWD+" "+simDirName);

    myF.createFeaturelinesOnRegions(45.0);

    myF.defaultPrismForAll();

    myF.disablePrism("upstream","inlet");
    myF.disablePrism("upstream","ambience");

    myF.setTargetSize("upstream","wall",100.0);
    myF.setTargetSize("upstream","wall_pipe_end",25.0);
    myF.setTargetSize("upstream","inlets",200.0);
    myF.setTargetSize("upstream","ambience", 2000);

    
  }
}
