// STAR-CCM+ macro: t.java
package General;


import java.util.List;
import star.common.*;

import myFunctions.*;

public class stripPatchNames extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation = getActiveSimulation();

    myMeshing myF = new myMeshing(simulation);

    List<Region> regions = myF.getRegions(".*"); 
    for (Region r: regions)
    {
	    myF.stripBoundaryNames(r);
    }
  }
}
