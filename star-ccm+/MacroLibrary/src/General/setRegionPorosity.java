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
public class setRegionPorosity  extends StarMacro {
	
	
  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation SIM = getActiveSimulation();

    myCase myC = new myCase(SIM);

    String porousRegion = "filter";
    // FAI Systems settings (UFI)
    double v = 217;
    double i = 6350;

    // double[] inertial = new double[]{6350, 63500, 6350};
    // double[] viscous = new double[]{217,2170,217};

    // Donaldson 200/300
    //double v = 2547;
    //double i = 420;

    // Donaldson 400
    // double v = 2397;
    // double i = 383;


    double[] viscous  = new double[]{v, v*100, v/2};
    double[] inertial = new double[]{i, i*100, i/2};

    // Mann Hummel
    //double[] viscous  = new double[]{1638, 30000, 800};
    //double[] inertial = new double[]{508,0,0};

    myC.matchCsysToPorousResistance("Cylindric","filter");
    myC.setPorousResistance("filter", inertial, viscous);
  }

}

