// STAR-CCM+ macro: t.java
package myFunctions;

import java.io.*;
import java.util.*;
import star.base.neo.*;
import star.base.report.*;
import star.common.*;
import star.flow.*;
import star.vis.*;

public class myPost extends myCase {

	public myPost(Simulation s) {
		super(s);
	}

	/* General */
	public void clearScenes() {
		SceneManager smgr = sim.getSceneManager();
		for (Scene s : smgr.getScenes()) {
			smgr.deleteScene(s);
		}
	}

	public void clearDerivedParts() {
		Collection<Part> Parts = sim.getPartManager().getObjects();
		for (Part p : Parts) {
			sim.getPartManager().remove(p);
		}
	}

	public Scene createNewScene(String sceneName_script) {

		if (sim.getSceneManager().has(sceneName_script)) {
			Scene deleteScene = sim.getSceneManager().getScene(sceneName_script);
			sim.getSceneManager().deleteScenes(new NeoObjectVector(new Object[]{deleteScene}));
		}

		sim.getSceneManager().createScalarScene(sceneName_script, "Outline", "Scalar");
		Scene scene_1 = sim.getSceneManager().getScene(sceneName_script + " 1");
		scene_1.setPresentationName(sceneName_script);
		return scene_1;
	}

	public void setVolumeRepresentation(Scene s) {
		FvRepresentation rep = ((FvRepresentation) sim.getRepresentationManager().getObject("Volume Mesh"));
		Collection<Displayer> displayers = s.getDisplayerManager().getObjects();
		for (Displayer d : displayers) {
			d.setRepresentation(rep);
		}
	}

	public void removeLogo(Scene scene) {
		if (scene.getAnnotationPropManager().has("Logo")) {
			AnnotationProp annot = ((AnnotationProp) scene.getAnnotationPropManager().getAnnotationProp("Logo"));
			scene.getAnnotationPropManager().remove(annot);
		}
	}

	public void showRegion(String regionName, Scene scene, boolean show) {
		try {
			Region region = sim.getRegionManager().getRegion(regionName);
			Collection boundaries = region.getBoundaryManager().getBoundaries();
			ScalarDisplayer displayer = ((ScalarDisplayer) scene.getDisplayerManager().getDisplayer("Scalar 1"));

			if (show) {
				displayer.getParts().addParts(boundaries);
			} else {
				displayer.getHiddenParts().addObjects(boundaries);
			}
		} catch (NeoException e) {
			System.out.println("Warning in macro: Could not display region " + regionName);
		}
	}

	public void showGeomBoundaries(String regionName, Scene scene, String pattern){
			try {
			Region region = sim.getRegionManager().getRegion(regionName);
			Collection<Boundary> allBoundaries = region.getBoundaryManager().getBoundaries();
			PartDisplayer displayer = ((PartDisplayer) scene.getDisplayerManager().createPartDisplayer("Geometry"));
			displayer.initialize();
			
			displayer.getHiddenParts().addObjects(allBoundaries);
			displayer.setSurface(true);

			/* Count boundaries matching pattern */
			int count=0;
			for (Boundary b: allBoundaries ) {
				if ( b.getPresentationName().matches(pattern)) {
					count++;
				}
			}

			Info("Added number of boundaries = "+count);

			ArrayList<Boundary> boundariesL = new ArrayList<Boundary>(count);

			for (Boundary b: allBoundaries ) {
				if ( b.getPresentationName().matches(pattern)) {
					Info(b.getPresentationName());
					boundariesL.add(b);
					Info(b.getPresentationName());
				}
			}

			Info("Added number of boundaries = "+boundariesL.size());
			
			displayer.getParts().addParts(boundariesL);

		} catch (NeoException e) {
			System.out.println("Warning in macro: Could not display region " + regionName);
		}
	
	}

