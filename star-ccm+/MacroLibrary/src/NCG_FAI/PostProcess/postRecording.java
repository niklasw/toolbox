// STAR-CCM+ macro: postRecording.java
package NCG_FAI.PostProcess;

import java.util.*;

import star.common.*;
import star.base.neo.*;
import star.vis.*;

import myFunctions.*;

public class postRecording extends StarMacro {

  public void execute() {
    execute0();
  }

  private void execute0() {

    Simulation simulation_0 = 
      getActiveSimulation();


    myCase myC = new myCase(simulation_0);
    myPost myP = new myPost(simulation_0);

    String simFileName = simulation_0.getSessionPath();
    String simTitle = simFileName.substring(0,simFileName.lastIndexOf("."));
    String CWD = System.getProperty("user.dir");

    SceneManager scnMgr = simulation_0.getSceneManager();
    for (Scene s: scnMgr.getScenes())
    {
        scnMgr.deleteScene(s);
    }

    PartManager partMgr = simulation_0.getPartManager();

    partMgr.removeObjects(partMgr.getObjects());

    scnMgr.createScalarScene("Recorded Scene", "Outline", "Scalar");

    Scene scene_4 = 
      simulation_0.getSceneManager().getScene("Recorded Scene 1");

    scene_4.initializeAndWait();

    PartDisplayer partDisplayer_1 = 
      ((PartDisplayer) scene_4.getCreatorDisplayer());

    partDisplayer_1.initialize();

    PartDisplayer partDisplayer_0 = 
      ((PartDisplayer) scene_4.getDisplayerManager().getDisplayer("Outline 1"));

    partDisplayer_0.initialize();

    scene_4.open(true);

    PartDisplayer partDisplayer_2 = 
      ((PartDisplayer) scene_4.getHighlightDisplayer());

    partDisplayer_2.initialize();

    ScalarDisplayer scalarDisplayer_0 = 
      ((ScalarDisplayer) scene_4.getDisplayerManager().getDisplayer("Scalar 1"));

    scalarDisplayer_0.initialize();

    CurrentView currentView_0 = 
      scene_4.getCurrentView();

    myP.removeLogo(scene_4);

    currentView_0.setInput(new DoubleVector(new double[] {-0.3089536134122989, 0.46689671698059143, 0.4965230167814323}), new DoubleVector(new double[] {-0.3089536134122989, -5.580030238723631, 0.4965230167814323}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 1.5650598604800592, 1);

    scalarDisplayer_0.setFillMode(1);

    scalarDisplayer_0.setFaceCullMode(1);

    PartDisplayer partDisplayer_3 = 
      scene_4.getDisplayerManager().createPartDisplayer("Geometry", -1, 4);

    partDisplayer_3.initialize();

    scalarDisplayer_0.setFaceCullMode(0);
    scalarDisplayer_0.getScalarDisplayQuantity().setClip(0);
    scalarDisplayer_0.getLegend().setVisible(false);

    Region region_0 = 
      simulation_0.getRegionManager().getRegion("a_upstream");

    Region region_1 = 
      simulation_0.getRegionManager().getRegion("c_downstream");

    Region region_2 = 
      simulation_0.getRegionManager().getRegion("b_filter");

    List<Boundary> wallBoundaries = myC.getBoundaries(region_0,"wall");

    wallBoundaries.addAll(myC.getBoundaries(region_1,"pipe"));

    List<Boundary> filterInterfaces = myC.getBoundaries(region_2,"interface");

    DirectBoundaryInterfaceBoundary directBoundaryInterfaceBoundary_0 = 
      ((DirectBoundaryInterfaceBoundary) region_0.getBoundaryManager().getBoundary("filter_interface_outer [a_upstream/b_filter]"));

    DirectBoundaryInterfaceBoundary directBoundaryInterfaceBoundary_1 = 
      ((DirectBoundaryInterfaceBoundary) region_1.getBoundaryManager().getBoundary("filter_interface_inner [b_filter/c_downstream]"));

    partDisplayer_3.getParts().setObjects(wallBoundaries);

    partDisplayer_3.setSurface(true);

    myP.verticalLegend(scalarDisplayer_0);

    currentView_0.setInput(new DoubleVector(new double[] {-1.0141493970837205, 0.14278908958447456, 0.5086222912243563}), new DoubleVector(new double[] {-1.0141493970837205, -5.580030238723631, 0.5086222912243563}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.8309564336229026, 1);

    partDisplayer_3.setFaceCullMode(1);

    Units units_0 = 
      simulation_0.getUnitsManager().getPreferredUnits(new IntVector(new int[] {0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}));

    scene_4.getCreatorGroup().setObjects(region_0, region_1, region_2);

    StreamDisplayer streamDisplayer_0 = 
      scene_4.getDisplayerManager().createStreamDisplayer("Streamline Stream");

    PrimitiveFieldFunction primitiveFieldFunction_0 = 
      ((PrimitiveFieldFunction) simulation_0.getFieldFunctionManager().getFunction("Velocity"));

    StreamPart streamPart_0 = 
      simulation_0.getPartManager().createStreamPart(new NeoObjectVector(simulation_0.getRegionManager().getRegions().toArray()), new NeoObjectVector( filterInterfaces.toArray()), primitiveFieldFunction_0, 5, 5, 2);

    streamPart_0.setPresentationName("myStreamline");

    streamDisplayer_0.getParts().addParts(streamPart_0);

    VectorMagnitudeFieldFunction vectorMagnitudeFieldFunction_0 = 
      ((VectorMagnitudeFieldFunction) primitiveFieldFunction_0.getMagnitudeFunction());

    streamDisplayer_0.getScalarDisplayQuantity().setFieldFunction(vectorMagnitudeFieldFunction_0);

    SourceSeed sourceSeed_0 = 
      streamPart_0.getSourceSeed();

    sourceSeed_0.getSeedParts().setObjects(directBoundaryInterfaceBoundary_1);

    streamDisplayer_0.setMode(2);

    streamDisplayer_0.setWidth(0.0020);

    myP.verticalLegend(streamDisplayer_0);

    scalarDisplayer_0.getLegend().setVisible(false);

    currentView_0.setInput(new DoubleVector(new double[] {-0.8733628980056887, 1.0228812335969257, 0.565898966451489}), new DoubleVector(new double[] {-0.8733628980056887, -5.580030238723627, 0.565898966451489}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.8868372200408026, 1);

    myP.showAllOutline(scene_4,false);

    simulation_0.println("HardCopy");
    scene_4.printAndWait(resolvePath(CWD+"/"+simTitle+"_strls_side1.png"), 1, 1000,1200);

    currentView_0.setInput(new DoubleVector(new double[] {-0.944014585257592, 1.0185277103425259, 0.34842264415174345}), new DoubleVector(new double[] {-0.944014585257592, 7.625792705917477, 0.34842264415174345}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.6465950746286993, 1);

    streamDisplayer_0.getScalarDisplayQuantity().setRange(new DoubleVector(new double[] {0.0, 60.0}));

    simulation_0.println("HardCopy");
    scene_4.printAndWait(resolvePath(CWD+"/"+simTitle+"_strls_side1.png"), 1, 1000,1200);

    currentView_0.setInput(new DoubleVector(new double[] {-0.944014585257592, 1.0185277103425259, 0.34842264415174345}), new DoubleVector(new double[] {-0.944014585257592, -5.588737285232427, 0.34842264415174345}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.6465950746286993, 1);

    simulation_0.println("HardCopy");
    scene_4.printAndWait(resolvePath(CWD+"/"+simTitle+"_strls_side2.png"), 1, 1000,1200);

    currentView_0.setInput(new DoubleVector(new double[] {-0.944014585257592, 1.0185277103425259, 0.34842264415174345}), new DoubleVector(new double[] {-7.551279580832544, 1.0185277103425259, 0.34842264415174345}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.6465950746286993, 1);

    currentView_0.setInput(new DoubleVector(new double[] {-1.2744918229590088, 0.8868139419606593, 0.39447082884922624}), new DoubleVector(new double[] {-7.551279580832544, 0.8868139419606593, 0.39447082884922624}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.7112495175158121, 1);

    simulation_0.println("HardCopy");
    scene_4.printAndWait(resolvePath(CWD+"/"+simTitle+"_strls_front.png"), 1, 1000,1200);

    currentView_0.setInput(new DoubleVector(new double[] {-1.2659759881506591, 0.8868139419606593, 0.3914602488809054}), new DoubleVector(new double[] {5.0193276045312265, 0.8868139419606593, 0.3914602488809054}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.7112495175158121, 1);

    simulation_0.println("HardCopy");
    scene_4.printAndWait(resolvePath(CWD+"/"+simTitle+"_strls_back.png"), 1, 1000,1200);

    streamDisplayer_0.getHiddenParts().addObjects(streamPart_0);

    partDisplayer_3.getHiddenParts().addObjects(wallBoundaries);

    partDisplayer_3.getHiddenParts().addObjects(directBoundaryInterfaceBoundary_1, directBoundaryInterfaceBoundary_0);

    scalarDisplayer_0.getParts().setObjects(directBoundaryInterfaceBoundary_0);

    PrimitiveFieldFunction primitiveFieldFunction_1 = 
      ((PrimitiveFieldFunction) simulation_0.getFieldFunctionManager().getFunction("TotalPressure"));

    scalarDisplayer_0.getScalarDisplayQuantity().setFieldFunction(primitiveFieldFunction_1);

    scalarDisplayer_0.getHiddenParts().addObjects(filterInterfaces);

    scalarDisplayer_0.getLegend().setVisible(true);

    scalarDisplayer_0.getScalarDisplayQuantity().setRange(new DoubleVector(new double[] {3000.0, 5000.0}));

    currentView_0.setInput(new DoubleVector(new double[] {-0.954567408039023, 0.9217672149723715, -0.01613585024062692}), new DoubleVector(new double[] {-0.954567408039023, -4.90717174605668, -0.01613585024062692}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.3404297551151202, 1);

    simulation_0.println("HardCopy");
    scene_4.printAndWait(resolvePath(CWD+"/"+simTitle+"_pTotFilter_side1.png"), 1, 1000,1200);

    currentView_0.setInput(new DoubleVector(new double[] {-0.954567408039023, 0.926773528296347, -0.015415363986415027}), new DoubleVector(new double[] {-0.954567408039023, 6.760718802649372, -0.015415363986415027}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.3404297551151202, 1);

    simulation_0.println("HardCopy");
    scene_4.printAndWait(resolvePath(CWD+"/"+simTitle+"_pTotFilter_side2.png"), 1, 1000,1200);

    currentView_0.setInput(new DoubleVector(new double[] {-0.8868642289936409, 0.9604463378971744, 0.17312019697929965}), new DoubleVector(new double[] {-0.8868642289936409, 6.760718802649372, 0.17312019697929965}), new DoubleVector(new double[] {0.0, 0.0, 1.0}), 0.8028202387392223, 1);

    partDisplayer_3.getParts().addParts(wallBoundaries);

    partDisplayer_3.getHiddenParts().setObjects();

    partDisplayer_3.getHiddenParts().addObjects(wallBoundaries);

    scalarDisplayer_0.getParts().setObjects(wallBoundaries);

    partDisplayer_2.getParts().setObjects(directBoundaryInterfaceBoundary_0);

    partDisplayer_2.getParts().setObjects();

    scalarDisplayer_0.getParts().addParts(filterInterfaces);

    scalarDisplayer_0.getHiddenParts().setObjects();

    scalarDisplayer_0.getHiddenParts().addObjects(wallBoundaries);

    scalarDisplayer_0.getParts().addParts(wallBoundaries);

    scalarDisplayer_0.getHiddenParts().setObjects();

    scalarDisplayer_0.getScalarDisplayQuantity().setClip(0);

    scalarDisplayer_0.getScalarDisplayQuantity().setRange(new DoubleVector(new double[] {1000.0, 6000.0}));

    scalarDisplayer_0.getScalarDisplayQuantity().setRange(new DoubleVector(new double[] {1000.0, 5800.0}));

    partDisplayer_0.getHiddenParts().addObjects(myC.getBoundaries(region_0,"wall_box_ext"));

    scalarDisplayer_0.getHiddenParts().addObjects(myC.getBoundaries(region_0,"wall_box_ext"));

    PrimitiveFieldFunction primitiveFieldFunction_2 = 
      ((PrimitiveFieldFunction) simulation_0.getFieldFunctionManager().getFunction("Pressure"));

    scalarDisplayer_0.getScalarDisplayQuantity().setFieldFunction(primitiveFieldFunction_2);

    scalarDisplayer_0.getScalarDisplayQuantity().setRange(new DoubleVector(new double[] {-5000.0, 5500.0}));

    currentView_0.setInput(new DoubleVector(new double[] {-0.6286647330492445, 0.4012228265441613, 0.5794620719035678}), new DoubleVector(new double[] {6.188961097838284, 4.3886186398325355, 1.476604124342846}), new DoubleVector(new double[] {-0.12274258785707874, -0.013408262287437328, 0.9923479609635819}), 0.8883109614975028, 1);

    simulation_0.println("HardCopy");
    scene_4.printAndWait(resolvePath(CWD+"/"+simTitle+"_wallPressure_1.png"), 1, 1175, 945);

  }
}
