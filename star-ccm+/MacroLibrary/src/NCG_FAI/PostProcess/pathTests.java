// STAR-CCM+ macro: t.java
package NCG_FAI.PostProcess;


import star.common.*;

import myFunctions.*;

public class pathTests extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation SIM = getActiveSimulation();

    myCase myC = new myCase(SIM);

    int xrez = 1250;
    int yrez = 1000;
    
    SIM.println("dirname              "+myC.dirname());
    SIM.println("PWD                  "+myC.pwd());
    SIM.println("basename             "+myC.basename());
    SIM.println("title                "+myC.title());

  }
}
