// STAR-CCM+ macro: importParts.java
package Truck_Exhaust;

import java.util.*;

import star.common.*;
import star.base.neo.*;
import star.meshing.*;
import myFunctions.*;

public class importParts extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    String prefix = "/home/fluidsim/Internal_Flow/261571_Eu6_Exhaust_outlet_pipes/PRE/Geometry";

    Hashtable<String,String> silencerMap = new Hashtable<String,String>();

    silencerMap.put("RH1_Medium","/Silencers/Medium/127mm/Eu6_Medium_127mm_2071281-1_1_cleaned.stl"                                  );
    silencerMap.put("RH1_Large", "/Silencers/Large/127mm/Eu6_Large_127mm_2071282-1_1_cleaned_removedFlanges_translated3mm.igs.stl");
    silencerMap.put("LH_oval_Large", "/Silencers/Large/127mm/Eu6_Large_127mm_2071282-1_1_cleaned_removedFlanges_translated3mm.igs.stl");

    Hashtable<String,String> pipeMap = new Hashtable<String,String>();
    pipeMap.put("RH1_Medium","/Pipes/127mm/Eu6_127mm_RH_1_2073079-1_1.stl");
    pipeMap.put("RH1_Large", "/Pipes/127mm/Eu6_127mm_RH_1_2073079-1_1.stl");
    pipeMap.put("LH_oval_Large", "/Pipes/127mm_oval_LHS/Eu6_127mm_LH_oval_HG-50367336.stl");

    Hashtable<String,String> ambienceMap = new Hashtable<String,String>();
    ambienceMap.put("RH1_Medium","/Silencers/Medium/127mm/Eu6_127mm_RH_1_2073079-1_1_ambience.stl");
    ambienceMap.put("RH1_Large", "/Silencers/Medium/127mm/Eu6_127mm_RH_1_2073079-1_1_ambience.stl" );
    ambienceMap.put("RH1_Large", "/Silencers/Medium/127mm/Eu6_127mm_RH_1_2073079-1_1_ambience.stl" );

    Simulation simulation = getActiveSimulation();

    myCase myC = new myCase(simulation);

    String simDirName = myC.directoryname();

    String silencerFile  = silencerMap.get(simDirName);
    String silencerName  = silencerFile.substring(silencerFile.lastIndexOf("/")+1,silencerFile.lastIndexOf("."));

    String pipeFile = pipeMap.get(simDirName);
    String pipeName = pipeFile.substring(pipeFile.lastIndexOf("/")+1,pipeFile.lastIndexOf("."));

    String ambienceFile = ambienceMap.get(simDirName);
    String ambienceName = ambienceFile.substring(ambienceFile.lastIndexOf("/")+1,ambienceFile.lastIndexOf("."));

    Units units = simulation.getUnitsManager().getPreferredUnits(new IntVector(new int[] {0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}));

    PartImportManager partImportManager = simulation.get(PartImportManager.class);

    Units units_1 = ((Units) simulation.getUnitsManager().getObject("mm"));

    partImportManager.importStlPart(resolvePath(prefix+silencerFile), "OneSurfacePerPatch", units_1, true, 1.0E-5);
    LeafMeshPart part = (LeafMeshPart) simulation.get(SimulationPartManager.class).getPart(silencerName);
    part.setPresentationName("Silencer");

    partImportManager.importStlPart(resolvePath(prefix+pipeFile), "OneSurfacePerPatch", units_1, true, 1.0E-5);
    part = (LeafMeshPart) simulation.get(SimulationPartManager.class).getPart(pipeName);
    part.setPresentationName("Pipe");

    partImportManager.importStlPart(resolvePath(prefix+ambienceFile), "OneSurfacePerPatch", units_1, true, 1.0E-5);
    part = (LeafMeshPart) simulation.get(SimulationPartManager.class).getPart(ambienceName);
    part.setPresentationName("Ambience");
  }
}



