// STAR-CCM+ macro: macro_wrapping.java
package Truck_Exhaust;


import star.common.*;
import star.base.neo.*;
import star.resurfacer.*;
import star.meshing.*;

public class createSurfaceMesh extends StarMacro {

  public void execute() {
    execute0();
  }

  public void Warning(String warn) {
    System.out.println("\nWARNING from macro: "+ warn+"\n");
  }

  public void setCustomSurfaceSizes(String regionName, String surfaceName, double minSize, double targetSize) {

    try{
    Simulation SIM = getActiveSimulation();
    Region region = SIM.getRegionManager().getRegion(regionName);
    Boundary boundary = region.getBoundaryManager().getBoundary(surfaceName);
    SurfaceSizeOption surfaceSizeOption= boundary.get(MeshConditionManager.class).get(SurfaceSizeOption.class);
    surfaceSizeOption.setSurfaceSizeOption(true);
    SurfaceSize surfaceSize= boundary.get(MeshValueManager.class).get(SurfaceSize.class);
    if ( minSize > 0.0 ) {
        RelativeMinimumSize relativeMinimumSize= surfaceSize.getRelativeMinimumSize();
        relativeMinimumSize.setPercentage(minSize);
    }
    if ( targetSize > 0.0 ) {
        RelativeTargetSize relativeTargetSize= surfaceSize.getRelativeTargetSize();
        relativeTargetSize.setPercentage(targetSize);
    }
    } catch (NeoException e) {Warning("Could not set custom surface size on "+surfaceName);}
  }

  private void execute0() {

    Simulation simulation_0 = getActiveSimulation();

    MeshContinuum meshContinuum_0 = ((MeshContinuum) simulation_0.getContinuumManager().getContinuum("Mesh 1"));

    meshContinuum_0.enable(ResurfacerMeshingModel.class);

    ResurfacerMeshingModel resurfacerMeshingModel_0 = meshContinuum_0.getModelManager().getModel(ResurfacerMeshingModel.class);

    resurfacerMeshingModel_0.setDoAutomaticSurfaceRepair(true);

    MeshPipelineController meshPipelineController_0 = simulation_0.get(MeshPipelineController.class);

    meshPipelineController_0.generateSurfaceMesh();
  }
}
