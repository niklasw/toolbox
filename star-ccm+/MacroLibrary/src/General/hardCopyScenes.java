// STAR-CCM+ macro: t.java
package General;


import NCG_FAI.PostProcess.*;
import java.util.Collection;
import star.common.*;
import star.vis.*;
import myFunctions.*;

public class hardCopyScenes extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation SIM = getActiveSimulation();
    myPost myP = new myPost(SIM);

    int xrez = 1250;
    int yrez = 950;
    
    Collection<Scene> allScenes = SIM.getSceneManager().getScenes();

    for (Scene s: allScenes)
    {
	myP.removeLogo(s);
	String sceneName = s.getPresentationName();
	String imgFileName = myP.fullPathNoExt()+sceneName+".png"; 
	SIM.println("WKN --> Saving image "+ imgFileName);
	s.printAndWait(imgFileName,1,xrez,yrez);
    }
  }
}
