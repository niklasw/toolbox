// STAR-CCM+ macro: importCutplane.java
package Truck_Exhaust;

import java.util.*;

import star.common.*;
import star.base.neo.*;
import star.vis.*;
import star.base.report.*;
import star.flow.*;

public class createMonitors extends StarMacro {

  public void execute() {
    execute0();
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


  private ArbitrarySection importArbitrary(Simulation SIM, String regionName, String fileName, String sectionName, Units units) {
    Region region= SIM.getRegionManager().getRegion(regionName);
    SIM.println("WKN--> reading stl file for arbitrary section: "+ fileName);
    if ( SIM.getPartManager().has(sectionName) )
    {
        ArbitrarySection oldSection = ((ArbitrarySection) SIM.getPartManager().getObject(sectionName));
        SIM.getPartManager().removeObjects(oldSection);
    }
    ArbitrarySection arbitrary = (ArbitrarySection) SIM.getPartManager().createArbitraryImplicitPart(new NeoObjectVector(new Object[] {region}), resolvePath(fileName), units);
    arbitrary.setPresentationName(sectionName);
    return arbitrary;
  }

  public double surfaceIntegral(String name, Simulation sim, ArbitrarySection sourcePlane, String scalarName)
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

  public DoubleVector planeVectorAverage(String name, Simulation sim, ArbitrarySection sourcePlane, String vectorName)
  {
    FieldFunction field= ((FieldFunction) sim.getFieldFunctionManager().getFunction(vectorName));
    IntVector dimLess = new IntVector(new int[] {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});
    FieldFunction X = createFieldFunction("vX","$$"+vectorName+"[0]",dimLess,FieldFunctionTypeOption.SCALAR);
    FieldFunction Y = createFieldFunction("vY","$$"+vectorName+"[1]",dimLess,FieldFunctionTypeOption.SCALAR);
    FieldFunction Z = createFieldFunction("vZ","$$"+vectorName+"[2]",dimLess,FieldFunctionTypeOption.SCALAR);
    double avgX = planeAverage("tmp",sim,sourcePlane,"vX");
    double avgY = planeAverage("tmp",sim,sourcePlane,"vY");
    double avgZ = planeAverage("tmp",sim,sourcePlane,"vZ");
    //sim.getReportManager().removeObjects(sim.getReportManager().getReport("tmp"));
    DoubleVector V = new DoubleVector(new double[] {avgX,avgY,avgZ});
    return V;
  }


  public double planeAverage(String name, Simulation sim, ArbitrarySection sourcePlane, String scalarName)
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

  public double planeMassflowAverage(String name, Simulation sim, ArbitrarySection sourcePlane, String scalarName)
  {
    FieldFunction field= ((FieldFunction) sim.getFieldFunctionManager().getFunction(scalarName));
    double average = 0.0;
    if ( ! sim.getReportManager().has(name) )
    {
        MassFlowAverageReport report = sim.getReportManager().createReport(MassFlowAverageReport.class);
        report.setPresentationName(name);
    }
    MassFlowAverageReport report = ((MassFlowAverageReport) sim.getReportManager().getObject(name));
    report.setScalar(field);
    report.getParts().setObjects(sourcePlane);
    ReportMonitor reportMonitor = report.createMonitor();
    reportMonitor.setPresentationName(name);
    try {
        report.printReport();
        average = report.getValue();
    } catch(NeoException e) {}
    return average;
  }


  public double boundaryMassFlowAverage(String regionName, List<String> boundaryNames, String reportName, String scalarName)
  {
    Simulation SIM = getActiveSimulation();
    FieldFunction field= ((FieldFunction) SIM.getFieldFunctionManager().getFunction(scalarName));
    if ( ! SIM.getReportManager().has(reportName) ) {
       MassFlowAverageReport report = SIM.getReportManager().createReport(MassFlowAverageReport.class);
       report.setPresentationName(reportName);
    }
    MassFlowAverageReport report = ((MassFlowAverageReport) SIM.getReportManager().getObject(reportName));

    Region region = SIM.getRegionManager().getRegion(regionName);
    LinkedList<Boundary> boundaries = new LinkedList();
    Iterator<String> namesIter = boundaryNames.iterator();
    while ( namesIter.hasNext() ) {
        String boundaryName = namesIter.next();
        Boundary boundary = region.getBoundaryManager().getBoundary(boundaryName);
        boundaries.add(boundary);
    }
    report.getParts().setObjects(boundaries);
    report.setScalar(field);
    ReportMonitor reportMonitor = report.createMonitor();
    reportMonitor.setPresentationName(reportName);
    double average = 0.0;
    try {
        report.printReport();
        average = report.getValue();
    } catch(NeoException e) {}
    return average;
  }



  private void execute0() {
    String prefix = "/home/fluidsim/Internal_Flow/261571_Eu6_Exhaust_outlet_pipes/PRE/Geometry";

    Hashtable<String,String> silencerMap = new Hashtable<String,String>();

    silencerMap.put("A1","/Silencers/Medium/127mm/Eu6_Medium_127mm_2071281-1_1.stosToPipe.stl");
    silencerMap.put("B1","/Silencers/Large/127mm/Eu6_Large_127mm_2071282-1_1_cleaned_removedFlanges_translated3mm.stosToPipe.stl");
    silencerMap.put("C1","/Silencers/Medium/114mm/Eu6inc_Medium_114mm_50208935-1_1.stosToPipe.stl");
    silencerMap.put("A2","/Silencers/Medium/127mm/Eu6_Medium_127mm_2071281-1_1.stosToPipe.stl");
    silencerMap.put("B2","/Silencers/Large/127mm/Eu6_Large_127mm_2071282-1_1_cleaned_removedFlanges_translated3mm.stosToPipe.stl");
    silencerMap.put("C2","/Silencers/Medium/114mm/Eu6inc_Medium_114mm_50208935-1_1.stosToPipe.stl");
    silencerMap.put("A3","/Silencers/Medium/127mm/Eu6_Medium_127mm_2071281-1_1.stosToPipe.stl");
    silencerMap.put("B3","/Silencers/Large/127mm/Eu6_Large_127mm_2071282-1_1_cleaned_removedFlanges_translated3mm.stosToPipe.stl");
    silencerMap.put("C3","/Silencers/Medium/114mm/Eu6inc_Medium_114mm_50208935-1_1.stosToPipe.stl");
    silencerMap.put("C3_ref","/Silencers/Medium/114mm/Eu6inc_Medium_114mm_50208935-1_1.stosToPipe.stl");

    Hashtable<String,String> pipeMap = new Hashtable<String,String>();
    pipeMap.put("A1","/Pipes/127mm/Eu6_127mm_1_2071255-1_1_outlet.stl");
    pipeMap.put("A2","/Pipes/127mm/Eu6_127mm_2_2071256-1_1_outlet.stl");
    pipeMap.put("A3","/Pipes/127mm/Eu6_127mm_3_2071257-1_1_outlet.stl");
    pipeMap.put("B1","/Pipes/127mm/Eu6_127mm_1_2071255-1_1_outlet.stl");
    pipeMap.put("B2","/Pipes/127mm/Eu6_127mm_2_2071256-1_1_outlet.stl");
    pipeMap.put("B3","/Pipes/127mm/Eu6_127mm_3_2071257-1_1_outlet.stl");
    pipeMap.put("C1","/Pipes/114mm/Eu6inc_114mm_4_2072114-1_1_outlet.igs.stl");
    pipeMap.put("C2","/Pipes/114mm/Eu6inc_114mm_5_2071367-1_1_outlet.stl"    );
    pipeMap.put("C3","/Pipes/114mm/Eu6inc_114mm_6_2071370-1_1_outlet.stl"    );
    pipeMap.put("C3_ref","/Pipes/114mm/Eu6inc_114mm_6_2071370-1_1_outlet.stl"    );

    Simulation SIM = getActiveSimulation();

    String CWD = System.getProperty("user.dir");
    String simDirName = CWD.substring(CWD.lastIndexOf("/")+1);
    SIM.println("WKN --> "+CWD+" "+simDirName);

    String silencerFile  = silencerMap.get(simDirName);
    String silencerName  = silencerFile.substring(silencerFile.lastIndexOf("/")+1,silencerFile.lastIndexOf("."));

    String pipeFile = pipeMap.get(simDirName);
    String pipeName = pipeFile.substring(pipeFile.lastIndexOf("/")+1,pipeFile.lastIndexOf("."));


    Units units_0 = SIM.getUnitsManager().getPreferredUnits(new IntVector(new int[] {0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}));
    Units units_1 = ((Units) SIM.getUnitsManager().getObject("mm"));

    ArbitrarySection silencerOutSection = importArbitrary(SIM,"Region 1",prefix+silencerFile,"silencerOutlet",units_1);
    ArbitrarySection pipeOutSection = importArbitrary(SIM,"Region 1",prefix+pipeFile,"pipeOutlet",units_1);

    IntVector dimP = new IntVector(new int[] {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0});
    createFieldFunction("DynamicPressure", "$TotalPressure-$Pressure", dimP, FieldFunctionTypeOption.SCALAR);

    double muzzlePtotMFA = planeMassflowAverage("Pipe outlet total pressure mass flow avg",SIM,pipeOutSection,"TotalPressure");
    double muzzlePdynMFA = planeMassflowAverage("Pipe outlet dynamic pressure mass flow avg",SIM,pipeOutSection,"DynamicPressure");
    double silencerToPipeInterfacePtotMFA = planeMassflowAverage("Silencer outlet mass flow avg",SIM,silencerOutSection,"TotalPressure");

    List<String> inletBoundary = Arrays.asList( "Silencer.inletsfromscr" );

    double inletMassFlowAvg = boundaryMassFlowAverage("Region 1", inletBoundary, "Silencer inlet mass flow avg", "TotalPressure");

    SIM.println("Silencer inlet total Pressure Mass flow average = "+inletMassFlowAvg);
    SIM.println("Silencer outlet  total Pressure Mass flow average = "+silencerToPipeInterfacePtotMFA);
    SIM.println("Pipe outlet total Pressure Mass flow average = "+muzzlePtotMFA);
    SIM.println("Pipe outlet dynamic Pressure Mass flow average = "+muzzlePdynMFA);

    double pipePressureIntegral = surfaceIntegral("Static pressure integral", SIM, pipeOutSection, "Pressure");
    double pipeDynamicPressureIntegral = surfaceIntegral("Dynamic pressure integral", SIM, pipeOutSection, "DynamicPressure");
    SIM.println("Pipe outlet integrated static pressure  = "+pipePressureIntegral);
    SIM.println("Pipe outlet integrated dynamic pressure = "+pipeDynamicPressureIntegral);
  }
}
