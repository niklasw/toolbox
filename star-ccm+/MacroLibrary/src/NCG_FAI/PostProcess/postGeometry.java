/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package NCG_FAI.PostProcess;

import java.util.*;

import star.common.*;
import star.base.neo.*;
import star.vis.*;

import myFunctions.*;

/**
 *
 * @author konwkn
 */
public class postGeometry extends StarMacro{

	public void execute() {
    		execute0();
  	}

	private void execute0() {
		
		Simulation sim = getActiveSimulation();
		myPost myP = new myPost(sim);

		
		Scene scene_1 = sim.getSceneManager().getScene("postGeometry");
		String sceneName = scene_1.getPresentationName();
	        String imgFileName = "";
		int xrez = 2000;
		int yrez = 2000;
		CurrentView currentView_0 = scene_1.getCurrentView();

                currentView_0.setInput(
			new DoubleVector(new double[] {-0.840, 0.960, 0.195}),
			new DoubleVector(new double[] {0.448, 2.240, 0.830}),
			new DoubleVector(new double[] {-0.208, -0.259, 0.943}),
			0.5, 1);

	        imgFileName = myP.fullPathNoExt()+sceneName+"_view1.png"; 
        	sim.println("WKN --> Saving image "+ imgFileName);
        	scene_1.printAndWait(imgFileName,1,xrez,yrez);

    		currentView_0.setInput(
			new DoubleVector(new double[] {-1.110, 0.608, 0.318}),
			new DoubleVector(new double[] {-2.026, -0.341, 1.300}),
			new DoubleVector(new double[] {0.549, 0.284, 0.786}),
			0.5, 1);

	        imgFileName = myP.fullPathNoExt()+sceneName+"_view2.png"; 
        	sim.println("WKN --> Saving image "+ imgFileName);
        	scene_1.printAndWait(imgFileName,1,xrez,yrez);

		/*
		myP.clearScenes();


		scene_1 = myP.createNewScene("postGeometry");

		myP.removeLogo(scene_1);

		myP.showAllRegions(scene_1, true);

		List<Region> extrusion = myP.getRegions(".*Extrusion.*");
		List<Region> deleted = myP.getRegions(".*deleted.*");
			
		for (Region r: extrusion) { myP.Info(r.getPresentationName()); myP.showRegion(r.getPresentationName(), scene_1, false); }
		for (Region r: deleted) { myP.Info(r.getPresentationName()); myP.showRegion(r.getPresentationName(), scene_1, false); }
		 */

	}
	


	
}
