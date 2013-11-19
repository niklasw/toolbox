// STAR-CCM+ macro: macro_volume.java
package macro;

import java.util.*;

import star.common.*;
import star.base.neo.*;
import star.vis.*;
import star.dualmesher.*;
import star.prismmesher.*;
//
import star.resurfacer.*;
import star.surfacewrapper.*;
import star.meshing.*;

public class createVolumeMesh extends StarMacro {

  public void execute() {
    execute0();
  }

  public void setCustomVolumeDensity(String regionName, double density, double growth) {

    Simulation SIM = getActiveSimulation();

    Region region = SIM.getRegionManager().getRegion(regionName);

    CustomizeVolumeMeshDensityOption customizeVolumeMeshDensityOption_0 = 
      region.get(MeshConditionManager.class).get(CustomizeVolumeMeshDensityOption.class);

    customizeVolumeMeshDensityOption_0.setCustomizeVolumeMeshDensityOption(true);

    VolumeMeshDensity volumeMeshDensity_0 = 
      region.get(MeshValueManager.class).get(VolumeMeshDensity.class);

    volumeMeshDensity_0.setVolumeMeshDensity(density);

    volumeMeshDensity_0.setGrowthFactor(growth);

  }

  private void execute0() {

    Simulation simulation_0 =
      getActiveSimulation();

    MeshContinuum meshContinuum_0 =
      ((MeshContinuum) simulation_0.getContinuumManager().getContinuum("Mesh 1"));

    MeshPipelineController meshPipelineController_0 =
      simulation_0.get(MeshPipelineController.class);

    meshPipelineController_0.generateVolumeMesh();
  }
}
