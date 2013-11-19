// STAR-CCM+ macro: setMonitorFrq.java
package Truck_Exhaust;


import star.common.*;
import star.base.report.*;

public class setMonitorFrq extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation_0 = 
      getActiveSimulation();

    ReportMonitor reportMonitor_6 = 
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("Pipe outlet mass flow avg Monitor"));

    reportMonitor_6.setUpdateFrequency(5);

    ReportMonitor reportMonitor_7 = 
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("Silencer inlet mass flow avg Monitor"));

    reportMonitor_7.setUpdateFrequency(5);

    ReportMonitor reportMonitor_8 = 
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("Silencer outlet mass flow avg Monitor"));

    reportMonitor_8.setUpdateFrequency(5);

    //simulation_0.saveState(resolvePath("/home/fluidsim/Internal_Flow/261571_Eu6_Exhaust_outlet_pipes/PRE/Mesh/Generalised/B2/B2@01000.sim"));
  }
}
