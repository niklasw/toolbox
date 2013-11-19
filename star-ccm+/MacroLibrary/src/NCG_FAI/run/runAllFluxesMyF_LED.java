// STAR-CCM+ macro: start.java
// Auth: sssler@scania.com, modified by konwkn@scania.com
package NCG_FAI.run;

import java.io.*;
import java.util.*;
import myFunctions.*;
import star.common.*;
import star.vis.*;


public class runAllFluxesMyF_LED extends StarMacro {

  public void execute() {
    execute0();
  }

  public void createMonitors(Simulation SIM)
  {
    myCase myC = new myCase(SIM);
    myPost myP = new myPost(SIM);

    String prefix = myC.dirname();
    String simTitle = myC.title();

    SIM.println("WKN --> "+prefix+" "+myC.dirname());

    String inletRegionName = "box_cab";

    List<String> sectionFiles = myC.findFile(prefix,"section.*stl");

    Units units_mm = ((Units) SIM.getUnitsManager().getObject("mm"));
    Units units_m = ((Units) SIM.getUnitsManager().getObject("m"));

    try {

        FileWriter outFile = new FileWriter(myC.fullPathNoExt()+".monitors");
        BufferedWriter out = new BufferedWriter(outFile);

        for (String sectionFile: sectionFiles)
        {
            String sectionName = myC.basenameNoExt(sectionFile);
            ArbitrarySection section = myP.importArbitrary(sectionFile, units_mm);
            String reportString = sectionName+" total pressure mavg";
            double pTotMAvg = myP.surfaceMassFlowAverage(reportString,section,"TotalPressure");
            SIM.println("Report --> " + reportString+" = "+ pTotMAvg);
            out.write(reportString+" = "+ pTotMAvg+"\n");
        }

        //String inletRegionName = promptUserForInput("Inlet in which region?", "Insert region name");
        Region inletRegion = SIM.getRegionManager().getRegion(inletRegionName);
        List<Boundary> inletBoundary = myC.getBoundaries(inletRegion,"inlet");
        double inletPTotMAvg = myP.surfaceMassFlowAverage("Inlet mass flow avg", inletBoundary,  "TotalPressure");
        SIM.println("Report --> " + "Inlet total pressure mavg = "+ inletPTotMAvg);
        out.write("Inlet total pressure mavg = "+ inletPTotMAvg+"\n");
        out.close();

    } catch(IOException e) {}
  }

  private void execute0() {

    double[] massFluxes = {0.57,0.75,0.82};

    Simulation SIM = getActiveSimulation();

    myCase myC = new myCase(SIM);

    Solution sol = SIM.getSolution();
    sol.initializeSolution();

    String simFile = SIM.getSessionPath();
    String simPath  = myC.dirname();
    String simFileName = myC.fullPath();
    String simTitle = myC.title();

    myC.matchCsysToPorousResistance("Cylind", "pipe_filter");

    int N_TIMESTEPS=1500;

    System.out.println("About to start session: " + simFileName);
    System.out.println("Session folder        : " + simPath);

    SimulationIterator Iterator = SIM.getSimulationIterator();

    double startElapsedTime = Iterator.getElapsedTime();
    double startCpuTime = Iterator.getCpuTime();

    createMonitors(SIM);

    for ( double flux: massFluxes )
    {
        for ( Region r: SIM.getRegionManager().getRegions() )
        {
            myC.setInletMassFlux( r.getPresentationName(),"inlet", flux);
            myC.setWall(r.getPresentationName(),"inlet_led");
            myC.setPressureOutlet(r.getPresentationName(),"outlet",0.0);
        }
        SIM.getSimulationIterator().step(N_TIMESTEPS);
        SIM.saveState(simPath+"/"+simTitle+"_"+flux+"_FINISHED.sim");
    }

    double elapsedTime = Iterator.getElapsedTime() - startElapsedTime;
    double cpuTime = Iterator.getCpuTime() - startCpuTime;
    System.out.printf("Iterator timer: Elapsed time = %e s, CPU time = %e s\n",elapsedTime,cpuTime);
  }
}
