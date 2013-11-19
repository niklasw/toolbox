/*
 * STAR-CCM+ macro: dc60loc.java
 *
 * Originally Written by Mattias Chevalier 2010-02,
 * heavily modified by Niklas Wikstrom 2011-05
 *
 * Macro to compute dc60 in a predefined plane. Required input is:
 * 1.   A complete cutplane called "dc60 plane"
 *   -  The surface normal is calculated from the cut plane
 *   -  The surface centre is calculated from the cut plane
 *   -  One surface tangent vector is calculated from the cut plane
 * 1b.  A complete cutplane called "near inlet plane"
 * 2. Region name has to be "Region 1"
 *
 * The user input can be changed in the section "Reguired user input" below
 *
 * The macro computes the centre of gravity based on the plane cut defined in 1.
 * Constrained planes are then generated for a range of cuts. The macro outputs
 * the total pressure and the "dc60" for each sector as a function of angle
 *
 *
 */
package macro;

import java.util.*;
import java.io.*;

import star.common.*;
import star.base.neo.*;
import star.vis.*;
import star.base.report.*;
import star.flow.*;

//import JSci.maths.*;

public class dc60Calculator extends StarMacro {

  public void execute() {
    execute0();
  }

  public void info(Simulation SIM, String i)
  {
    //System.out.println("--> "+i);
    SIM.println("--> "+i);
  }

  public void createPlaneSection(Simulation SIM, String name, double[] normal, double[] origin) {
    DoubleVector Normal = new DoubleVector(normal);
    DoubleVector Origin = new DoubleVector(origin);
    if ( SIM.getPartManager().has(name) )
    {
        PlaneSection oldPlane = ((PlaneSection) SIM.getPartManager().getObject(name));
        SIM.getPartManager().removeObjects(oldPlane);
    }
    PlaneSection planeSection = (PlaneSection) SIM.getPartManager().createImplicitPart(new NeoObjectVector(new Object[] {}), Normal, Origin, 0, 1, new DoubleVector(new double[] {0.0}));
    planeSection.setPresentationName(name);

    Collection regions = SIM.getRegionManager().getRegions();

    planeSection.getInputParts().setObjects(regions);
  }


  public UserFieldFunction createFieldFunction(String name, String definition, IntVector dimensions, int type)
  {
    Simulation SIM = getActiveSimulation();
    if ( SIM.getFieldFunctionManager().has(name) )
    {
        UserFieldFunction func = ((UserFieldFunction) SIM.getFieldFunctionManager().getFunction(name) );
        func.setDimensionsVector(dimensions);
        func.getTypeOption().setSelected(type);
        func.setDefinition(definition);
        return func;
    }
    else
    {
        UserFieldFunction func = ((UserFieldFunction) SIM.getFieldFunctionManager().createFieldFunction());
        func.setDimensionsVector(dimensions);
        func.getTypeOption().setSelected(type);
        func.setFunctionName(name);
        func.setPresentationName(name);
        func.setDefinition(definition);
        return func;
    }
  }

  public double surfaceIntegral(String name, Simulation sim, PlaneSection sourcePlane, String scalarName)
  {
    FieldFunction field= ((FieldFunction) sim.getFieldFunctionManager().getFunction(scalarName));
    if ( ! sim.getReportManager().has(name) )
    {
        SurfaceIntegralReport report = sim.getReportManager().createReport(SurfaceIntegralReport.class);
        report.setPresentationName(name);
    }
    SurfaceIntegralReport report = ((SurfaceIntegralReport) sim.getReportManager().getObject(name));
    report.setScalar(field);
    report.getParts().setObjects(sourcePlane);
    return report.getValue();
  }

  public double surfaceIntegral(String name, Simulation sim, ConstrainedPlaneSection sourcePlane, String scalarName)
  {
    FieldFunction field= ((FieldFunction) sim.getFieldFunctionManager().getFunction(scalarName));
    if ( ! sim.getReportManager().has(name) )
    {
        SurfaceIntegralReport report = sim.getReportManager().createReport(SurfaceIntegralReport.class);
        report.setPresentationName(name);
    }
    SurfaceIntegralReport report = ((SurfaceIntegralReport) sim.getReportManager().getObject(name));
    report.setScalar(field);
    report.getParts().setObjects(sourcePlane);
    return report.getValue();
  }

