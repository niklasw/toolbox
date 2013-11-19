// STAR-CCM+ macro: t.java
package myFunctions;

import java.util.*;
import star.common.*;
import star.base.report.*;

public class myRunControl extends myCase {

    //Simulation sim;

    public myRunControl(Simulation s) {
	super(s);
    }

    public void setDefaultMaximumSteps(int nSteps){
	    StepStoppingCriterion crit = ((StepStoppingCriterion)
		    sim.getSolverStoppingCriterionManager().getSolverStoppingCriterion("Maximum Steps"));
	    crit.setMaximumNumberSteps(nSteps);
    }

    public void increaseDefaultMaximumSteps(int nSteps){
	    StepStoppingCriterion crit = ((StepStoppingCriterion)
		    sim.getSolverStoppingCriterionManager().getSolverStoppingCriterion("Maximum Steps"));
	    int currentN = crit.getMaximumNumberSteps();
	    crit.setMaximumNumberSteps(currentN+nSteps);
    }

    // Stopping criteria manipulators

    public MonitorIterationStoppingCriterion createMonitorStdDevStopper(String monitorName, int nSamples, double stdDev){

	Collection<Monitor> monitors = sim.getMonitorManager().getMonitors();

	for (Monitor M: monitors){
		String name = M.getPresentationName();
		String stopperName = name+"_myCriterion";
		if (name.matches(monitorName)){
			Info("Created monitor stopping criteria "+ name);

			/* Delete first, if exists, to reset all values hard*/
			if (sim.getSolverStoppingCriterionManager().has(stopperName)) {
				MonitorIterationStoppingCriterion stopper;
				stopper = ((MonitorIterationStoppingCriterion) 
					  sim.getSolverStoppingCriterionManager().getSolverStoppingCriterion(stopperName));
				sim.getSolverStoppingCriterionManager().deleteSolverStoppingCriterion(stopper);
			}

	   		MonitorIterationStoppingCriterion crit = M.createIterationStoppingCriterion();

			crit.setPresentationName(stopperName);

			( (MonitorIterationStoppingCriterionOption)
				crit.getCriterionOption()
			).setSelected(MonitorIterationStoppingCriterionOption.STANDARD_DEVIATION);

			crit.setIsUsed(false);

			MonitorIterationStoppingCriterionStandardDeviationType devType;
			devType = ((MonitorIterationStoppingCriterionStandardDeviationType) crit.getCriterionType());

        		devType.getStandardDeviation().setValue(stdDev);
        		devType.setNumberSamples(nSamples);
			return crit;
		}
	}	
	Info("Did not find monitor for stopper by name "+ monitorName);
	return null;
    }

    public void activateMonitorStopper(MonitorIterationStoppingCriterion M, boolean onoff){
	
	    if (onoff) {
	 	Info("Activating monitorStopper");
	    } else {
	 	Info("Deactivating monitorStopper");
	    }
	 M.setOuterIterationCriterion(onoff);
	 M.setInnerIterationCriterion(onoff);
	 M.setIsUsed(onoff);
    }

    public boolean runWithMonitorStopper(MonitorIterationStoppingCriterion M, int nSteps) {
	    /*
	     * Take nSteps step and then evaluate monitor. If satisfied, return
	     * satisfaction.
	     * DOES NOT SEEM TO WORK. Ignores stopper?
	     */
	    boolean satisfied = false;
	    activateMonitorStopper(M, true);
	    while (! satisfied )
	    {
		Info("Monitor stopper not yet satisfied. Stepping another "+nSteps);
	    	sim.getSimulationIterator().step(nSteps);
	    	satisfied = M.getIsSatisfied();
	    }
       	    activateMonitorStopper(M, false);
	    return satisfied;
    }

    public boolean runWithMonitorStopper(MonitorIterationStoppingCriterion M) {
	    activateMonitorStopper(M, true);
	    sim.getSimulationIterator().run();
	    M.getIsSatisfied();
	    boolean satisfied = M.getIsSatisfied();
	    activateMonitorStopper(M, false);
	    return satisfied;
    }

	public void setMonitorFrequency(String name, int frq) {

		Monitor mon = ((Monitor) sim.getMonitorManager().getMonitor(name));
    	mon.setUpdateFrequency(frq);
	}

	public void setMonitorsFrequencyByPattern(String pattern, int frq) {
		Collection<Monitor> monitors = sim.getMonitorManager().getMonitors();

		for (Monitor mon: monitors) {
			String monitorName = mon.getPresentationName();
			if (monitorName.matches(pattern))
			{
				Info("Changed frequency of monitor "+monitorName+" to "+frq);
				mon.setUpdateFrequency(frq);	
			}
		}
	}


}