	public void showBoundaries(String regionName, Scene scene, String pattern){
			try {
			Region region = sim.getRegionManager().getRegion(regionName);
			Collection<Boundary> allBoundaries = region.getBoundaryManager().getBoundaries();
			ScalarDisplayer displayer = ((ScalarDisplayer) scene.getDisplayerManager().getDisplayer("Scalar 1"));
			
			displayer.getHiddenParts().addObjects(allBoundaries);

			/* Count boundaries matching pattern */
			int count=0;
			for (Boundary b: allBoundaries ) {
				if ( b.getPresentationName().matches(pattern)) {
					count++;
				}
			}

			Info("Added number of boundaries = "+count);

			ArrayList<Boundary> boundariesL = new ArrayList<Boundary>(count);

			for (Boundary b: allBoundaries ) {
				if ( b.getPresentationName().matches(pattern)) {
					Info(b.getPresentationName());
					boundariesL.add(b);
					Info(b.getPresentationName());
				}
			}

			Info("Added number of boundaries = "+boundariesL.size());
			
			displayer.getParts().addParts(boundariesL);

		} catch (NeoException e) {
			System.out.println("Warning in macro: Could not display region " + regionName);
		}
	
	}
	public void showAllRegions(Scene scene, boolean show) {
		Collection regions = sim.getRegionManager().getRegions();
		Iterator<Region> regIter = regions.iterator();

		while (regIter.hasNext()) {
			Region R = regIter.next();
			showRegion(R.getPresentationName(), scene, show);
		}
	}

	public void setScalarField(ScalarDisplayer displayer, String fieldName, double min, double max, String unit) {
		PrimitiveFieldFunction ff = ((PrimitiveFieldFunction) sim.getFieldFunctionManager().getFunction(fieldName));
		try {
			VectorMagnitudeFieldFunction vmff = (VectorMagnitudeFieldFunction) ff.getMagnitudeFunction();
			displayer.getScalarDisplayQuantity().setFieldFunction(vmff);
		} catch (NeoException e) {
			displayer.getScalarDisplayQuantity().setFieldFunction(ff);
		}
		displayer.getScalarDisplayQuantity().setUnits((Units) sim.getUnitsManager().getObject(unit));
		displayer.getScalarDisplayQuantity().setRange(new DoubleVector(new double[]{min, max}));
		displayer.getScalarDisplayQuantity().setClip(0);
	}

	public void setScalarField(StreamDisplayer displayer, String fieldName, double min, double max, String unit) {
		FieldFunction ff = sim.getFieldFunctionManager().getFunction(fieldName);
		displayer.getScalarDisplayQuantity().setFieldFunction(ff);
		displayer.getScalarDisplayQuantity().setUnits(sim.getUnitsManager().getObject(unit));
		displayer.getScalarDisplayQuantity().setRange(new DoubleVector(new double[]{min, max}));
		displayer.getScalarDisplayQuantity().setClip(0);
	}

	public UserFieldFunction createFieldFunction(String name, String definition, IntVector dimensions, int type) {
		if (sim.getFieldFunctionManager().has(name)) {
			UserFieldFunction func = ((UserFieldFunction) sim.getFieldFunctionManager().getFunction(name));
			func.setDimensionsVector(dimensions);
			func.getTypeOption().setSelected(type);
			func.setDefinition(definition);
			return func;
		} else {
			UserFieldFunction func = ((UserFieldFunction) sim.getFieldFunctionManager().createFieldFunction());
			func.setDimensionsVector(dimensions);
			func.getTypeOption().setSelected(type);
			func.setFunctionName(name);
			func.setPresentationName(name);
			func.setDefinition(definition);
			return func;
		}
	}

	/* Sections */
	public PlaneSection createPlaneSection(Scene scene, String name, double[] normal, double[] origin) {
		DoubleVector Normal = new DoubleVector(normal);
		DoubleVector Origin = new DoubleVector(origin);
		if (sim.getPartManager().has(name)) {
			PlaneSection oldPlane = ((PlaneSection) sim.getPartManager().getObject(name));
			sim.getPartManager().removeObjects(oldPlane);
		}
		PlaneSection planeSection = (PlaneSection) sim.getPartManager().createImplicitPart(new NeoObjectVector(new Object[]{}), Normal, Origin, 0, 1, new DoubleVector(new double[]{0.0}));
		planeSection.setPresentationName(name);

		Collection regions = sim.getRegionManager().getRegions();

		planeSection.getInputParts().setObjects(regions);

		ScalarDisplayer scalarDisplayer = ((ScalarDisplayer) scene.getDisplayerManager().getDisplayer("Scalar 1"));
		PartDisplayer partDisplayer = ((PartDisplayer) scene.getDisplayerManager().getDisplayer("Outline 1"));

		scalarDisplayer.getParts().setObjects(planeSection);
		partDisplayer.getParts().setObjects(planeSection);
		return planeSection;
	}

