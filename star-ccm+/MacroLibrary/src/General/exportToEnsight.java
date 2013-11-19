/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package General;
import java.util.*;
import myFunctions.*;
import star.common.*;

/**
 *
 * @author konwkn
 */
public class exportToEnsight extends StarMacro {

	public void execute() {
    		execute0();
  	}

	private void execute0() {

   		Simulation simulation = getActiveSimulation();

   		myCase myC = new myCase(simulation);
		myExport myEx = new myExport(simulation);

   		myC.Info("pwd() =           ",myC.pwd());
   		myC.Info("exportPath() =       ",myEx.path("Ensigth",".case"));

		String[] scalarFields = {
			"Pressure",
			"Temperature",
			"TotalPressure",
			"TurbulentViscosity"
		};

		String[] vectorFields = {
			"Velocity"
		};

		List<String> sFields = Arrays.asList(scalarFields);
		List<String> vFields = Arrays.asList(vectorFields);

		myC.Info("Exporting to Ensight data."+vFields+sFields);
		myEx.toEnsight(sFields, vFields);
	}
	
}
