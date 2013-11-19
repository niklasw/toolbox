// STAR-CCM+ macro: start.java
// Auth: sssler@scania.com, modified by konwkn@scania.com
package NCG_FAI.run;


import star.common.*;

import myFunctions.*;



public class runAllFluxesMyF extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    double[] massFluxes = {0.57,0.75,0.82};

    Simulation SIM = getActiveSimulation();

    myCase myC = new myCase(SIM);
    myMeshing myM = new myMeshing(SIM);

    myM.createMesh(true);

    Solution sol = SIM.getSolution();
    sol.initializeSolution();

    String simFile = SIM.getSessionPath();
    String simPath  = myC.dirname();
    String simFileName = myC.fullPath();
    String simTitle = myC.title();

    int N_TIMESTEPS=2000;

    System.out.println("About to start session: " + simFileName);
    System.out.println("Session folder        : " + simPath);

    SimulationIterator Iterator = SIM.getSimulationIterator();

    double startElapsedTime = Iterator.getElapsedTime();
    double startCpuTime = Iterator.getCpuTime();

    for ( double flux: massFluxes )
    {
        for ( Region r: SIM.getRegionManager().getRegions() )
        {
            myC.setInletMassFlux( r.getPresentationName(),"inlet_eye", flux);
            //myC.setWall(r.getPresentationName(),"inlet_led");
            myC.setPressureOutlet(r.getPresentationName(),"tp_extrusion_outlet",0.0);
        }
        SIM.getSimulationIterator().step(N_TIMESTEPS);
        SIM.saveState(simPath+"/"+simTitle+"_"+flux+"_FINISHED.sim");
    }

    double elapsedTime = Iterator.getElapsedTime() - startElapsedTime;
    double cpuTime = Iterator.getCpuTime() - startCpuTime;
    System.out.printf("Iterator timer: Elapsed time = %e s, CPU time = %e s\n",elapsedTime,cpuTime);
  }
}
