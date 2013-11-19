// STAR-CCM+ macro: A1_addThinMesher.java
package Truck_Exhaust;

import java.util.*;

import star.common.*;

public class playSetupMesh extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

  Simulation simulation_0 = getActiveSimulation();

  List<String> scriptList = Arrays.asList(
               "importParts.java",
               "mergeAmbience.java",
               "makeFeatureLines.java",
               "partsToRegions.java",
               "setLocalMeshValues.java",
               "setupBC.java",
               "createMonitors.java"
            );

    Iterator<String> scriptIter = scriptList.iterator();
    while ( scriptIter.hasNext() ) {
        String scriptName = scriptIter.next();
        System.out.println("Running "+scriptName);
        new StarScript(simulation_0, new java.io.File(resolvePath(scriptName)), getClass().getClassLoader()).play();
    }
  }
}
