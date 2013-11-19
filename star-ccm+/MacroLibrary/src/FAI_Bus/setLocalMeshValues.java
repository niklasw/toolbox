// STAR-CCM+ macro: t.java
package FAI_Bus;


import star.common.*;

import star.common.*;
import star.base.neo.*;
import star.extruder.*;
import star.meshing.*;

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


    myF.createNormalExtrusion("region","boundary", 40, 10.0);
  }
}
