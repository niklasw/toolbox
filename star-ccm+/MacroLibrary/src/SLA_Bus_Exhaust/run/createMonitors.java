// STAR-CCM+ macro: importCutplane.java
package SLA_Bus_Exhaust.run;

import NCG_FAI.PostProcess.*;
import java.util.*;
import java.io.*;
import star.base.neo.*;

import star.common.*;
import star.vis.*;

import myFunctions.*;

public class createMonitors extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation SIM = getActiveSimulation();

    myPost myP = new myPost(SIM);

    String prefix = myP.dirname();
    String simTitle = myP.title();

    SIM.println("WKN --> "+prefix+" "+myP.dirname());

    String inletRegionName = "a_upstream";

    List<String> sectionFiles = myP.findFile(prefix,"section.*stl");

    Units units_mm = ((Units) SIM.getUnitsManager().getObject("mm"));
    Units units_m = ((Units) SIM.getUnitsManager().getObject("m"));

    try {

        FileWriter outFile = new FileWriter(myP.fullPathNoExt()+".monitors");
        BufferedWriter out = new BufferedWriter(outFile);

        for (String sectionFile: sectionFiles)
        {
            String sectionName = myP.basenameNoExt(sectionFile);
            ArbitrarySection section = myP.importArbitrary(sectionFile, units_mm);
            String reportString = sectionName+" total pressure mavg";
            double pTotMAvg = myP.surfaceMassFlowAverage(reportString,section,"TotalPressure");
            SIM.println("Report --> " + reportString+" = "+ pTotMAvg);
            out.write(reportString+" = "+ pTotMAvg+"\n");
        }

        //String inletRegionName = promptUserForInput("Inlet in which region?", "Insert region name");
        Region inletRegion = SIM.getRegionManager().getRegion(inletRegionName);
        List<Boundary> inletBoundary = myP.getBoundaries(inletRegion,"inlet");
        double inletPTotMAvg = myP.surfaceMassFlowAverage("Inlet mass flow avg", inletBoundary,  "TotalPressure");
        SIM.println("Report --> " + "Inlet total pressure mavg = "+ inletPTotMAvg);
        out.write("Inlet total pressure mavg = "+ inletPTotMAvg+"\n");
        out.close();

    } catch(IOException e) {}
  }
}
