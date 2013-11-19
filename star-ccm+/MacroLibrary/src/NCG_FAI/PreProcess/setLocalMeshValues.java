// STAR-CCM+ macro: t.java
package NCG_FAI.PreProcess;


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

    myF.defaultPrismForAll();

    myF.disablePrism("upstream","inlet_eye");
    myF.disablePrism("upstream","interface");

    myF.setTargetSize("upstream","wall",300.0);
    myF.setTargetSize("upstream","wall_funnel",100.0);
    myF.setTargetSize("upstream","inlet_eye",200.0);
    myF.setTargetSize("upstream","equipment",200.0);
    myF.setTargetSize("upstream","bellow",50.0);
    myF.setTargetSize("upstream","sail",50.0);

    myF.disablePrism("filter_house","interface");
    myF.disablePrism("filter_porous","interface");
    myF.disablePrism("filter_inner","interface");

    myF.disablePrism("turbo_pipe","outlet");
    myF.disablePrism("turbo_pipe","interface");

    myF.setTargetSize("turbo_pipe","outlet", 150);

    
  }
}