	public PlaneSection createPlaneSection(Scene scene, String name, double[] normal, double[] origin, String regionPattern) {
		DoubleVector Normal = new DoubleVector(normal);
		DoubleVector Origin = new DoubleVector(origin);
		if (sim.getPartManager().has(name)) {
			PlaneSection oldPlane = ((PlaneSection) sim.getPartManager().getObject(name));
			sim.getPartManager().removeObjects(oldPlane);
		}
		PlaneSection planeSection = (PlaneSection) sim.getPartManager().createImplicitPart(new NeoObjectVector(new Object[]{}), Normal, Origin, 0, 1, new DoubleVector(new double[]{0.0}));
		planeSection.setPresentationName(name);

		Collection regions = getRegions(regionPattern);

		planeSection.getInputParts().setObjects(regions);

		ScalarDisplayer scalarDisplayer = ((ScalarDisplayer) scene.getDisplayerManager().getDisplayer("Scalar 1"));
		PartDisplayer partDisplayer = ((PartDisplayer) scene.getDisplayerManager().getDisplayer("Outline 1"));

		scalarDisplayer.getParts().setObjects(planeSection);
		partDisplayer.getParts().setObjects(planeSection);
		return planeSection;
	}

	/* Arbitrary Sections and averaging */
	public ArbitrarySection importArbitrary(String fileName, Units units) {
		String name = basenameNoExt(fileName);
		Collection<Region> allRegions = sim.getRegionManager().getRegions();
		sim.println("WKN--> reading stl file for arbitrary section: " + fileName);
		if (sim.getPartManager().has(name)) {
			ArbitrarySection oldSection = ((ArbitrarySection) sim.getPartManager().getObject(name));
			sim.getPartManager().removeObjects(oldSection);
		}
		ArbitrarySection arbitrary = (ArbitrarySection) sim.getPartManager().createArbitraryImplicitPart(new Vector(allRegions), fileName, units);
		arbitrary.setPresentationName(name);
		return arbitrary;
	}

	public double surfaceIntegral(String name, NamedObject sourcePlane, String scalarName) {
		FieldFunction field = ((FieldFunction) sim.getFieldFunctionManager().getFunction(scalarName));
		if (!sim.getReportManager().has(name)) {
			SurfaceIntegralReport report = sim.getReportManager().createReport(SurfaceIntegralReport.class);
			report.setPresentationName(name);
		}
		SurfaceIntegralReport report = ((SurfaceIntegralReport) sim.getReportManager().getObject(name));
		report.setScalar(field);
		report.getParts().setObjects(sourcePlane);
		return report.getValue();
	}

	public double surfaceAverage(String name, NamedObject sourcePlane, String scalarName) {
		FieldFunction field = ((FieldFunction) sim.getFieldFunctionManager().getFunction(scalarName));
		if (!sim.getReportManager().has(name)) {
			AreaAverageReport report = sim.getReportManager().createReport(AreaAverageReport.class);
			report.setPresentationName(name);
		}
		AreaAverageReport report = ((AreaAverageReport) sim.getReportManager().getObject(name));
		report.setScalar(field);
		report.getParts().setObjects(sourcePlane);
		return report.getValue();
	}

	public double surfaceAverage(String name, NamedObject sourcePlane, VectorComponentFieldFunction scalar) {
		double average;
		if (!sim.getReportManager().has(name)) {
			AreaAverageReport report = sim.getReportManager().createReport(AreaAverageReport.class);
			report.setPresentationName(name);
		}
		AreaAverageReport report = ((AreaAverageReport) sim.getReportManager().getObject(name));
		report.setScalar(scalar);
		report.getParts().setObjects(sourcePlane);
		average = report.getValue();
		return average;
	}

	public DoubleVector tangentVector(DoubleVector planeNormal) {
		myOps op = new myOps();
		DoubleVector random = op.normalize(new DoubleVector(new double[]{0, 1, 0}));
		while (op.dotProduct(random, planeNormal) > 0.5) {
			random = op.normalize(new DoubleVector(new double[]{Math.random(), Math.random(), Math.random()}));
			System.out.println("Random vector" + random);
		}
		DoubleVector t = op.crossProduct(planeNormal, random);
		t = op.normalize(t);
		return t;
	}

