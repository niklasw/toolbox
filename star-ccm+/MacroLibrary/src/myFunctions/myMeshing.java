// STAR-CCM+ macro: t.java
package myFunctions;

import java.util.*;
import star.base.neo.*;
import star.common.*;
import star.extruder.*;
import star.meshing.*;
import star.prismmesher.*;

public class myMeshing extends myCase {

	//Simulation sim;
	public myMeshing(Simulation s) {
		super(s);
	}

	/* Mesh generation */
	/**
	 * Reads a set of STL files as parts from disk.
	 * @param prefix
	 * @param pattern
	 * @param units
	 */
	public void readParts(String prefix, String pattern, String units) {
		List<String> files = findFile(prefix, pattern);
		PartImportManager partImportManager = sim.get(PartImportManager.class);
		Units units_1 = ((Units) sim.getUnitsManager().getObject(units));

		for (String f : files) {
			String partName = f.substring(f.lastIndexOf("/") + 1, f.lastIndexOf("."));
			partImportManager.importStlPart(f, "OneSurfacePerPatch", units_1, true, 1.0E-5);
			LeafMeshPart part = (LeafMeshPart) sim.get(SimulationPartManager.class).getPart(partName);
			String presentationName = f.substring(f.lastIndexOf("/") + 1, f.indexOf("."));
			part.setPresentationName(presentationName);
		}
	}

	public void createFeaturelinesOnRegion(String regionName, double sharpAngle) {
		SurfaceRep surfaceRep = ((SurfaceRep) sim.getRepresentationManager().getObject("Initial Surface"));

		Region region = sim.getRegionManager().getRegion(regionName);
		Collection boundaries = region.getBoundaryManager().getBoundaries();
		surfaceRep.createFeatureEdgesOnBoundaries(
			new NeoObjectVector(boundaries.toArray()), true, true, true, true, true, true, sharpAngle, true
			);
	}

	public void createFeaturelinesOnRegions(double sharpAngle) {
		SurfaceRep surfaceRep = ((SurfaceRep) sim.getRepresentationManager().getObject("Initial Surface"));

		Collection<Region> regions = sim.getRegionManager().getRegions();
		for (Region r : regions) {
			createFeaturelinesOnRegion(r.getPresentationName(), sharpAngle);
		}
	}

	public void clearFeaturesOnRegion(String regionName) {
		Region region = sim.getRegionManager().getRegion(regionName);
		Collection<FeatureCurve> features = region.getFeatureCurveManager().getObjects();
		region.getFeatureCurveManager().removeObjects(features);
	}

	public void clearFeaturesOnRegions() {
		Collection<Region> regions = sim.getRegionManager().getRegions();
		for (Region r : regions) {
			clearFeaturesOnRegion(r.getPresentationName());
		}
	}

	public void createFeaturelinesOnParts(double angle) {
		Collection<GeometryPart> parts = sim.get(SimulationPartManager.class).getObjects();
		sim.println(parts.size());

		for (GeometryPart part : parts) {
			sim.println(part.getPresentationName());
			LeafMeshPart leafMeshPart_0 = (
				(LeafMeshPart) sim.get(SimulationPartManager.class).getPart(part.getPresentationName())
				);
			Collection partObjects = leafMeshPart_0.getPartSurfaceManager().getObjects();
			PartCurve partCurve_0 = leafMeshPart_0.createPartCurvesOnPartSurfaces(
				new NeoObjectVector(partObjects.toArray()), true, false, false, true, false, false, true, angle, true
				);
			partCurve_0.setPresentationName(part.getPresentationName() + "_Curves");
		}
	}

	public void clearWrapFeatures() {

		String rmFeatureName = "Edges from Wrapping";

		Collection<Region> regions = sim.getRegionManager().getObjects();

		for (Region reg : regions) {
			Collection<FeatureCurve> features = reg.getFeatureCurveManager().getObjects();
			for (FeatureCurve crv : features) {
				if (crv.getPresentationName().contains(rmFeatureName)) {
					reg.getFeatureCurveManager().removeObjects(crv);
				}
			}

		}
	}

	public void removeBoundaries(String bString) {
		for (Region r : sim.getRegionManager().getRegions()) {
			Collection<Boundary> bnds = getBoundaries(r, bString);
			r.getBoundaryManager().removeBoundaries(new NeoObjectVector(bnds.toArray()));
		}
	}

	public void cleanWrap() {
		removeBoundaries("Gap Closure");
		clearWrapFeatures();
	}

