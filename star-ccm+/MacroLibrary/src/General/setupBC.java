// STAR-CCM+ macro: start.java
// Auth: sssler@scania.com, modified by konwkn@scania.com
package General;


import myFunctions.*;
import star.common.*;

public class setupBC extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    double[] massFluxes = {0.45,0.57,0.63};
    double inletTemperature = 700;

    Simulation SIM = getActiveSimulation();

    myCase myC = new myCase(SIM);

    Solution sol = SIM.getSolution();
    sol.initializeSolution();

    String simFile = SIM.getSessionPath();
    String simPath  = myC.dirname();
    String simFileName = myC.fullPath();
    String simTitle = myC.title();

    int N_TIMESTEPS=2000;

    System.out.println("About to start session: " + simFileName);
    System.out.println("Session folder        : " + simPath);

    for ( double flux: massFluxes )
    {
	double haiPressure = -3080*flux*flux;
        for ( Region r: SIM.getRegionManager().getRegions() )
        {
	    String rname = r.getPresentationName();
            myC.setInletMassFlux( rname,"inlet", flux);
            myC.setWall(rname,"wall");
            myC.setPressureOutlet(rname, "ambience",0.0);
            myC.setSlipWall(rname,"behind");
            myC.setSlipWall(rname,"ambience_max");
            myC.setSlipWall(rname,"ambience_min");
	    myC.setStagnationInlet(rname, "inlet_ejector", haiPressure);
	    myC.setInletTemperature(rname, "inlet_exh", inletTemperature,"K");
        }
    }
  }
}
