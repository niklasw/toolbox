/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package General;

import star.common.*;
import java.util.*;
import star.vis.*;
import star.base.neo.*;
import myFunctions.*;

/**
 *
 * @author konwkn
 */
public class postIsoTerms extends StarMacro {

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

		Scene S = myP.createNewScene("PlaneScene");
		myP.showAllRegions(S, true);
		myP.removeLogo(S);

   		myC.Info("title() =         ",myC.title());

		for (Region r: myP.getRegions(".*")){
			myP.showGeomBoundaries(r.getPresentationName(), S, "(.*wall.*|.*ground.*)");
		}

		myP.setVolumeRepresentation(S);
		
		CurrentView V = S.getCurrentView();

  		ScalarDisplayer displayer = ((ScalarDisplayer) S.getDisplayerManager().getDisplayer("Scalar 1"));

		myP.showAllRegions(S,false);

		myP.setScalarField(displayer, "Temperature", 473.15, 673.15, "C");

		V.setInput(new DoubleVector(new double[] {-0.5799177950929202, 0.6193630281389801, -0.5531213154242184}),
				   new DoubleVector(new double[] {5.826556655489373, 3.7689740828952076, 1.615573133908372}),
				   new DoubleVector(new double[] {-0.2521626418453628, -0.14579104018617442, 0.9566394172618023}),
				   0.6796060746661083,
				   1);

		/*
		IsoPart isoPart_1 = ((IsoPart) simulation.getPartManager().getObject("iso 300 C"));

    	IsoPart isoPart_2 = ((IsoPart) simulation.getPartManager().getObject("iso 400 C"));

    	IsoPart isoPart_3 = ((IsoPart) simulation.getPartManager().getObject("iso 200 C"));
		*/

		IsoPart isoPart = myP.createIsoSurface("Temperature", new double[] {200,300,400},"C");

    	displayer.getParts().setObjects(isoPart);

		displayer.setOpacity(0.4);

		String imgFileName = myP.fullPathNoExt()+"isoTerms.png";
		myP.Info("WKN --> Saving image "+ imgFileName);
		int xrez = 2000;
		int yrez = 1500;
		S.printAndWait(imgFileName,1,xrez,yrez);

		myC.Info("END");

	};
}
