// STAR-CCM+ macro: start.java
// Auth: sssler@scania.com, modified by konwkn@scania.com
package macro;

import java.util.*;
import java.io.*;

import star.common.*;
import star.base.neo.*;
import star.vis.*;
import star.flow.*;
import star.prismmesher.*;
import star.meshing.*;



public class runAllFluxesStart extends StarMacro {

  public void execute() {
    execute0();
  }

  Collection<Boundary> getBoundaries(Simulation sim, Region region, String boundaryString)
  {
        List<Boundary> bnds = new ArrayList(region.getBoundaryManager().getBoundaries());
        List<Boundary> keepBnds = new ArrayList();
        for ( Boundary b: bnds )
        {
            if (b.getPresentationName().contains(boundaryString))
            {
                keepBnds.add(b);
            }
        }
        if ( keepBnds.isEmpty() )
        {
            sim.println("WKN--> Could not find any boundary containing name "+boundaryString+" in region "+region.getPresentationName());
        }
        return keepBnds;
  }

  public void setInletMassFlux(String regionName, String boundaryName, double value)
  {
        Simulation sim = getActiveSimulation();
        Region region = sim.getRegionManager().getRegion(regionName);

        Collection<Boundary> bnds = getBoundaries(sim, region, boundaryName);

        if ( bnds != null )
        {

        for ( Boundary b: bnds )
        {
            try {
                b.setBoundaryType(MassFlowBoundary.class);
                MassFlowRateProfile profile = b.getValues().get(MassFlowRateProfile.class);
                profile.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(value);
                sim.println("WKN--> Did set mass flow rate condition for "+ b.getPresentationName()+" in region "+region.getPresentationName());
            }
            catch(NeoException e) {
                sim.println("WKN--> Could not set boundary condition for "+ b.getPresentationName());
            }
        }
        }
  }

    public void setWall(Region region, String bString)
    {
        Simulation sim = getActiveSimulation();
        for (Boundary b : getBoundaries(sim, region, bString)) {
            try {
                b.setBoundaryType(WallBoundary.class);
                sim.println("WKN--> Did set wall condition for " + b.getPresentationName() + " in region " + region.getPresentationName());
            } catch (NeoException e) {
                sim.println("WKN--> Could not set boundary condition for " + b.getPresentationName());
            }
        }
    }

    public void setPressureOutlet(Simulation sim, String regionName, String bString, double value)
    {

        Region region = sim.getRegionManager().getRegion(regionName);

        for (Boundary b : getBoundaries(sim, region, bString)) {
            try {
                b.setBoundaryType(PressureBoundary.class);
                StaticPressureProfile profile = b.getValues().get(StaticPressureProfile.class);
                profile.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(value);
                sim.println("WKN--> Did set pressure outlet condition for " + b.getPresentationName() + " in region " + region.getPresentationName());
            } catch (NeoException e) {
                sim.println("WKN--> Could not set boundary condition for " + b.getPresentationName());
            }
        }
    }


  private void execute0() {

    double[] massFluxes = {0.82,0.75,0.57};

    Simulation SIM = getActiveSimulation();

    Solution sol = SIM.getSolution();
    sol.initializeSolution();

    String simFile = SIM.getSessionPath();
    String simPath  = SIM.getSessionDir();
    String simFileName = (new File(simFile)).getName();
    String simTitle = simFileName.substring(0,simFileName.lastIndexOf("."));

    int N_TIMESTEPS=1000;

    System.out.println("About to start session: " + simFileName);
    System.out.println("Session folder        : " + SIM.getSessionDir());

    SimulationIterator Iterator = SIM.getSimulationIterator();

    double startElapsedTime = Iterator.getElapsedTime();
    double startCpuTime = Iterator.getCpuTime();

    for ( double flux: massFluxes )
    {
        for ( Region r: SIM.getRegionManager().getRegions() )
        {
            setInletMassFlux( r.getPresentationName(),"inlet", flux);
            setWall(r,"inlet_led");
            setPressureOutlet(SIM,r.getPresentationName(),"outlet",0.0);
        }
        SIM.getSimulationIterator().step(N_TIMESTEPS);
        SIM.saveState(simPath+"/"+simTitle+"_"+flux+"_FINISHED.sim");
    }

    double elapsedTime = Iterator.getElapsedTime() - startElapsedTime;
    double cpuTime = Iterator.getCpuTime() - startCpuTime;
    System.out.printf("Iterator timer: Elapsed time = %e s, CPU time = %e s\n",elapsedTime,cpuTime);
  }
}
