// STAR-CCM+ macro: setWallRoughness.java
package macro;

import java.util.*;

import star.turbulence.*;
import star.common.*;
import star.base.neo.*;

public class setWallRoughness extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation_0 = 
      getActiveSimulation();

    Region region_0 = 
      simulation_0.getRegionManager().getRegion("downstream");

    Boundary boundary_0 = 
      region_0.getBoundaryManager().getBoundary("interface_compressor");

    boundary_0.getConditions().get(WallSurfaceOption.class).setSelected(WallSurfaceOption.ROUGH);

    RoughnessHeightProfile roughnessHeightProfile_0 = 
      boundary_0.getValues().get(RoughnessHeightProfile.class);

    roughnessHeightProfile_0.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(1.0E-4);
  }
}
