/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package NCG_FAI.PostProcess;

/**
 *
 * @author konwkn
 */
import java.util.*;
import star.common.*;
import star.base.neo.*;
import star.vis.*;
import myFunctions.*;

public class turbopipeViews extends StarMacro{
  public void execute() {
    execute0();
  }

  private void execute0() {


    Simulation SIM = getActiveSimulation();

    myCase myC = new myCase(SIM);

    String pwd = myC.pwd();

    Scene scene = SIM.getSceneManager().getScene("turbopipe");

    CurrentView currentView = scene.getCurrentView();

    currentView.setInput(new DoubleVector(new double[] {-0.75, 0.5, 0.5}),
	    new DoubleVector(new double[] {-0.5,0.5, 0.5}),
	    new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.35, 1);

    myC.Info("Writing to "+myC.pwd());
    scene.printAndWait(myC.pwdFile("turboPipeView_1.png"), 1, 1500, 1000);

    currentView.setInput(new DoubleVector(new double[] {-0.75, 0.5, 0.5}),
	    new DoubleVector(new double[] {-0.75,1.0, 0.5}),
	    new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.35, 1);

    myC.Info("Writing to "+myC.pwd());
    scene.printAndWait(myC.pwdFile("turboPipeView_2.png"), 1, 1500, 1000);

    currentView.setInput(new DoubleVector(new double[] {-0.75, 0.5, 0.5}),
	    new DoubleVector(new double[] {-0.75,-1.0, 0.5}),
	    new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.35, 1);

    myC.Info("Writing to "+myC.pwd());
    scene.printAndWait(myC.pwdFile("turboPipeView_3.png"), 1, 1500, 1000);

    currentView.setInput(new DoubleVector(new double[] {-0.75, 0.5, 0.5}),
	    new DoubleVector(new double[] {-0.75,-1.0, 0.2}),
	    new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.35, 1);

    myC.Info("Writing to "+myC.pwd());
    scene.printAndWait(myC.pwdFile("turboPipeView_4.png"), 1, 1500, 1000);
/*
    currentView.setInput(new DoubleVector(new double[] {-1.0, 1.0, 0.0}),
	    new DoubleVector(new double[] {-1.001616825066636, 0.4243133883045711, 0.01}),
	    new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.28, 1);

    scene.printAndWait(myC.pwdFile("turboPipeView_2.png"), 1, 1500, 1000);

    currentView.setInput(new DoubleVector(new double[] {-1.0, 1.0, 0.0}),
	    new DoubleVector(new double[] {-1.5684074654207942, 0.9911040286587296, 0.01}),
	    new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.28, 1);

    scene.printAndWait(myC.pwdFile("turboPipeView_3.png"), 1, 1500, 1000);

    currentView.setInput(new DoubleVector(new double[] {-1.0, 1.0, 0.0}),
	    new DoubleVector(new double[] {-0.4348261847124778, 0.9911040286587296, 0.01}),
	    new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.28, 1);

    scene.printAndWait(myC.pwdFile("turboPipeView_4.png"), 1, 1500, 1000);
    
    currentView.setInput(new DoubleVector(new double[] {-1.0, 1.0, 0.0}),
	    new DoubleVector(new double[] {-0.4348261847124778, 0.9911040286587296, 0.01}),
	    new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.28, 1);


    scene.printAndWait(myC.pwdFile("turboPipeView_5.png"), 1, 1500, 1000);

    currentView.setInput(new DoubleVector(new double[] {-0.9868792723168484, 0.9803271878114728, 0.04242087377191933}),
	    new DoubleVector(new double[] {-1.507367555851756, 0.5293939656911624, -0.25682403977436197}),
	    new DoubleVector(new double[] {-0.17260187503359808, -0.3985342495963088, 0.9007658100936076}), 0.24475826337813672, 1);
 */
  }

	
}
