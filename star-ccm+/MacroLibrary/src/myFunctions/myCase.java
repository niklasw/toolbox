// STAR-CCM+ macro: t.java
package myFunctions;

import java.util.*;

import java.io.*;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

import star.common.*;
import star.base.neo.*;
import star.base.report.*;
import star.flow.*;
import star.energy.*;

public class myCase {

    Simulation sim;

    /*
     * Not sure about the dimensions!!!
     */
    public IntVector dimPressure = new IntVector(new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0});
    public IntVector dimLess = new IntVector(new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});
    public IntVector dimVelocity = new IntVector(new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0});
    public IntVector dimLength = new IntVector(new int[]{0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});

    public myCase(Simulation s) {
        sim = s;
    }

    /* General */
    /**
     * Simple messages to stdout. Shown on command line and in GUI.
     *
     * @param infoStr
     */
    public void Info(String infoStr) {
        sim.println("WKN --> " + infoStr);
    }

    /**
     * Simple messages to stdout. Shown on command line and in GUI. With two
     * strings that becomes concatenated.
     *
     * @param infoStr
     * @param infoStr2
     */
    public void Info(String infoStr1, String infoStr2) {
        Info(infoStr1 + " " + infoStr2);
    }

    public void Warning(String infoString){
	Info("WARNING!! -- "+infoString);
    }

    /**
     * Returns the OS dependant file separator.
     *
     * @return
     */
    public String sep() {
        return File.separator;
    }

    /**
     * Returns the name of the sim file (like shell basename)
     *
     * @return
     */
    public String basename() {
        String simFile = sim.getSessionPath();
        String simFileName = simFile.substring(simFile.lastIndexOf(File.separator) + 1);
        return simFileName;
    }

    /**
     * Returns the file name (like basename) but without the suffix.
     *
     * @return
     */
    public String title() {
        String fileName = basename();
        return fileName.substring(0, fileName.lastIndexOf("."));
    }

    /**
     * Returns the session dir path.
     *
     * @return
     */
    public String dirname() {
        return sim.getSessionDir();
    }

    public String directoryname() {
        return dirname().substring(dirname().lastIndexOf(File.separator) + 1);
    }

    public String fullPath() {
        return dirname() + sep() + basename();
    }

    public String fullPathNoExt() {
        return dirname() + sep() + title();
    }

    public String pwd() {
        return System.getProperty("user.dir");
    }

    public String pwdFile(String fileName) {
        return pwd() + sep() + fileName;
    }

    public List<String> findFile(String prefix, String pattern) {
        File dir = new File(prefix);
        String[] files = dir.list();
        List<String> found = new LinkedList<String>();
        Pattern pat = Pattern.compile(pattern);
        for (String f : files) {
            Matcher match = pat.matcher(f);
            if (match.find()) {
                found.add(new File(prefix, f).toString());
            }
        }
        return found;
    }

    public String basenameNoExt(String path) {
        return path.substring(path.lastIndexOf("/") + 1, path.lastIndexOf("."));
    }

    public void pathInfo() {
        String CWD = System.getProperty("user.dir");
        String simDirName = CWD.substring(CWD.lastIndexOf("/") + 1);
        Info("WKN --> " + CWD + " " + simDirName);
    }

    public void writeSummary() {
        new star.common.SimulationSummaryReporter().report(sim, fullPathNoExt() + ".html");
    }

    /**
     * Returns a list of boundaries from a region which names matches the
     * boundaryString argument. Matching is made with the String.contains
     * function. Change to regexp?
     *
     * @param region
     * @param boundaryString
     * @return
     */
    public List<Boundary> getBoundaries(Region region, String boundaryString) {
        List<Boundary> bnds = new ArrayList(region.getBoundaryManager().getBoundaries());
        List<Boundary> keepBnds = new ArrayList();
        for (Boundary b : bnds) {
            if (b.getPresentationName().matches(boundaryString)) {
                keepBnds.add(b);
            }
        }
        if (keepBnds.isEmpty()) {
            Info("Could not find any boundary containing name " + boundaryString 
                    + " in region " + region.getPresentationName());
        }
        return keepBnds;
    }

    public List<InterfaceBoundary> getInterfaces(Region region, String boundaryString) {
        Collection<Boundary> bnds = new ArrayList(region.getBoundaryManager().getObjects());
        List<InterfaceBoundary> keepBnds = new ArrayList();
        for (Object b : bnds) {
            if (b instanceof InterfaceBoundary) {
                InterfaceBoundary i = (InterfaceBoundary) b;
                if (i.getPresentationName().contains(boundaryString)) {
                    keepBnds.add(i);
                }
            }
        }
        if (keepBnds.isEmpty()) {
            Info("Could not find any interface containing name " + boundaryString
                + " in region " + region.getPresentationName());
        }
        return keepBnds;
    }

    public List<Region> getRegions(String regionMatchPat) {
        /*Collects regions matching regex to a List*/
        List<Region> selected;
        selected = new ArrayList();
        Collection<Region> regions = sim.getRegionManager().getRegions();
        for (Region r : regions) {
            if (r.getPresentationName().matches(regionMatchPat)) {
                selected.add(r);
            }
        }
        return selected;
    }

    public void stripBoundaryNames(Region r) {
        /*Removes strings before last dot in boundary name.
         * E.g. cleans part names from boundary names*/
        for (Boundary b : r.getBoundaryManager().getBoundaries()) {
            String name = b.getPresentationName();
            if (name.contains(".")) {
                String newName = name.substring(name.lastIndexOf(".") + 1);
                b.setPresentationName(newName);
                Info("Renaming " + name + " -> " + newName);
            }
        }
    }

	public PrimitiveFieldFunction getPrimitiveField(String name) {
		Info("getPrimitiveField "+name);
		return ((PrimitiveFieldFunction) sim.getFieldFunctionManager().getFunction(name));
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

    /*Boundary conditions
     * Set of functions to spec BCs on boundaries in a specified region
     * where boundary name matches the String bString.
     */
    public void setInletTemperature(String regionName, String bString, double value, String unit) {
        Region region = sim.getRegionManager().getRegion(regionName);

        Units tempUnit = ((Units) sim.getUnitsManager().getObject(unit));

        Collection<Boundary> bnds = getBoundaries(region, bString);

        if (bnds != null) {

            for (Boundary b : bnds) {
                try {
                    TotalTemperatureProfile profile = b.getValues().get(TotalTemperatureProfile.class);
                    profile.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(value);
                    profile.getMethod(ConstantScalarProfileMethod.class).getQuantity().setUnits(tempUnit);
                    Info("Did set fix temperature condition for " + b.getPresentationName() + " in region " + region.getPresentationName());
                } catch (NeoException e) {
                    Info("Could not set boundary condition for " + b.getPresentationName());
                }
            }
        }
    }

    public void setInletMassFlux(String regionName, String bString, double value) {
        Region region = sim.getRegionManager().getRegion(regionName);

        Collection<Boundary> bnds = getBoundaries(region, bString);

        if (bnds != null) {

            for (Boundary b : bnds) {
                try {
                    b.setBoundaryType(MassFlowBoundary.class);
                    MassFlowRateProfile profile = b.getValues().get(MassFlowRateProfile.class);
                    profile.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(value);
                    Info("Did set mass flow rate condition for "
                        + b.getPresentationName() + " in region " + region.getPresentationName());
                } catch (NeoException e) {
                    Info("Could not set boundary condition for " + b.getPresentationName());
                }
            }
        }
    }

    public void setWall(String regionName, String bString) {

        Region region = sim.getRegionManager().getRegion(regionName);

        for (Boundary b : getBoundaries(region, bString)) {
            try {
                b.setBoundaryType(WallBoundary.class);
                Info("Did set wall condition for "
                    + b.getPresentationName() + " in region " + region.getPresentationName());
            } catch (NeoException e) {
                Info("Could not set boundary condition for " + b.getPresentationName());
            }
        }
    }

    public void setSlipWall(String regionName, String bString) {

        Region region = sim.getRegionManager().getRegion(regionName);

        for (Boundary b : getBoundaries(region, bString)) {
            try {
                b.setBoundaryType(WallBoundary.class);
                b.getConditions().get(WallShearStressOption.class).setSelected(WallShearStressOption.SLIP);
                Info("Did set slip wall condition for "
                    + b.getPresentationName() + " in region " + region.getPresentationName());
            } catch (NeoException e) {
                Info("Could not set boundary condition for " + b.getPresentationName());
            }
        }
    }

    public void setPressureOutlet(String regionName, String bString, double value) {

        Region region = sim.getRegionManager().getRegion(regionName);

        for (Boundary b : getBoundaries(region, bString)) {
            try {
                b.setBoundaryType(PressureBoundary.class);
                StaticPressureProfile profile = b.getValues().get(StaticPressureProfile.class);
                profile.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(value);
                Info("Did set pressure outlet condition for "
                    + b.getPresentationName() + " in region " + region.getPresentationName());
            } catch (NeoException e) {
                Info("Could not set boundary condition for " + b.getPresentationName());
            }
        }
    }

    /**
     * The set boundary condition function sets a specific BC type and value
     * depending on function used, to a boundary in selected region with
     * name matching bString. Uses the getBoundaries function.
     *
     * @param regionName
     * @param bString
     * @param value
     */
    public void setStagnationInlet(String regionName, String bString, double value) {

        Region region = sim.getRegionManager().getRegion(regionName);

        for (Boundary b : getBoundaries(region, bString)) {
            try {
                b.setBoundaryType(StagnationBoundary.class);
                TotalPressureProfile totalPressure = b.getValues().get(TotalPressureProfile.class);
                totalPressure.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(value);
                Info("Did set stagnation inlet to "
                    + value + " Pa for " + b.getPresentationName() + " in region " + region.getPresentationName());
            } catch (NeoException e) {
                Info("Could not set boundary condition for " + b.getPresentationName());
            }
        }
    }

    public void setTargetMassflowOutlet(String regionName, String bString, double value, double targetValue) {

        Region region = sim.getRegionManager().getRegion(regionName);

        for (Boundary b : getBoundaries(region, bString)) {
            try {
                b.setBoundaryType(PressureBoundary.class);
                b.getConditions().get(TargetMassFlowOption.class).setTargetMassFlowOption(true);
                b.getValues().get(TargetMassFlowPressureAdjuster.class).getMassFlowRate().setValue(targetValue);
                StaticPressureProfile profile = b.getValues().get(StaticPressureProfile.class);
                profile.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(value);
                Info("Did set pressure outlet condition for " + b.getPresentationName() + " in region " + region.getPresentationName());
            } catch (NeoException e) {
                Info("Could not set boundary condition for " + b.getPresentationName());
            }
        }
    }

    public void matchCsysToPorousResistance(String csysName, String regionName) {

        Region region = sim.getRegionManager().getRegion(regionName);

        region.setRegionType(PorousRegion.class);

        PorousInertialResistance pI = region.getValues().get(PorousInertialResistance.class);
        VectorProfile vectorInertialX = pI.getMethod(PrincipalTensorProfileMethod.class).getXAxis();
        VectorProfile vectorInertialY = pI.getMethod(PrincipalTensorProfileMethod.class).getYAxis();

        PorousViscousResistance pV = region.getValues().get(PorousViscousResistance.class);
        VectorProfile vectorViscX = pV.getMethod(PrincipalTensorProfileMethod.class).getXAxis();
        VectorProfile vectorViscY = pV.getMethod(PrincipalTensorProfileMethod.class).getYAxis();

        LabCoordinateSystem labCoordinateSystem = sim.getCoordinateSystemManager().getLabCoordinateSystem();

        Collection<CoordinateSystem> lcs = labCoordinateSystem.getLocalCoordinateSystemManager().getObjects();

        for (CoordinateSystem cs : lcs) {
            if (cs.getPresentationName().contains(csysName)) {
                    CartesianCoordinateSystem clcs = (CartesianCoordinateSystem) cs;
                    Info("Selected LCS for porous region " + regionName + " = " + clcs.getPresentationName());
                    vectorInertialX.setCoordinateSystem(clcs);
                    vectorInertialY.setCoordinateSystem(clcs);
                    vectorViscX.setCoordinateSystem(clcs);
                    vectorViscY.setCoordinateSystem(clcs);
                    break;
            }
        }
    }

    public void setPorousResistance(String regionName, double[] inertial, double[] viscous) {

        Region region = sim.getRegionManager().getRegion(regionName);

        region.setRegionType(PorousRegion.class);

        PorousInertialResistance pI = region.getValues().get(PorousInertialResistance.class);
        PorousViscousResistance pV = region.getValues().get(PorousViscousResistance.class);
        Info("Set porous resistances to region " + regionName);
        for (int i = 0; i < 3; i++) {
            Info("Set porous inertial component " + i + " to " + inertial[i]);
            pI.getMethod(PrincipalTensorProfileMethod.class).getProfile(i).setValue(inertial[i]);
            Info("Set porous viscous component  " + i + " to " + viscous[i]);
            pV.getMethod(PrincipalTensorProfileMethod.class).getProfile(i).setValue(viscous[i]);
        }
    }

    public void matchCsysToRegion(String csysName, String regionName) {

        Region region = sim.getRegionManager().getRegion(regionName);

        ReferenceFrame referenceFrame = region.getValues().get(ReferenceFrame.class);

        LabCoordinateSystem labCoordinateSystem = sim.getCoordinateSystemManager().getLabCoordinateSystem();

        Collection<CoordinateSystem> lcs = labCoordinateSystem.getLocalCoordinateSystemManager().getObjects();

        for (CoordinateSystem cs : lcs) {
            if (cs.getPresentationName().contains(csysName)) {
                CylindricalCoordinateSystem clcs = (CylindricalCoordinateSystem) cs;
                Info("Selected LCS for porous region " + regionName + " = " + clcs.getPresentationName());
                referenceFrame.setCoordinateSystem(clcs);
                break;
            }

        }
    }
}