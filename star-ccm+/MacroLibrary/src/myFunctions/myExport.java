// STAR-CCM+ macro: t.java
package myFunctions;

import java.util.*;
import java.io.File;
import star.common.*;
import star.base.neo.*;
import star.base.report.*;

public class myExport extends myCase {

    //Simulation sim;

    public myExport(Simulation s) {
	super(s);
    }

	public String dirPath(String subDir) {
		String path = dirname()+"/"+subDir+"/"+title();
		return path;
	}
	public String path(String subDir,String extension) {
		String path = dirPath(subDir)+"/"+title()+extension;
		return path;
	}
	public void toEnsight(List<String> scalarFieldNames, List<String> vectorFieldNames) {

		String expPath = path("Ensight",".case");

		File dir = new File(dirPath("Ensight"));

		dir.mkdirs();

		List<Region> regions = getRegions(".*");	
		List<Boundary> boundaries = new ArrayList();

		ImportManager importManager = sim.getImportManager();

		importManager.setExportPath(expPath);

		for (Region r: regions) {
			Info("Adding region "+r.getPresentationName());
			try{
				boundaries.addAll( getBoundaries(r,".*") );
			} catch (NeoException e){
				Info("Could not add boundaries to region "+ r.getPresentationName());
			}
		}

		Info("Number of regions added = "+ regions.size());
		Info("Number of boundaries added = "+ boundaries.size());

		importManager.setExportRegions(new NeoObjectVector(regions.toArray()));
		importManager.setExportBoundaries(new NeoObjectVector(boundaries.toArray()));

		
		List<PrimitiveFieldFunction> scalarFields = new ArrayList();
		List<PrimitiveFieldFunction> vectorFields = new ArrayList();
		for (String f: scalarFieldNames){
			scalarFields.add(getPrimitiveField(f));
		}
		for (String f: vectorFieldNames){
			vectorFields.add(getPrimitiveField(f));
		}

		importManager.setExportScalars(new NeoObjectVector(scalarFields.toArray()));
		importManager.setExportVectors(new NeoObjectVector(vectorFields.toArray()));

	    importManager.setExportOptionAppendToFile(false);
    	importManager.setExportOptionSolutionOnly(false);

		importManager.export(expPath,
				new NeoObjectVector(scalarFields.toArray()),
				new NeoObjectVector(vectorFields.toArray()));
	}
}