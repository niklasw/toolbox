package General;

import star.common.*;

import myFunctions.*;

/**
 *
 * @author konwkn
 */
public class makeRegionFeatures extends StarMacro{

  public void execute() {
    execute0();
  }

  private void execute0(){
	Simulation sim = getActiveSimulation();
	myMeshing myF = new myMeshing(sim);
	myF.clearFeaturesOnRegions();
	myF.createFeaturelinesOnRegions(75);
  }
}
