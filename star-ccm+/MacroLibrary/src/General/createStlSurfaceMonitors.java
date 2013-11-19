// STAR-CCM+ macro: importCutplane.java
package General;

import java.util.*;
import java.io.*;

import star.common.*;
import star.vis.*;

import myFunctions.*;

public class createStlSurfaceMonitors extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation SIM = getActiveSimulation();

    myPost myP = new myPost(SIM);

    String prefix = myP.dirname();
    String simTitle = myP.title();

    SIM.println("WKN --> "+prefix+" "+myP.dirname());

    myP.Info("Parsing for section stl files in", prefix);

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
            //String reportString = sectionName+" mass flux";
            //double pTotMAvg = myP.planeMassFlux(reportString,section);
            String reportString = sectionName+" total pressure mavg";
            double pTotMAvg = myP.surfaceMassFlowAverage(reportString,section,"TotalPressure");
            SIM.println("Report --> " + reportString+" = "+ pTotMAvg);
            out.write(reportString+" = "+ pTotMAvg+"\n");
        }

        out.close();

    } catch(IOException e) {}
  }
}
