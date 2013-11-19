// STAR-CCM+ macro: mesh.java
package General;

import java.util.*;

import star.common.*;
import star.meshing.*;

public class mesh extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation SIM = getActiveSimulation();

    MeshPipelineController mesh = SIM.get(MeshPipelineController.class);
    mesh.generateVolumeMesh();
  }
}
