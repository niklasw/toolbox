// STAR-CCM+ macro: start.java
// Auth: sssler@scania.com, modified by konwkn@scania.com
package General;


import myFunctions.*;
import star.common.*;

public class runSimulation extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    double[] massFluxes = {0.1778,0.513};
    double[] temperatures = {573, 713};
    Simulation SIM = getActiveSimulation();

    myCase myC = new myCase(SIM);

    //myMeshing myM = new myMeshing(SIM);
    //myM.createMesh(true);

    Solution sol = SIM.getSolution();
    sol.initializeSolution();

    String simFile = SIM.getSessionPath();
    String simPath  = myC.dirname();
    String simFileName = myC.fullPath();
    String simTitle = myC.title();

    int N_TIMESTEPS=3000;

    System.out.println("About to start session: " + simFileName);
    System.out.println("Session folder        : " + simPath);

    SimulationIterator Iterator = SIM.getSimulationIterator();

    double startElapsedTime = Iterator.getElapsedTime();
    double startCpuTime = Iterator.getCpuTime();

    int fluxI = 0;
    for ( double flux: massFluxes )
    {
        double temp = temperatures[fluxI];
        for ( Region r: SIM.getRegionManager().getRegions() )
        {
            myC.setInletMassFlux( r.getPresentationName(),"inlet", flux);
            myC.setInletTemperature( r.getPresentationName(),"inlet", temp,"K");
            //myC.setWall(r.getPresentationName(), "wall");
            //myC.setPressureOutlet(r.getPresentationName(),"tp_extrusion_outlet",0.0);
        }
        SIM.getSimulationIterator().step(N_TIMESTEPS);
        SIM.saveState(simPath+"/"+simTitle+"_"+flux+"_"+temp+"_FINISHED.sim");
        fluxI++;
    }

    double elapsedTime = Iterator.getElapsedTime() - startElapsedTime;
    double cpuTime = Iterator.getCpuTime() - startCpuTime;
    System.out.printf("Iterator timer: Elapsed time = %e s, CPU time = %e s\n",elapsedTime,cpuTime);
  }
}