	public void disablePrism(String regionName, String bString) {

		Region region = sim.getRegionManager().getRegion(regionName);

		for (Boundary b : getBoundaries(region, bString)) {
			try {
				b.get(MeshConditionManager.class).get(CustomizeBoundaryPrismsOption.class).setSelected(CustomizeBoundaryPrismsOption.DISABLE);
				sim.println("WKN--> Did disable prism for " + b.getPresentationName());
			} catch (NeoException e) {
				//sim.println("WKN--> Could not disable prism for " + b.getPresentationName());
			}
		}
	}

	public void defaultPrism(String regionName, String bString) {
		Region r = sim.getRegionManager().getRegion(regionName);
		for (Boundary b : getBoundaries(r, bString)) {
			try {
				b.get(MeshConditionManager.class).get(CustomizeBoundaryPrismsOption.class).setSelected(CustomizeBoundaryPrismsOption.DEFAULT);
				sim.println("WKN--> Default prism set for " + b.getPresentationName());
			} catch (NeoException e) {
				//sim.println("WKN--> Could not reset prism for " + b.getPresentationName());
			}
		}
	}

	public void defaultPrismForAll() {
		for (Region r : sim.getRegionManager().getRegions()) {
			for (Boundary b : r.getBoundaryManager().getBoundaries()) {
				try {
					b.get(MeshConditionManager.class).get(CustomizeBoundaryPrismsOption.class).setSelected(CustomizeBoundaryPrismsOption.DEFAULT);
					sim.println("WKN--> Default prism set for " + b.getPresentationName() + " in region " + r.getPresentationName());
				} catch (NeoException e) {
					//sim.println("WKN--> Could not reset prism for " + b.getPresentationName());
				}
			}
		}
	}

	public void setTargetSize(String regionName, String bString, double percentage) {

		Region region = sim.getRegionManager().getRegion(regionName);

		for (Boundary b : getBoundaries(region, bString)) {
			try {
				try {
					SurfaceSizeOption sopt = b.get(MeshConditionManager.class).get(SurfaceSizeOption.class);
					sopt.setSurfaceSizeOption(true);
				} catch (NeoException e) {
					//sim.println("WKN--> Could not set surface size option.");
				}

				SurfaceSize size = b.get(MeshValueManager.class).get(SurfaceSize.class);
				RelativeTargetSize relSize = size.getRelativeTargetSize();
				relSize.setPercentage(percentage);
				sim.println("WKN--> Did set set surface size on " + b.getPresentationName() + " to " + percentage);
			} catch (NeoException e) {
				//sim.println("WKN--> Could not set target size.");
			}
		}
	}

	public void createNormalExtrusion(String regionName, String boundaryName, int nLayers, double stretch) {

		Region region = sim.getRegionManager().getRegion(regionName);

		Boundary boundary_0 =
			region.getBoundaryManager().getBoundary(boundaryName);

		ExtrudeBoundaryOption extrudeBoundaryOption_0 =
			boundary_0.get(MeshConditionManager.class).get(ExtrudeBoundaryOption.class);

		extrudeBoundaryOption_0.getType().setSelected(ExtrusionTypeValue.CONSTANT_RATE_NORMAL);

		ExtrudeBoundaryNormalValues extrudeBoundaryNormalValues_0 =
			boundary_0.get(MeshValueManager.class).get(ExtrudeBoundaryNormalValues.class);

		extrudeBoundaryNormalValues_0.setAverageNormalOption(true);

		extrudeBoundaryNormalValues_0.setNumLayers(nLayers);

		extrudeBoundaryNormalValues_0.setStretching(stretch);

		extrudeBoundaryNormalValues_0.setExtruderNewRegionOption(true);

		extrudeBoundaryNormalValues_0.setNewRegionName("extrusion");

		extrudeBoundaryNormalValues_0.setBoundaryNames(new StringVector(new String[]{"interface_extrusion", "outlet", "wall_extrusion"}));
	}

	public void createMesh(boolean removeInvalid) {
		MeshPipelineController mesh = sim.get(MeshPipelineController.class);
		mesh.generateVolumeMesh();
		if (removeInvalid) {
			Collection<Region> regions = sim.getRegionManager().getObjects();
			MeshManager meshManager = sim.getMeshManager();
			meshManager.removeInvalidCells(new NeoObjectVector(regions.toArray()), 0.95, 0.0010, 1.0E-5, 1, 0.0, 0.0);
		}
	}
}