	public <T extends NamedObject> DoubleVector areaCOG(T plane) {
		PrimitiveFieldFunction pos = (PrimitiveFieldFunction) sim.getFieldFunctionManager().getFunction("Position");
		VectorComponentFieldFunction p0 = (VectorComponentFieldFunction) pos.getComponentFunction(0);
		VectorComponentFieldFunction p1 = (VectorComponentFieldFunction) pos.getComponentFunction(1);
		VectorComponentFieldFunction p2 = (VectorComponentFieldFunction) pos.getComponentFunction(2);
		double c0 = surfaceAverage("tmp", plane, p0);
		double c1 = surfaceAverage("tmp", plane, p1);
		double c2 = surfaceAverage("tmp", plane, p2);
		DoubleVector C = new DoubleVector(new double[]{c0, c1, c2});
		Info("areaCOG = " + C);
		return C;
	}

	public <T extends NamedObject> DoubleVector surfaceNormalAverage(T plane) {
		PrimitiveFieldFunction pos = (PrimitiveFieldFunction) sim.getFieldFunctionManager().getFunction("Area");
		VectorComponentFieldFunction p0 = (VectorComponentFieldFunction) pos.getComponentFunction(0);
		VectorComponentFieldFunction p1 = (VectorComponentFieldFunction) pos.getComponentFunction(1);
		VectorComponentFieldFunction p2 = (VectorComponentFieldFunction) pos.getComponentFunction(2);
		double c0 = surfaceAverage("tmp", plane, p0);
		double c1 = surfaceAverage("tmp", plane, p1);
		double c2 = surfaceAverage("tmp", plane, p2);
		DoubleVector C = new DoubleVector(new double[]{c0, c1, c2});
		myOps op = new myOps();
		C = op.normalize(C);
		Info("surfaceNormalAverage = " + C);
		return C;
	}

	public <T extends NamedObject> double surfaceMassFlux(String name, T sourcePlane) {
		double mf = 0.0;
		if (!sim.getReportManager().has(name)) {
			MassFlowReport report = sim.getReportManager().createReport(MassFlowReport.class);
			report.setPresentationName(name);
		}
		MassFlowReport report = ((MassFlowReport) sim.getReportManager().getObject(name));
		report.getParts().setObjects(sourcePlane);

		ReportMonitor reportMonitor = null;

		if (sim.getMonitorManager().has(name)) {
			try {
				sim.getMonitorManager().removeObjects(sim.getMonitorManager().getObject(name));
				reportMonitor = report.createMonitor();
			} catch (NeoException e) {
				sim.println("WKN --> Could not remove monitor. Probably used. Reusing old.");
				reportMonitor = (ReportMonitor) sim.getMonitorManager().getMonitor(name);
			}
		} else {
			reportMonitor = report.createMonitor();
		}
		reportMonitor.setUpdateFrequency(10);
		reportMonitor.setPresentationName(name);
		try {
			//report.printReport();
			mf = report.getValue();
		} catch (NeoException e) {
		}
		return mf;
	}

	public <T extends NamedObject> double surfaceMassFlowAverage(String name, T sourcePlane, String scalarName) {
		FieldFunction field = ((FieldFunction) sim.getFieldFunctionManager().getFunction(scalarName));
		double average = 0.0;
		if (!sim.getReportManager().has(name)) {
			MassFlowAverageReport report = sim.getReportManager().createReport(MassFlowAverageReport.class);
			report.setPresentationName(name);
		}
		MassFlowAverageReport report = ((MassFlowAverageReport) sim.getReportManager().getObject(name));
		report.setScalar(field);
		report.getParts().setObjects(sourcePlane);

		ReportMonitor reportMonitor;

		if (sim.getMonitorManager().has(name)) {
			try {
				sim.getMonitorManager().removeObjects(sim.getMonitorManager().getObject(name));
				reportMonitor = report.createMonitor();
			} catch (NeoException e) {
				sim.println("WKN --> Could not remove monitor. Probably used. Reusing old.");
				reportMonitor = (ReportMonitor) sim.getMonitorManager().getMonitor(name);
			}
		} else {
			reportMonitor = report.createMonitor();
		}
		reportMonitor.setUpdateFrequency(10);
		reportMonitor.setPresentationName(name);
		try {
			//report.printReport();
			average = report.getValue();
		} catch (NeoException e) {
		}
		return average;
	}

