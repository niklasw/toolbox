// STAR-CCM+ macro: tmp.java
package General;


import star.common.*;

import myFunctions.*;

public class cleanWrap extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {
    myMeshing myF = new myMeshing(getActiveSimulation());
    myF.cleanWrap();
  }
}
