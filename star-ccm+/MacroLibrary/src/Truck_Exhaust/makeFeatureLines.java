// STAR-CCM+ macro: t.java
package Truck_Exhaust;

import java.util.*;

import star.common.*;
import star.base.neo.*;
import star.meshing.*;

public class makeFeatureLines extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation_0 = getActiveSimulation();

    LeafMeshPart leafMeshPart_0 = ((LeafMeshPart) simulation_0.get(SimulationPartManager.class).getPart("Silencer"));

    Collection partObjects = leafMeshPart_0.getPartSurfaceManager().getObjects();

    PartCurve partCurve_0 = leafMeshPart_0.createPartCurvesOnPartSurfaces(new NeoObjectVector(partObjects.toArray()), true, false, false, true, false, false, true, 31.0, true);
  }
}