  public double planeMassflowAverage(String name, Simulation sim, PlaneSection sourcePlane, String scalarName)
  {
    FieldFunction field= ((FieldFunction) sim.getFieldFunctionManager().getFunction(scalarName));
    double average;
    if ( ! sim.getReportManager().has(name) )
    {
        MassFlowAverageReport report = sim.getReportManager().createReport(MassFlowAverageReport.class);
        report.setPresentationName(name);
    }
    MassFlowAverageReport report = ((MassFlowAverageReport) sim.getReportManager().getObject(name));
    report.setScalar(field);
    report.getParts().setObjects(sourcePlane);
    average = report.getValue();
    return average;
  }

  public double planeAverage(String name, Simulation sim, PlaneSection sourcePlane, VectorComponentFieldFunction scalar)
  {
    double average;
    if ( ! sim.getReportManager().has(name) )
    {
        AreaAverageReport report = sim.getReportManager().createReport(AreaAverageReport.class);
        report.setPresentationName(name);
    }
    AreaAverageReport report = ((AreaAverageReport) sim.getReportManager().getObject(name));
    report.setScalar(scalar);
    report.getParts().setObjects(sourcePlane);
    average = report.getValue();
    return average;
  }

  public double planeAverage(String name, Simulation sim, PlaneSection sourcePlane, String scalarName)
  {
    FieldFunction field= ((FieldFunction) sim.getFieldFunctionManager().getFunction(scalarName));
    if ( ! sim.getReportManager().has(name) )
    {
        AreaAverageReport report = sim.getReportManager().createReport(AreaAverageReport.class);
        report.setPresentationName(name);
    }
    AreaAverageReport report = ((AreaAverageReport) sim.getReportManager().getObject(name));
    report.setScalar(field);
    report.getParts().setObjects(sourcePlane);
    return report.getValue();
  }

  public double planeAverage(String name, Simulation sim, ConstrainedPlaneSection sourcePlane, String scalarName)
  {
    FieldFunction field= ((FieldFunction) sim.getFieldFunctionManager().getFunction(scalarName));
    if ( ! sim.getReportManager().has(name) )
    {
        AreaAverageReport report = sim.getReportManager().createReport(AreaAverageReport.class);
        report.setPresentationName(name);
    }
    AreaAverageReport report = ((AreaAverageReport) sim.getReportManager().getObject(name));
    report.setScalar(field);
    report.getParts().setObjects(sourcePlane);
    return report.getValue();
  }


  public DoubleVector crossProduct(DoubleVector v1, DoubleVector v2)
  {
      double r0 = v1.getComponent(1)*v2.getComponent(2)-v1.getComponent(2)*v2.getComponent(1);
      double r1 = -( v1.getComponent(0)*v2.getComponent(2)-v1.getComponent(2)*v2.getComponent(0) );
      double r2 = v1.getComponent(0)*v2.getComponent(1)-v1.getComponent(1)*v2.getComponent(0);
      DoubleVector r = new DoubleVector(new double[] {r0,r1,r2});
      return r;
  }

  public double dotProduct(DoubleVector v1, DoubleVector v2)
  {
    return v1.getComponent(0)*v2.getComponent(0)+v1.getComponent(1)*v2.getComponent(1)+v1.getComponent(2)*v2.getComponent(2);
  }

  public DoubleVector normalize(DoubleVector t)
  {
    double length = Math.sqrt(dotProduct(t,t));
    t.setComponent(0,t.getComponent(0)/length);
    t.setComponent(1,t.getComponent(1)/length);
    t.setComponent(2,t.getComponent(2)/length);
    return t;
  }

  public DoubleVector tangentVector(DoubleVector planeNormal)
  {
    DoubleVector random = normalize(new DoubleVector( new double[] {0,1,0}));
    while ( dotProduct(random,planeNormal) > 0.5 )
    {
        random = normalize(new DoubleVector( new double[] {Math.random(),Math.random(),Math.random()}));
        System.out.println("Random vector"+random);
    }
    DoubleVector t = crossProduct(planeNormal,random);
    t = normalize(t);
    return t;
  }

  public DoubleVector areaCOG(Simulation SIM, PlaneSection plane)
  {
    PrimitiveFieldFunction pos = (PrimitiveFieldFunction) SIM.getFieldFunctionManager().getFunction("Position");
    VectorComponentFieldFunction p0 = (VectorComponentFieldFunction) pos.getComponentFunction(0);
    VectorComponentFieldFunction p1 = (VectorComponentFieldFunction) pos.getComponentFunction(1);
    VectorComponentFieldFunction p2 = (VectorComponentFieldFunction) pos.getComponentFunction(2);
    double c0 = planeAverage("tmp",SIM,plane,p0);
    double c1 = planeAverage("tmp",SIM,plane,p1);
    double c2 = planeAverage("tmp",SIM,plane,p2);
    DoubleVector C = new DoubleVector(new double[]{c0,c1,c2});
    return C;
  }

