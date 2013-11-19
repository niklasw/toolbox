// STAR-CCM+ macro: start.java
// Auth: sssler@scania.com, modified by konwkn@scania.com
package Exhaust_Bus;


import General.*;
import myFunctions.*;
import star.common.*;

public class runSimulation extends StarMacro {

  public void execute() {
    execute0();
  }

  private double M(double m) {
	  return m/3600;
  }

  private double C(double K) {
	  return K+273.15;
  }

  private void execute0() {

    double[] massFluxes = 
    {
 	M(164.8),
	M(226.0),
	M(993.2),
	M(382.1)
    };


    double[] massFluxesAir =
    {
	M(0),
	M(145.5),
	M(705.1),
	M(184.9)
    };

    double[] temperatures = 
    {
        C(312.5),
        C(548.2),
	C(568.0),
	C(500)
    };

    Simulation sim = getActiveSimulation();

    myCase myC = new myCase(sim);
    myRunControl myRun = new myRunControl(sim);

    //myMeshing myM = new myMeshing(sim);
    //myM.createMesh(true);

    Solution sol = sim.getSolution();
    sol.initializeSolution();

    String simFile = sim.getSessionPath();
    String simPath  = myC.dirname();
    String simFileName = myC.fullPath();
    String simTitle = myC.title();

    int N_PRESTEPS = 500;
    int maxStepsIncrease = 3000;
    myRun.setDefaultMaximumSteps(4000);

    System.out.println("About to start session: " + simFileName);
    System.out.println("Session folder        : " + simPath);

    SimulationIterator Iterator = sim.getSimulationIterator();

    double startElapsedTime = Iterator.getElapsedTime();
    double startCpuTime = Iterator.getCpuTime();

    int monitorSpan = 250;
    double monitorStdDev = 5;

    int fluxI = 0;
    for ( double flux: massFluxes )
    {
        MonitorIterationStoppingCriterion MStop = myRun.createMonitorStdDevStopper
	    				      ( "Temperature_Ground Monitor",
						monitorSpan,
						monitorStdDev);
        double temp = temperatures[fluxI];
        double airFlux = massFluxesAir[fluxI];

        for ( Region r: sim.getRegionManager().getRegions() )
        {
	    String rName = r.getPresentationName();
            myC.setInletMassFlux( rName,"massflow_inlet", flux);

	    if (airFlux != 0)
	    {
            	myC.setInletMassFlux( rName,"ambient_massflow_inlet", airFlux);
	    } else
	    {
		myC.setWall(rName,"ambient_massflow_inlet");
	    }

            myC.setInletTemperature( rName,"massflow_inlet", temp,"K");

	    myC.setStagnationInlet( rName, "ambient_stagnation_inlet", 0.0);
        }

		myC.writeSummary();

        sim.getSimulationIterator().step(N_PRESTEPS);

	boolean converged = myRun.runWithMonitorStopper(MStop);

	if (converged == false) {
	    myC.Warning("Solution did not converge");
	} else {
	    myC.Info("Converged due to monitor stopper.");
	}

        sim.saveState(simPath+"/"+simTitle+"_run_"+fluxI+"_FINISHED.sim");

        fluxI++;

	myRun.increaseDefaultMaximumSteps(maxStepsIncrease);
    }

    double elapsedTime = Iterator.getElapsedTime() - startElapsedTime;
    double cpuTime = Iterator.getCpuTime() - startCpuTime;
    System.out.printf("Iterator timer: Elapsed time = %e s, CPU time = %e s\n",elapsedTime,cpuTime);
  }
}
