// STAR-CCM+ macro: setupDefaultRunOptions.java
package Truck_Exhaust;


import star.common.*;

public class setupDefaultRunOptions extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    int autoFrq = 500;
    int autoN   = 1;
    Simulation simulation_0 = getActiveSimulation();

    AutoSave autoSave_0 = simulation_0.getSimulationIterator().getAutoSave();

    autoSave_0.setEnabled(true);

    autoSave_0.setTriggerFrequency(autoFrq);

    autoSave_0.setMaxAutosavedFiles(autoN);
    simulation_0.println("Autosave every =                 "+autoFrq);
    simulation_0.println("Keep number of autosaved files = "+autoN);

    StepStoppingCriterion stepStoppingCriterion_0 = ((StepStoppingCriterion) simulation_0.getSolverStoppingCriterionManager().getSolverStoppingCriterion("Maximum Steps"));

    int currentMaxSteps = stepStoppingCriterion_0.getMaximumNumberSteps();
    currentMaxSteps += 1000;
    stepStoppingCriterion_0.setMaximumNumberSteps(currentMaxSteps);

    currentMaxSteps = stepStoppingCriterion_0.getMaximumNumberSteps();
    simulation_0.println("Current stepStoppingCriterion =  "+currentMaxSteps);
  }
}
