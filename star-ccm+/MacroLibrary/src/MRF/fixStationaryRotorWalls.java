// STAR-CCM+ macro: ttt.java
package MRF;


import star.common.*;
import star.flow.*;
import myFunctions.*;

public class fixStationaryRotorWalls extends StarMacro {

/*
	 * If non rotating walls are included in an MRF
	 * region, this seems to set the wall velocity
	 * to zero in the global coordinate frame of ref.
	 * NOTE hard coded names and values.
*/

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation SIM = 
      getActiveSimulation();

    myCase myC = new myCase(SIM);

    //myC.createFieldFunction('RPM', '10000.0', null, double)
    
    Region r = SIM.getRegionManager().getRegion("rotor");

    for (Boundary b: r.getBoundaryManager().getBoundaries())
    {

        if (b.getPresentationName().matches(".*stationary_rotor.*"))
        {
            b.getConditions().get(WallSlidingOption.class).setSelected(WallSlidingOption.ROTATION_RATE);

            WallRotationProfile wallRotationProfile_0 = b.getValues().get(WallRotationProfile.class);

            wallRotationProfile_0.getMethod(ConstantScalarProfileMethod.class).getQuantity().setDefinition("-$omega");
        }
    }
  }
}
