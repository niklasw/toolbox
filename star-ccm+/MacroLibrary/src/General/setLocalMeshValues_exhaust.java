// STAR-CCM+ macro: t.java
package General;


import java.util.Arrays;
import java.util.List;
import star.common.*;

import myFunctions.*;

public class setLocalMeshValues_exhaust extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation = getActiveSimulation();

    myMeshing myF = new myMeshing(simulation);

    myF.defaultPrismForAll();

    List<String> noPrisms = Arrays.asList(
	    "inlet",
	    "outlet",
	    "ambience",
	    "ambient",
	    "interface",
	    "edge"
	    );

    double huge = 1000;
    double large = 250;
    double normal = 100;
    double small = 50;
    double tiny	 = 25;

    List<String> huges = Arrays.asList(
	    "ambience",
	    "ambient"
	    );
    
    List<String> larges = Arrays.asList(
	    );

    List<String> normals = Arrays.asList(
	    "wall"
	    );
    
    List<String> smalls = Arrays.asList(
	    "ejector"
	    );
    
    List<String> tinies = Arrays.asList(
	    "edge"
	    );
    

    List<Region> regions = myF.getRegions(".*"); 
    for (Region r: regions)
    {
	    myF.Info(r.getPresentationName());
	    for (String s: huges)
	    {
	    	myF.setTargetSize(r.getPresentationName(), s, huge);
	    }
	    for (String s: larges)
	    {
	    	myF.setTargetSize(r.getPresentationName(), s, large);
	    }
	    for (String s: normals)
	    {
	    	myF.setTargetSize(r.getPresentationName(), s, normal);
	    }
	    for (String s: smalls)
	    {
	    	myF.setTargetSize(r.getPresentationName(), s, small);
	    }
	    for (String s: tinies)
	    {
	    	myF.setTargetSize(r.getPresentationName(), s, tiny);
	    }
	    for (String s: noPrisms)
	    {
	    	myF.disablePrism(r.getPresentationName(), s);
	    }
    }
  }
}
