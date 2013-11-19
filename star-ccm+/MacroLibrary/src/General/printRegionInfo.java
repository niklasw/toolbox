/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package General;

import java.util.*;
import star.common.*;
import myFunctions.*;

/**
 *
 * @author konwkn
 */
public class printRegionInfo extends StarMacro {

	public void execute() {
    		execute0();
  	}

	private void execute0() {

   		Simulation simulation = getActiveSimulation();

   		myCase myC = new myCase(simulation);

   		myC.Info("pwd() =           ",myC.pwd());
   		myC.Info("dirname() =       ",myC.dirname());
   		myC.Info("directoryname() = ",myC.directoryname());
   		myC.Info("basename() =      ",myC.basename());
   		myC.Info("title() =         ",myC.title());

		Collection<Region> regions;
		regions = simulation.getRegionManager().getRegions();

		myC.Info("\nBEGIN: Region and bounday info");
		for (Region r: regions){

			List<Boundary> boundaries;
			boundaries = myC.getBoundaries(r, ".*");

			myC.Info("Region ",r.getPresentationName());
			for (Boundary b: boundaries) {
				myC.Info("\tBoundary:",b.getPresentationName());
			}
		}
		myC.Info("\nEND: Region and bounday info\n");
	}
	
}