	public <T extends NamedObject> double surfaceMassFlowAverage(String reportName, List<T> surfaces, String scalarName) {
		FieldFunction field = ((FieldFunction) sim.getFieldFunctionManager().getFunction(scalarName));
		if (!sim.getReportManager().has(reportName)) {
			MassFlowAverageReport report = sim.getReportManager().createReport(MassFlowAverageReport.class);
			report.setPresentationName(reportName);
		}
		MassFlowAverageReport report = ((MassFlowAverageReport) sim.getReportManager().getObject(reportName));

		report.getParts().setObjects(surfaces);
		report.setScalar(field);

		ReportMonitor reportMonitor = null;

		if (sim.getMonitorManager().has(reportName)) {
			try {
				sim.getMonitorManager().removeObjects(sim.getMonitorManager().getObject(reportName));
				reportMonitor = report.createMonitor();
			} catch (NeoException e) {
				sim.println("WKN --> Could not remove monitor. Probably used. Reusing old.");
				reportMonitor = (ReportMonitor) sim.getMonitorManager().getMonitor(reportName);
			}
		} else {
			reportMonitor = report.createMonitor();
		}

		reportMonitor.setUpdateFrequency(5);
		reportMonitor.setPresentationName(reportName);
		double average = 0.0;
		try {
			//report.printReport();
			average = report.getValue();
		} catch (NeoException e) {
		}
		return average;
	}

	public void runAllReports() {

		Collection<Report> reports = sim.getReportManager().getObjects();
		for (Report r : reports) {
			r.printReport();
		}
	}

	public void runAllReports(String fileName) {
		try {
			BufferedWriter out = new BufferedWriter(new FileWriter(fileName));

			Collection<Report> reports = sim.getReportManager().getObjects();
			for (Report r : reports) {
				if (r instanceof ScalarReport) {
					ScalarReport sr = ((ScalarReport) r);
					r.printReport();
					out.write(r.getPresentationName() + " = " + sr.getValue() + "\n");
				} else {
					Info(r.getPresentationName() + "is not a Scalar Report");
				}
			}
			out.close();
		} catch (IOException e) {
		}
	}

	public void showOutline(String regionName, Scene scene, boolean show) {
		Region region = sim.getRegionManager().getRegion(regionName);
		Collection boundaries = region.getBoundaryManager().getBoundaries();
		if (scene.getDisplayerManager().has("Outline 1")) {
			PartDisplayer displayer = ((PartDisplayer) scene.getDisplayerManager().getDisplayer("Outline 1"));

			if (show) {
				displayer.getParts().addParts(boundaries);
			} else {
				displayer.getHiddenParts().addObjects(boundaries);
			}
		}
	}

	public IsoPart createIsoSurface(String isoName, double[] values, String unit) {
		NullFieldFunction nullField = (NullFieldFunction) sim.getFieldFunctionManager().getFunction("NullFieldFunction");
		IsoPart isoPart = sim.getPartManager().createIsoPart(new NeoObjectVector(new Object[] {}), nullField);
		isoPart.setMode(0);
		isoPart.setPresentationName("iso"+isoName);
		isoPart.setMode(1);
		
		PrimitiveFieldFunction field = ((PrimitiveFieldFunction) sim.getFieldFunctionManager().getFunction(isoName));
		isoPart.setFieldFunction(field);
		MultiIsoValue multiIsoValue_2 = isoPart.getMultiIsoValue();
		Units units_1 = ((Units) sim.getUnitsManager().getObject(unit));
		multiIsoValue_2.getValueQuantities().setUnits(units_1);
		multiIsoValue_2.getValueQuantities().setArray(new DoubleVector(values));
		myCase myC = new myCase(sim);
		List<Region> regions = myC.getRegions(".*");
		isoPart.getInputParts().setObjects(regions);
		return isoPart;
	}

	public void showAllOutline(Scene scene, boolean show) {
		Collection<Region> regions = sim.getRegionManager().getRegions();
		for (Region R : regions) {
			showOutline(R.getPresentationName(), scene, show);
		}
	}

	public void verticalLegend(Legend l) {
		l.setOrientation(1);
		l.setWidth(0.1);
		l.setHeight(0.6);
		l.setOrientation(1);
		l.setPositionCoordinate(new DoubleVector(new double[]{0.03, 0.3}));
		l.setWidth(0.11);
		l.setHeight(0.6);
	}

	public void verticalLegend(StreamDisplayer displayer) {
		verticalLegend(displayer.getLegend());
	}

	public void verticalLegend(ScalarDisplayer displayer) {
		verticalLegend(displayer.getLegend());
	}
}
