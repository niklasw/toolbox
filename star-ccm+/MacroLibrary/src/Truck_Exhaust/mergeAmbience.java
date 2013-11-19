// STAR-CCM+ macro: t.java
package Truck_Exhaust;

import java.util.*;

import star.common.*;
import star.base.neo.*;
import star.vis.*;
import star.meshing.*;

public class mergeAmbience extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation_0 = 
      getActiveSimulation();

    MeshActionManager meshActionManager_0 = 
      simulation_0.get(MeshActionManager.class);

    String pipeName = "Pipe";
    String pipeSurfaceName = "partbody";
    String ambienceName = "Ambience";

    LeafMeshPart leafMeshPart_0 = ((LeafMeshPart) simulation_0.get(SimulationPartManager.class).getPart(ambienceName));

    LeafMeshPart leafMeshPart_1 = ((LeafMeshPart) simulation_0.get(SimulationPartManager.class).getPart(pipeName));

    LeafMeshPart leafMeshPart_2 = (LeafMeshPart) meshActionManager_0.subtractParts(new NeoObjectVector(new Object[] {leafMeshPart_1, leafMeshPart_0}), leafMeshPart_0, "Discrete");

    // Test below. How consistent is the naming??
    // Delete flow blocking surfaces and doublets
    leafMeshPart_2.setPresentationName("Ambience_merged");

    PartSurface partSurface_0 = leafMeshPart_2.getPartSurfaceManager().getPartSurface(pipeSurfaceName);
    leafMeshPart_2.deleteMeshPartSurfaces(new NeoObjectVector(new Object[] {partSurface_0}));

    partSurface_0 = leafMeshPart_2.getPartSurfaceManager().getPartSurface("pipe_end");
    leafMeshPart_2.deleteMeshPartSurfaces(new NeoObjectVector(new Object[] {partSurface_0}));

    Collection partSurfaces = leafMeshPart_2.getPartSurfaceManager().getObjects();
    PartSurface partSurface_1 = (PartSurface) partSurfaces.toArray()[0];

    leafMeshPart_2.getPartSurfaceManager().splitPartSurfacesByAngle(new NeoObjectVector(new Object[] {partSurface_1}), 89.0);

    PartSurface partSurface_2 = leafMeshPart_2.getPartSurfaceManager().getPartSurface(" 4");

    leafMeshPart_2.deleteMeshPartSurfaces(new NeoObjectVector(new Object[] {partSurface_2}));

    // Combine remaining ambient patches into one

    PartSurface partSurface_3 = leafMeshPart_2.getPartSurfaceManager().getPartSurface(" 2");

    PartSurface partSurface_4 = leafMeshPart_2.getPartSurfaceManager().getPartSurface(" 3");

    leafMeshPart_2.combinePartSurfaces(new NeoObjectVector(new Object[] {partSurface_1, partSurface_3, partSurface_4}));

  }
}
