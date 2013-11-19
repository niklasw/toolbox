// STAR-CCM+ macro: t.java
package SimulationReport;

import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import star.base.neo.*;
import star.common.*;

public class SimInfo {

    Simulation sim;

    /*
     * Not sure about the dimensions!!! But if correct, might come in handy...
     */
    public IntVector dimPressure = new IntVector(new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0});
    public IntVector dimLess = new IntVector(new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});
    public IntVector dimVelocity = new IntVector(new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0});
    public IntVector dimLength = new IntVector(new int[]{0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0});
	private SimPaths path = null;

    public SimInfo(Simulation s) {
        sim = s;
		path = new SimPaths(s);
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
	
    /**
	 * Dump starccm+ html info to file.
	 */
	public void dumpHtmlSummary() {
		String htmlFileName = path.fullPathNoExt() + ".html";
        new star.common.SimulationSummaryReporter().report(sim, htmlFileName);
    }

    /**
	 * Username of simulant
	 * @return
	 */
	public String username(){
	    return System.getProperty("user.name");
    }

    /**
         * Parse, in some way for PA name.
	 * Possibly use SimPaths::dirname() or part of SimPaths::basename()
	 * @return
	 */
	public String getPAName(){
	   return "NOT IMPLEMENTED";
    }

}
