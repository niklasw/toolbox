// STAR-CCM+ macro: t.java
package General;



import star.common.*;

import myFunctions.*;

public class createNormalExtrusion extends StarMacro {

  public void execute() {
    execute0();
  }

 
  private void execute0() {

    Simulation simulation = getActiveSimulation();

    myMeshing myF = new myMeshing(simulation);

    String CWD = myF.pwd();
    String simDirName = myF.dirname();
    myF.createNormalExtrusion("Outlet_Region","outlet", 50, 10.0);
  }
}
