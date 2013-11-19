/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package General;
import star.common.*;
import star.vis.*;
import star.base.neo.*;

import myFunctions.*;

/**
 *
 * @author konwkn
 */
public class postScalarSection extends StarMacro {

	public void execute() {
    		execute0();
  	}

	private void execute0() {

   		Simulation simulation = getActiveSimulation();

   		myCase myC = new myCase(simulation);
		myPost myP = new myPost(simulation);

   		myC.Info("pwd() =           ",myC.pwd());
   		myC.Info("dirname() =       ",myC.dirname());
   		myC.Info("directoryname() = ",myC.directoryname());
   		myC.Info("basename() =      ",myC.basename());
   		myC.Info("title() =         ",myC.title());

		Scene S = myP.createNewScene("PlaneScene");
		//myP.showAllRegions(S, true);
		myP.showRegion("upstream", S, true);
		myP.removeLogo(S);
		
		double[] normal = new double[]{0,1,0};
		double[] origin = new double[]{-0.9,0.54,0.25};

		PlaneSection P = myP.createPlaneSection(S, "Plane Section", normal, origin);
    		ScalarDisplayer displayer = ((ScalarDisplayer) S.getDisplayerManager().getDisplayer("Scalar 1"));
		myP.setScalarField(displayer , "Velocity", 0, 70, "m/s");

		CurrentView V = S.getCurrentView();

                V.setInput(
			new DoubleVector(new double[] {-0.75, 0.0, 0.31}),
			new DoubleVector(new double[] {-0.75, 0.5, 0.31}),
			new DoubleVector(new double[] {0,0,1}),
			0.07, 1);

	}
	
}
