/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package NCG_FAI.PostProcess;
import General.*;
import star.common.*;
import star.vis.*;
import star.base.neo.*;
import star.flow.*;
import java.io.*;
import star.base.report.*;
import java.util.*;

import myFunctions.*;

/**
 *
 * @author konwkn
 */
public class px04totalPressure extends StarMacro {

	public void execute() {
    		execute0();
  	}

	private void execute0() {

   		Simulation simulation = getActiveSimulation();

   		myCase myC = new myCase(simulation);
		myPost myP = new myPost(simulation);
		myOps   op  = new myOps();

   		myC.Info("pwd() =           ",myC.pwd());
   		myC.Info("dirname() =       ",myC.dirname());
   		myC.Info("directoryname() = ",myC.directoryname());
   		myC.Info("basename() =      ",myC.basename());
   		myC.Info("title() =         ",myC.title());

		myP.Info("\nCalculating total pressure in PX04 plane\n Based on bulk velocity.");
		myP.Info("You have to give normal and origin of PX04 in macro!");
		Scene S = myP.createNewScene("PX04 for ptot");
		Double px04Offset = 0.25; //[m]

		//myP.showAllRegions(S, true);
		myP.showRegion("downstream", S, true);
		myP.removeLogo(S);
			
		/* Calculate rig like total pressure in px04 section
		 * 0.25 m downstream interface_compressor
		 */
		Region downstream = myC.getRegions("downstream").get(0);
		InterfaceBoundary iface = myC.getInterfaces(downstream,"interface_compressor").get(0);
		DoubleVector origin  = myP.areaCOG(iface);
		DoubleVector normal  = myP.surfaceNormalAverage(iface);
	 	origin = op.vectorAddition(origin, op.scalarMultiply(normal,px04Offset));

		PlaneSection P = myP.createPlaneSection(S, "Plane Section", normal.toDoubleArray(), origin.toDoubleArray(), "extrusion");

    		ScalarDisplayer displayer = ((ScalarDisplayer) S.getDisplayerManager().getDisplayer("Scalar 1"));
		myP.setScalarField(displayer , "Velocity", 0, 70, "m/s");

		CurrentView V = S.getCurrentView();

                V.setInput(
			new DoubleVector(origin),
			new DoubleVector(new double[] {-0.75, 0.5, 0.31}),
			new DoubleVector(new double[] {0,0,1}),
			0.07, 1);

		UserFieldFunction unity = myP.createFieldFunction("unity","1",myP.dimLess,FieldFunctionTypeOption.SCALAR);
		
		double averagePstat = myP.surfaceAverage("average pstat", P, "Pressure");
		double planeArea = myP.surfaceIntegral("Area integrate", P, "unity");


		double massFlow = myP.surfaceMassFlux("px04MassFlux",P);
		double avgRho = myP.surfaceAverage("px04 rho average", P, "Density");
		double volFlow = massFlow/avgRho;
		double U = volFlow/planeArea;
		double pDyn = avgRho/2.0*U*U;
		double pTot_bulk = pDyn+averagePstat;
		myP.Info("Mass flow through px04 = "+massFlow);
		myP.Info("Volume flow through px04 = "+volFlow);
		myP.Info("Bulk velocity in px04 = "+U);
		myP.Info("Average static pressure in px04 = "+averagePstat);
		myP.Info("Bulk dynamic pressure in px04 = "+pDyn);
		myP.Info("Bulk total pressure in px04 = "+pTot_bulk);

		double mavgPtot = myP.surfaceMassFlowAverage("px04 mfap", P, "TotalPressure");

		myP.Info("Mass flow averaged total pressure in px04 ="+mavgPtot);

		String volRepName = "Volume Integral pxrun";
		if (!simulation.getReportManager().has(volRepName)){
			VolumeIntegralReport volRep = simulation.getReportManager().createReport(VolumeIntegralReport.class);
			volRep.setPresentationName(volRepName);
		}
		VolumeIntegralReport volRep = (VolumeIntegralReport) simulation.getReportManager().getObject(volRepName);
		volRep.getParts().setObjects(myP.getRegions("downstream"));
		volRep.setScalar(unity);
		volRep.printReport();

		String reportsFileName = myP.fullPathNoExt()+"_wPx04.reports";
		myP.runAllReports(reportsFileName);

		try {
            		BufferedWriter out = new BufferedWriter(new FileWriter(reportsFileName,true));
			out.write("Bulk Ptot px04 = "+ pTot_bulk+"\n");
			myP.Info("Appended to "+reportsFileName);
			out.close();
		} catch(IOException e) {
			System.err.println("Error: " + e.getMessage());
		}
	}
	
}
