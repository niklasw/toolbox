// STAR-CCM+ macro: setupBC.java
package Truck_Exhaust;


import star.turbulence.*;
import star.common.*;
import star.flow.*;
import star.energy.*;

public class setupBC_large extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {


    String inletBoundary = "Silencer.inletsfromscr";
    String outletBoundary = "Ambience_merged.";
    //double massFlow = 0.504;
    //double inletT   = 729;
    double massFlow = 0.63;
    double inletT   = 723;
    double ti       = 0.01;
    double viscRat  = 10.0;

    Simulation simulation_0 = getActiveSimulation();

    Region region_0 = simulation_0.getRegionManager().getRegion("Region 1");

    Boundary boundary_0 = region_0.getBoundaryManager().getBoundary(outletBoundary);

    boundary_0.setBoundaryType(PressureBoundary.class);

    Boundary boundary_2 = region_0.getBoundaryManager().getBoundary(inletBoundary);

    boundary_2.setBoundaryType(MassFlowBoundary.class);

        MassFlowRateProfile massFlowRateProfile_0 = boundary_2.getValues().get(MassFlowRateProfile.class);

        massFlowRateProfile_0.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(massFlow);

    TotalTemperatureProfile totalTemperatureProfile_0 = boundary_2.getValues().get(TotalTemperatureProfile.class);

        totalTemperatureProfile_0.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(inletT);

    TurbulenceIntensityProfile turbulenceIntensityProfile_0 = boundary_2.getValues().get(TurbulenceIntensityProfile.class);

        turbulenceIntensityProfile_0.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(ti);

        TurbulentViscosityRatioProfile turbulentViscosityRatioProfile_0 = boundary_2.getValues().get(TurbulentViscosityRatioProfile.class);

        turbulentViscosityRatioProfile_0.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(viscRat);
  }
}
