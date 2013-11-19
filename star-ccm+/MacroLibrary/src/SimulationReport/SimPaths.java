/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package SimulationReport;

/**
 *
 * @author niklasw
 */
import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import star.base.neo.*;
import star.common.*;

public class SimPaths extends SimInfo {
	
	public SimPaths(Simulation s) {
        super(s);
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
        List<String> found = new LinkedList<>();
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

	
}
