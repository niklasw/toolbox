// STAR-CCM+ macro: start.java
// Auth: sssler@scania.com, modified by konwkn@scania.com
package Truck_Exhaust;

import java.io.*;

import star.common.*;
import star.metrics.*;


public class starccmStart extends StarMacro {

  public void execute() {
    execute0();
  }

  private void setCellQualityRemedy(Simulation sim, String continua)
  {
    PhysicsContinuum physCont = ((PhysicsContinuum) sim.getContinuumManager().getContinuum(continua));
    physCont.enable(CellQualityRemediationModel.class);
  }


  private void execute0() {
    String CWD = System.getProperty("user.dir");
    Simulation SIM = getActiveSimulation();

    new star.common.SimulationSummaryReporter().report(getActiveSimulation(), resolvePath(SIM.getPresentationName()+".html"));

    String simFile = SIM.getSessionPath();
    String simPath  = SIM.getSessionDir();
    String simFileName = (new File(simFile)).getName();

    String simTitle = simFileName.substring(0,simFileName.lastIndexOf("."));

    setCellQualityRemedy(SIM,"Physics 1");

    AbortFileStoppingCriterion abortFileStoppingCriterion_0 = 
      ((AbortFileStoppingCriterion) SIM.getSolverStoppingCriterionManager().getSolverStoppingCriterion("Stop File"));

    abortFileStoppingCriterion_0.setIsUsed(false);
      // Do we want to start starccm without run?
      // Do we want to force auto-save?
    int N_TIMESTEPS=2000;

    /* Maby add forced autosave? First check if already set by user...
    AutoSave autoSave_0 = SIM.getSimulationIterator().getAutoSave();

    autoSave_0.setEnabled(true);

    autoSave_0.getTriggerOption().setSelected(AutoSaveTriggerOption.TIME_STEP);

    autoSave_0.setTriggerFrequency(N_TIMESTEPS/4);
    */
    System.out.println("About to start session: " + simFileName);
    System.out.println("Dir: " + SIM.getSessionDir());

    Solution sol = SIM.getSolution();
    sol.initializeSolution();

    SimulationIterator Iterator = (SimulationIterator) SIM.getSimulationIterator();

    double prevElapsedTime = Iterator.getElapsedTime();
    double prevCpuTime = Iterator.getCpuTime();

    if ( N_TIMESTEPS <= 0) {
        Iterator.run();
    }
    else
    {
        Iterator.step(N_TIMESTEPS);
    }

    double elapsedTime = Iterator.getElapsedTime() - prevElapsedTime;
    double cpuTime = Iterator.getCpuTime() - prevCpuTime;
    System.out.printf("Iterator timer: Elapsed time = %e s, CPU time = %e s\n",elapsedTime,cpuTime);
  }

}
