/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package General;
import star.common.*;

import myFunctions.*;

/**
 *
 * @author konwkn
 */
public class whereAmI extends StarMacro {

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
   
	}
	
}
