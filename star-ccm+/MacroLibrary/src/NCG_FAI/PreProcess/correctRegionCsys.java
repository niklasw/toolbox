/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package NCG_FAI.PreProcess;

import java.util.*;

import star.common.*;

import myFunctions.*;



/**
 *
 * @author konwkn
 */
public class correctRegionCsys  extends StarMacro {
	
	
  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation SIM = getActiveSimulation();

    myCase myC = new myCase(SIM);

    myC.matchCsysToPorousResistance("Cylindric","filter");
  }

}

