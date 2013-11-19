// STAR-CCM+ macro: tt.java
package Truck_Exhaust;


import star.common.*;
import star.base.neo.*;
import star.meshing.*;

public class partsToRegions extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation_0 = 
      getActiveSimulation();

    LeafMeshPart leafMeshPart_1 = 
      ((LeafMeshPart) simulation_0.get(SimulationPartManager.class).getPart("Pipe"));

    LeafMeshPart leafMeshPart_2 = 
      ((LeafMeshPart) simulation_0.get(SimulationPartManager.class).getPart("Silencer"));

    LeafMeshPart leafMeshPart_0 = 
      ((LeafMeshPart) simulation_0.get(SimulationPartManager.class).getPart("Ambience_merged"));

    simulation_0.getRegionManager().newRegionsFromParts(new NeoObjectVector(new Object[] {leafMeshPart_1, leafMeshPart_2, leafMeshPart_0}), "OneRegion", null, "OneBoundaryPerPartSurface", null, "OneFeatureCurve", null, true);

    Region region_0 = simulation_0.getRegionManager().getRegion("Region 1");

    if ( region_0.getBoundaryManager().has("Silencer.stostopipe") )
    {
        Boundary boundary_6 = region_0.getBoundaryManager().getBoundary("Silencer.stostopipe");
        region_0.getBoundaryManager().removeBoundaries(new NeoObjectVector(new Object[] {boundary_6}));
    }

  }
}