  public ConstrainedPlaneSection createConstrainedPlane
  (
    String name,
    Simulation SIM,
    Region region,
    DoubleVector points,
    DoubleVector cog,
    DoubleVector normal,
    Units units
  )
  {
    ConstrainedPlaneSection constrainedPlaneSection_cut;
    if ( ! SIM.getPartManager().has(name))
    {
        constrainedPlaneSection_cut =
            (ConstrainedPlaneSection) SIM.getPartManager().createConstrainedPlaneImplicitPart
            (
                new NeoObjectVector ( new Object[] {region}),
                new DoubleVector(points),
                units
            );
        constrainedPlaneSection_cut.setPresentationName(name);
    }
    else
    {
        constrainedPlaneSection_cut = ((ConstrainedPlaneSection) SIM.getPartManager().getObject(name));
        constrainedPlaneSection_cut.setLoop(points);
    }
    constrainedPlaneSection_cut.getOriginCoordinate().setValue(cog);
    constrainedPlaneSection_cut.getNormalCoordinate().setValue(normal);

    return constrainedPlaneSection_cut;
  }


  private void execute0() {

    String planeName = "dc60 plane";
    String inletPlaneName = "near inlet plane";

    Simulation SIM = getActiveSimulation();

    info(SIM,"DC60 macro running...");

    // Required user input ===============================================================

    /* Step size of sector in degrees when evaluating the distorsion coefficient
     * This might or might not need to be small. Effects have been noted for low (good)
     * DC60 values that the result is sensitive to which position the _first_ sector
     * (as defined by the dc60_tangent) start. In more distorted flows, this effect is
     * probably neglible (not as sensitive).
     **/
    double deltaangle = 5.0;

    // Scale factor on radius to make sure the complete sector is covered
    double rscale = 1.2;

    // Region to make dc60 cut in
    Region region_0 = SIM.getRegionManager().getRegion("Region 1");

    /* Set up two cut planes:
     * - dc60 plane
     * - near inlet plane // To be able to calc pressure loss
     */
    double input_origin_dc60[] = new double[]{0.0, 0.44, 1.0};
    double input_normal_dc60[] = new double[]{0.0, 0.0, 1.0};

    double input_origin_nearInlet[] = new double[]{0.0, 0.44, 0.1};
    double input_normal_nearInlet[] = new double[]{0.0,0.0,1.0};

    // End of required user input ========================================================

    createPlaneSection(SIM, planeName, input_normal_dc60, input_origin_dc60);
    createPlaneSection(SIM, inletPlaneName, input_normal_nearInlet, input_origin_nearInlet);

    //
    IntVector dimTime = new IntVector(new int[] {0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});
    IntVector dimV = new IntVector(new int[] {0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});
    IntVector dimL = new IntVector(new int[] {0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});
    IntVector dimA = new IntVector(new int[] {0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});
    IntVector dimLess = new IntVector(new int[] {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});
    IntVector dimP = new IntVector(new int[] {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0});
    int vectorType = FieldFunctionTypeOption.VECTOR;
    int scalarType = FieldFunctionTypeOption.SCALAR;

    createFieldFunction("unity","1",dimLess,scalarType);

    // Derived information ===============================================================
    int ncuts = 0;
    ncuts = (int)360.0/(int)deltaangle;

    double [] PtotSector = new double[ncuts];

    // Centre cut vector
    double p1 = 0.0;
    double p2 = 1.0;
    double p3 = 0.0;

    double radius = 0.0;

    double v1 = 0.0;
    double v2 = 0.0;
    double v3 = 0.0;

    double h1 = 0.0;
    double h2 = 0.0;
    double h3 = 0.0;

    double Ptot = 0.0;
    double PtotSectormin = 0.0;

    double dc60 = 0.0;
    double qdc60 = 0.0;

    double theta = 0.0;

    // +/- 30 degree defining the 60 degree sector
    double angle = 30.0;

    double c = 0.0;
    double s = 0.0;

    double norm = 0.0;

    // End of derived information ========================================================

    // Get plane to evaluate dc60 over
    PlaneSection dc60_plane = ((PlaneSection) SIM.getPartManager().getObject(planeName));
    PlaneSection inlet_plane = ((PlaneSection) SIM.getPartManager().getObject(inletPlaneName));

    DoubleVector dc60_origin = dc60_plane.getOrigin();
    DoubleVector dc60_normal = dc60_plane.getOrientation();
    DoubleVector dc60_tangent = tangentVector(dc60_normal);
    DoubleVector dc60_cog = areaCOG(SIM,dc60_plane);

    info(SIM,"Origin from derived part  = "+dc60_origin);
    info(SIM,"Normal                    = "+dc60_normal);
    info(SIM,"Tangent vector            = "+tangentVector(dc60_normal));

    // Compute DC60 surface area
    double area = surfaceIntegral("dc60PlaneArea",SIM,dc60_plane ,"unity");
    radius = Math.sqrt(area/Math.PI);
    info(SIM,planeName+" Area =   "+area);
    info(SIM,planeName+" Radius = "+radius);

    double n1 = dc60_normal.getComponent(0);
    double n2 = dc60_normal.getComponent(1);
    double n3 = dc60_normal.getComponent(2);

    double c1 = dc60_cog.getComponent(0);
    double c2 = dc60_cog.getComponent(1);
    double c3 = dc60_cog.getComponent(2);

    double r1 = dc60_tangent.getComponent(0);
    double r2 = dc60_tangent.getComponent(1);
    double r3 = dc60_tangent.getComponent(2);

    info(SIM,"Centre coordinate : (" + c1 + "," + c2  + "," + c3 + ")");



    /* Uniformity index calculation */
    {
        createFieldFunction("normal_vector",dc60_normal.toString(),dimLess,vectorType);
        createFieldFunction("normal_velocity","dot($$normal_vector,$$Velocity)",dimV,scalarType);

        double averageNormalVelocity = planeAverage("avgNormalVel",SIM, dc60_plane, "normal_velocity");

        createFieldFunction("avgNormalVel",""+averageNormalVelocity,dimV,scalarType);

        createFieldFunction("magVelDeviation","abs($normal_velocity-$avgNormalVel)",dimV,scalarType);

        createFieldFunction("planeArea",""+area,dimA,scalarType);

        double UI = 1.0-1.0/(2*area*averageNormalVelocity)
                * surfaceIntegral("magVelDeviationIntegral",SIM,dc60_plane,"magVelDeviation");

        info(SIM,"Calculations of UI for plane "+planeName+":");
        info(SIM,"\tAverage normal velocity = "+averageNormalVelocity);
        info(SIM,"\tUI                      = "+UI);
    }
    /* END Uniformity index calculation*/

    // Define dynamic pressure field function
    createFieldFunction("DynamicPressure","$TotalPressure-$StaticPressure", dimP, scalarType);

    qdc60 = planeAverage("dc60 avgDynamicPressure",SIM, dc60_plane, "DynamicPressure");
    info(SIM,"Average dynamic pressure : " + qdc60);

    // Compute average total pressure
    Ptot = planeAverage("dc60 avgTotalPressure",SIM,dc60_plane,"TotalPressure");
    info(SIM,"Average total pressure : " + Ptot);

    // Compute mass flow averaged total pressure at dc60 plane and near inlet plane
    double mPtot_dc60 = planeMassflowAverage("dc60 mAvgTotalPressure",SIM,dc60_plane,"TotalPressure");
    double mPtot_inlet = planeMassflowAverage("inlet mAavgTotalPressure",SIM,inlet_plane,"TotalPressure");
    double pressureDrop = mPtot_inlet-mPtot_dc60;

    info(SIM,"Pressure drop between "+inletPlaneName+" and "+planeName+" = "+pressureDrop);

    // Retrieve units in model
    Units unitsL = SIM.getUnitsManager().getPreferredUnits(new IntVector(new int[] {0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}));


    // Loop over all sectors and compute average total pressure
    for ( int i = 0; i < ncuts; i++) {

        // Rotate plane vector
        theta = deltaangle*i*Math.PI/180;
        // info(SIM,"Centre perimeter vector angle : " + theta*180/Math.PI);
        c = Math.cos(theta);
        s = Math.sin(theta);
        p1 = (n1*n1+(1-n1*n1)*c) * r1 +  (n1*n2*(1-c)-n3*s) * r2  + (n1*n3*(1-c)+n2*s) * r3;
        p2 = (n1*n2*(1-c)+n3*s) * r1  +  (n2*n2+(1-n2*n2)*c) * r2 + (n2*n3*(1-c)-n1*s) * r3;
        p3 = (n1*n3*(1-c)-n2*s) * r1  +  (n2*n3*(1-c)+n1*s) * r2  + (n3*n3+(1-n3*n3)*c) * r3;
        // info(SIM,"Perimeter centre coordinate : (" + p1 + "," + p2  + "," + p3 + ")");

        // Compute -30 degree vector
        theta = -angle*Math.PI/180;
        c = Math.cos(theta);
        s = Math.sin(theta);
        v1 = (n1*n1+(1-n1*n1)*c) * p1 +  (n1*n2*(1-c)-n3*s) * p2  + (n1*n3*(1-c)+n2*s) * p3;
        v2 = (n1*n2*(1-c)+n3*s) * p1  +  (n2*n2+(1-n2*n2)*c) * p2 + (n2*n3*(1-c)-n1*s) * p3;
        v3 = (n1*n3*(1-c)-n2*s) * p1  +  (n2*n3*(1-c)+n1*s) * p2  + (n3*n3+(1-n3*n3)*c) * p3;

        // Compute +30 degree vector
        theta = angle*Math.PI/180;
        c = Math.cos(theta);
        s = Math.sin(theta);
        h1 = (n1*n1+(1-n1*n1)*c) * p1 +  (n1*n2*(1-c)-n3*s) * p2  + (n1*n3*(1-c)+n2*s) * p3;
        h2 = (n1*n2*(1-c)+n3*s) * p1  +  (n2*n2+(1-n2*n2)*c) * p2 + (n2*n3*(1-c)-n1*s) * p3;
        h3 = (n1*n3*(1-c)-n2*s) * p1  +  (n2*n3*(1-c)+n1*s) * p2  + (n3*n3+(1-n3*n3)*c) * p3;

        // Scale vectors to cover radius and extend 20% outside of that
        p1 = p1 * radius * rscale;
        p2 = p2 * radius * rscale;
        p3 = p3 * radius * rscale;

        v1 = v1 * radius * rscale;
        v2 = v2 * radius * rscale;
        v3 = v3 * radius * rscale;

        h1 = h1 * radius * rscale;
        h2 = h2 * radius * rscale;
        h3 = h3 * radius * rscale;

        // Define constrained plane cut
        DoubleVector constraintPoints = new DoubleVector(new double[] {c1, c2, c3, c1+v1, c2+v2, c3+v3, c1+p1, c2+p2, c3+p3, c1+h1, c2+h2, c3+h3} );
        ConstrainedPlaneSection constrainedPlaneSection_cut = createConstrainedPlane("pieceOfCake",SIM,region_0,constraintPoints,dc60_cog,dc60_normal,unitsL);
        constrainedPlaneSection_cut.setReevaluateStatus(true);

        PtotSector[i] = planeAverage("sectionAveragePtot",SIM,constrainedPlaneSection_cut,"TotalPressure");

        //SIM.getPartManager().removeObjects(constrainedPlaneSection_cut);

        //double plane_area = surfaceIntegral("Plane Area", SIM, constrainedPlaneSection_cut,"unity");
        //info(SIM,"Iteration : " + i + " cut area = " + plane_area);
        //info(SIM,"PtotSector              = " + PtotSector[i] + "\n");
    }

    double maxDeltaPSector =  Math.abs(Ptot - PtotSector[0]);
    int worstSectorIndex = 0;
    for (int i=1; i<PtotSector.length; i++) {
        double deltaPSector = Math.abs(Ptot - PtotSector[i]);
        if ( deltaPSector > maxDeltaPSector ) {
            maxDeltaPSector = deltaPSector;
            worstSectorIndex = i;
        }
    }

    /*
     * Calculate dc60
     * */
    double DC60 = (Ptot-PtotSector[worstSectorIndex]) / qdc60;
    info(SIM,"==DC60=======================");
    info(SIM,"\tAvg Ptot             = "+Ptot);
    info(SIM,"\tMin section avg Ptot = "+PtotSectormin);
    info(SIM,"\tAvg Pdyn             = "+qdc60);
    info(SIM,"\tDC60                 = " + DC60);
    info(SIM,"Done!");

    /*
    try {
        DataOutputStream outStream = new DataOutputStream( new FileOutputStream("dc60.dat") );
        for (int i=0; i<PtotSector.length; i++) {
            angle = deltaangle*i;
            dc60 = ( Ptot - PtotSector[i] )/ qdc60;
            outStream.writeBytes(" " + angle + "  " + PtotSector[i] + "  " + dc60 + "\n");
        }
        outStream.close();
    } catch( Exception ex ) { }
    */

  }
}
