/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\
     ___________________________
    |                           |___________________
   O|  Gas Spring calculator.   |___________________O
    |___________________________|


   Developed on Visual Studio Express 2012.
   And Linux, Vim, Mono and Wine. Deployed to Windows 7+.
   Depends on .NET-4

   Copyright:               Lesjofors AB
   Original author:         Niklas Wikstrom, FS Dynamics AB
   Author contact:          niklas.wikstrom@gmail.com
   Year of first release:   2013
   Version:                 1.0-beta

\* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */


using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;
using System.Diagnostics;
using PdfSharp;
using PdfSharp.Drawing;
using PdfSharp.Pdf;
using PdfSharp.Pdf.IO;

namespace HatchTest
{
    public partial class SpringForms : Form
    {
        /*
         * Yes, this is a huge main class. Not satisfactory really, and should be split in
         * several classes. No time though.
         * First of all, a file management internal class perhaps.
         */

        private string tempPath_;
        private string saveStateFileName_;
        private string saveDesignerFileName_;
        private string databaseXls_ = "Gassprings.xls";

        private readonly Point hatchImageSize_ = new Point(400,380);
        private Hatch myHatch_;
        private Bitmap hatchBitmap_;
        private SpringReader springReader_;
        private CorrectionsReader correctionsReader_;
        private EndFittingReader endFittingReader_;
        private SpringList availableSprings_;
        private EndFittingList availableEndFittings_;
        private EndFittingList currentEndFittings_;
        private Tuple<double, double> requiredSpringLengths_
                 = new Tuple<double, double>(0,0);
        private string lastThread_ =  "Welded";
        private string currentThread_ =  "Welded";
        private Spring currentSpring_;

        private Vector2D springOrigin_ = new Vector2D(0, 0);

        // Options form data storage
        private OptionsForm optionsForm_ = null;

        // Geometrical data
        //private Vector2D springOrigin_ = new Vector2D();
        //private Vector2D hatchOrigin_ = new Vector2D();

        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
         * Main constructor. This is where it starts.
         * Hatch components constructed and joined to a
         * Hatch object; Database parsed for springs and conns;
         * Window forms filled with initial data;
         * The rest is more or less handled by the event driven
         * functions, below.
         * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

        public SpringForms()
        {
            InitializeComponent();

            optionsForm_ = new OptionsForm(this);

            initializeSessionFiles();

            openDesignerData(saveDesignerFileName_);

            hatchBitmap_ = new Bitmap(hatchImageSize_.X,hatchImageSize_.Y);

            correctionsReader_ = new CorrectionsReader(databaseXls_);

            springReader_ = new SpringReader(databaseXls_);

            springReader_.springs.applyCorrections(correctionsReader_);

            availableSprings_ = new SpringList();

            availableSprings_.AddRange(springReader_.springs);

            endFittingReader_ = new EndFittingReader(databaseXls_);

            currentEndFittings_ = new EndFittingList
                                      (
                                          new EndFitting(),
                                          new EndFitting()
                                      );

            availableEndFittings_ = new EndFittingList();

            availableEndFittings_.AddRange(endFittingReader_.endFittings);

            showAvailableEndFittings();

            /*
             * Initialize the hatch (Hatch = Lid and Spring compound)
             */
            MechanicalObject lidBase= new MechanicalObject(new Object2D());

            Lid myLid = new Lid(lidBase,0,0);

            currentSpring_ = availableSprings_[0];

            currentSpring_.origin = springOrigin_;

            myHatch_ = new Hatch(myLid, currentSpring_);

            setDefaultValues();

            lidConnectPosInput.Value = (decimal) lidLengthInput.Value / 2;

            updateHatch();

            updateAvailableSprings(getStartAngle(),getStopAngle(),currentThread_);

            showAvailableSprings();
        }

        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
         * Event driven functions
         * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

        private void inputField_ValueChanged(object sender, EventArgs e)
        {
            updateHatch();
            updateInfoBoxes();
            SpringBox.BackColor = Color.LightGray;
        }

        private void ResetButton_Click(object sender, EventArgs e)
        {
            setDefaultValues();
            applyFormValues();
        }

        private void inputDataSubmitted(object sender, EventArgs e)
        {
            // HIDE Console.WriteLine("AVAIL N ="+availableSprings_.Count);

            double a0 = getStartAngle();
            double a1 = getStopAngle();

            myHatch_.setAngle(a0);

            SpringBox.BackColor = Color.White;

            updateAvailableSprings(a0, a1, currentThread_);

            {
                angleSlider.SetRange(-180, 180);
                sliderRadioLimitOff.Checked = true;
                angleSlider.Value = (int) a0;
            }

            updateHatch();

            showAvailableSprings();
        }

        private void threadSelect(object sender, EventArgs e)
        {
            lastThread_ = currentThread_;

            if (threadRadioAll.Checked) currentThread_ = "All";
            else if (threadRadioWeld.Checked) currentThread_ = "Welded";
            else if (threadRadioM6.Checked) currentThread_ = "M6";
            else if (threadRadioM8.Checked) currentThread_ = "M8";

            availableEndFittings_.Clear();

            availableEndFittings_.AddRange
            (
                endFittingReader_.endFittings.filterByThread(currentThread_)
            );

            endFittingTubeBox.SelectedIndex = 0;
            endFittingRodBox.SelectedIndex = 0;

            showAvailableEndFittings();
        }

        private void endFittingsSelect(object sender, EventArgs e)
        {
            // Default EndFitting is "Welded". Will be set if no selection made.
            // (No selection renders SelectedIndex = -1, I believe.
            // Since this function is called from rod and tube selection events,
            // Special care must be taken, not to end up outOfRange.
            EndFitting endFit0 = new EndFitting();
            EndFitting endFit1 = new EndFitting();

            if (endFittingTubeBox.SelectedIndex >= 0 && endFittingTubeBox.SelectedIndex < availableEndFittings_.Count)
            {
                endFit0 = availableEndFittings_[endFittingTubeBox.SelectedIndex];
            }
            if (endFittingRodBox.SelectedIndex >= 0 && endFittingRodBox.SelectedIndex < availableEndFittings_.Count)
            {
                endFit1 = availableEndFittings_[endFittingRodBox.SelectedIndex];
            }

            currentEndFittings_[0] = endFit0;
            currentEndFittings_[1] = endFit1;

            updateHatch();
        }

        private void springListSelect(object sender, EventArgs e)
        {
            currentSpring_ =  availableSprings_[SpringBox.SelectedIndex];

            updateHatch();

            updateSlider();

            updatePlot();
        }

        private void slideAngle(object sender, EventArgs e)
        {
            double currentAngle = angleSlider.Value;

            myHatch_.setAngle(rad(currentAngle));

            currentAngleLabel.Text = getOpeningDeg().ToString();

            updateInfoBoxes();

            drawHatchBitmap();
        }

        private void radioLimitSlide(object sender, EventArgs e)
        {
            updateSlider();
        }


        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
         * Helper functions
         * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

        private void showAvailableEndFittings()
        {
            string text = currentEndFittings_[0].name;
            endFittingTubeBox.Text = text;
            endFittingTubeBox.Items.Clear();

            endFittingTubeBox.Items.AddRange(availableEndFittings_.getNames().ToArray());

            text = currentEndFittings_[1].name;
            endFittingRodBox.Text = text;
            endFittingRodBox.Items.Clear();

            endFittingRodBox.Items.AddRange(availableEndFittings_.getNames().ToArray());
        }

        public static double deg(double a)
        {
            return a * 180 / Math.PI;
        }
        public static double rad(double a)
        {
            return a * Math.PI / 180.0;
        }

        public void warning(string warn)
        {
            toolStripStatusLabel1.Text = warn;
            toolStripStatusLabel1.ForeColor = Color.Orange;
        }

        public void notify(string warning)
        {
            System.Windows.Forms.MessageBox.Show(warning);
        }

        private void clearHatchBitmap()
        {
            hatchBitmap_ = new Bitmap(hatchBitmap_.Width, hatchBitmap_.Height);
        }

        private void drawHatchBitmap()
        {
            clearHatchBitmap();

            double scale = 0.6 * hatchImageSize_.X / myHatch_.lid.length;
            myHatch_.lid.visualScaleFactor = scale;
            myHatch_.spring.visualScaleFactor = scale;
            myHatch_.draw(hatchBitmap_);
            myHatch_.drawShadow(hatchBitmap_, getStopAngle());
            myHatch_.drawShadow(hatchBitmap_, getStartAngle());
            myHatch_.drawLimits(hatchBitmap);

            hatchBox.Image = hatchBitmap_;
        }

        private void updatePlot()
        {
            Title title = new Title("Hand force [N]. (@ "+temperatureInput.Value+ "ºC) Positive pulls lid.");
            chart1.Titles.Clear();
            chart1.Titles.Add(title);
            HandForces handForces = myHatch_.handForces;
            chart1.Series.Clear();
            chart1.Series.Add("Open");
            chart1.Series.Add("Close");
            chart1.Series.Add("Zero");
            chart1.Series["Open"].Color = Color.DarkRed;
            chart1.Series["Close"].Color = Color.DarkBlue;
            chart1.Series["Zero"].Color = Color.Black;

            chart1.Series["Open"].ChartType = 
                System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            chart1.Series["Close"].ChartType = 
                System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            chart1.Series["Zero"].ChartType =
                System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;

            for (int i = 0; i < handForces.deg.Count; i++)
            {
                double a = -handForces.deg[i]+deg(getStartAngle());

                // Sing of forces a matter of definition.

                chart1.Series["Open"].Points.AddXY(a, handForces.open[i]);

                chart1.Series["Close"].Points.AddXY(a, handForces.close[i]);

                chart1.Series["Zero"].Points.AddXY(a, 0.0);
            }

            double Xinterval = 10;
                //(double)Math.Round(Math.Abs(getStartAngle()-getStopAngle())/10,0);

            chart1.ChartAreas[0].AxisX.MajorGrid.Interval = Xinterval;
            chart1.ChartAreas[0].AxisX.MajorTickMark.Interval = Xinterval;

            //chart1.ChartAreas[0].AxisX.LabelStyle.Interval = Xinterval;
            LabelStyle style1 = new LabelStyle();
            style1.Format = "#.##";
            chart1.ChartAreas[0].AxisX.LabelStyle.Format = "#";
            chart1.ChartAreas[0].AxisX.LabelStyle.Interval = 10; 

            chart1.ChartAreas[0].AxisX.MajorGrid.LineDashStyle =
                System.Windows.Forms.DataVisualization.Charting.ChartDashStyle.Dash ;
            chart1.ChartAreas[0].AxisY.MajorGrid.LineDashStyle =
                chart1.ChartAreas[0].AxisX.MajorGrid.LineDashStyle;

            chart1.ChartAreas[0].AxisX.MajorGrid.LineColor = Color.Gray;
            chart1.ChartAreas[0].AxisY.MajorGrid.LineColor = Color.Gray;

            chart1.ChartAreas[0].AxisX.Title = "Lid opening angle";

            // Cubersome legend adding...
            chart1.Legends.Clear();
            chart1.Legends.Add(new Legend("HandForce"));
            chart1.Series["Open"].Legend = "HandForce";
            chart1.Series["Close"].Legend = "HandForce";
            chart1.Series["Zero"].IsVisibleInLegend = false;
            
            //chart1.Series["Open"].IsVisibleInLegend = true;
            chart1.Legends["HandForce"].LegendStyle = LegendStyle.Column;
        }
        
        private void updateSlider()
        {
            if (sliderRadioLimitOff.Checked)
            {
                angleSlider.SetRange(-180, 180);
            }
            else if (sliderRadioLimitInput.Checked)
            {
                int start = (int)Math.Round(deg(getStartAngle()));
                int stop  = (int)Math.Round(deg(getStopAngle()));
                angleSlider.SetRange(Math.Min(start,stop), Math.Max(start,stop));
            }
            else if (sliderRadioLimitSpring.Checked)
            {
                int a0 = (int) Math.Round(myHatch_.minSpringDeg);
                int a1 = (int) Math.Round(myHatch_.maxSpringDeg);
                angleSlider.SetRange(a1, a0);
            }
        }

        private void updateHatch(bool redraw = true)
        {
            applyFormValues();

            currentSpring_.changeEndFittings(currentEndFittings_);

            myHatch_.changeSpring(currentSpring_);

            myHatch_.doMotionSweep(myHatch_.lid.angle);

            updateInfoBoxes();

            if (redraw)
            {
                drawHatchBitmap();
            }

            // Necessary to update slider ranges, depending on radio slider limit states
            updateSlider();

            // HIDE Console.WriteLine( myHatch_.hatchInfo() );
        }

        private void updateAvailableSprings
        (
            double a0,
            double a1,
            string thread
        )
        {
            // OBS: Compared to springs in springList. These are all
            // Welded from start.

            requiredSpringLengths_ =
                myHatch_.requiredSpringLengths(a0, a1);

            double minDist = requiredSpringLengths_.Item1
                           - currentEndFittings_.sumLengths();

            double maxDist = requiredSpringLengths_.Item2
                           - currentEndFittings_.sumLengths();

            SpringList inRangeSprings;
            inRangeSprings = filterSpringsInRange(a0, a1, springReader_.springs);

            // Now, find among inRangeSprings, items that manage the overshoot 
            // angle in both directions. Then remove these, since we don't want
            // unnecessary stroke. NOT IMPLEMENTED

            SpringList matchingThreadSprings;
            matchingThreadSprings = inRangeSprings.filterByThread(currentThread_);

            availableSprings_.Clear();

            availableSprings_.AddRange(matchingThreadSprings.ToArray());
        }


        private void showAvailableSprings()
        {
            NoSpringsText.Text = availableSprings_.Count().ToString();

            SpringBox.Items.Clear();

            SpringBox.Items.AddRange(availableSprings_.getNames().ToArray());

            int i = availableSprings_.getIndexByPartNumber(currentSpring_.partNumber);
            if (i >= 0  && i < availableSprings_.Count)
            {
                SpringBox.SelectedIndex = i;
            }

        }

        private SpringList filterSpringsInRange(double a0, double a1, SpringList testSprings)
        {

            requiredSpringLengths_ = myHatch_.requiredSpringLengths(a0, a1);

            double minDist = requiredSpringLengths_.Item1
                           - currentEndFittings_.sumLengths();

            double maxDist = requiredSpringLengths_.Item2
                           - currentEndFittings_.sumLengths();

            return testSprings.filterInRange(minDist, maxDist);
        }

        private void updateInfoBoxes()
        {
            double minStroke = requiredSpringLengths_.Item2 - requiredSpringLengths_.Item1;
            minExtLenTextBox.Text = Math.Round(requiredSpringLengths_.Item2).ToString();
            minStrokeTextBox.Text = Math.Round(minStroke).ToString();

            selectedTypeTextBox.Text = myHatch_.spring.typeName;
            selectedLengthTextBox.Text = myHatch_.spring.maxLength.ToString();
            lengthWithEndsTextBox.Text = myHatch_.spring.maxMountedLength.ToString();
            selectedStrokeTextBox.Text = myHatch_.spring.stroke.ToString();
            selectedForceTextBox.Text = myHatch_.spring.stiffness.ToString();
            selectedPartNoTextBox.Text = myHatch_.spring.partNumber;
            selectedFrictionTextBox.Text = myHatch_.spring.friction.ToString();

            endFittings1Label.Text = myHatch_.spring.endFittings[0].name;
            endFittings2Label.Text = myHatch_.spring.endFittings[1].name;

            // Special treatment for different self opening conditions
            if (myHatch_.equilibriumAngle > 1000)
            {
                selfOpeningAngleLabel.ForeColor = Color.Gray;
                selfOpeningAngleTextBox.Text = "No equilibrium";
            }
            else
            {
                if (myHatch_.staysClosed)
                {
                    selfOpeningAngleLabel.ForeColor = Color.Black;
                    selfOpeningAngleTextBox.Text = Math.Round(myHatch_.selfOpeningDeg).ToString();
                }
                else
                {
                    selfOpeningAngleLabel.ForeColor = Color.Gray;
                    selfOpeningAngleTextBox.Text = "Lid ajar at " + Math.Round(myHatch_.selfOpeningDeg).ToString();
                }
            }

            maxOpeningAngleTextBox.Text = Math.Round(getOpeningDeg(rad(myHatch_.maxSpringDeg))).ToString();
            overshootTextBox.Text = Math.Round(getOpeningDeg(rad(myHatch_.maxSpringDeg))-(double)openingAngleInput.Value).ToString();

        }

        private void setDefaultValues()
        {
            lidLengthInput.Value = 100; // 1000;
            cogInput.Value = (decimal) 0.0;// lidLengthInput.Value / 2;
            weightInput.Value = (decimal) 0.1; // 10;
            startAngleInput.Value = 0; // -90;
            openingAngleInput.Value = 0; // 90;
            springOriginXInput.Value = 0; // -50;
            springOriginYInput.Value = 0; // -50;
            lidConnectPosInput.Value = 0; // 300;
            lidOffsetInput.Value = 0; // 50;
            nbrOfSpringsInput.Value = 2;

            temperatureInput.Value = 20;

            threadRadioAll.Checked = true;

            customerNameTextBox.Text = "";
            customerCompanyTextBox.Text = "";
            customerMailTextBox.Text = "";
            customerProjectTextBox.Text = "";
        }

        private void applyFormValues()
        {
            myHatch_.lid.length = (double)lidLengthInput.Value;
            myHatch_.lid.relCog = getRelCog(); // Input %.
            myHatch_.lid.mass = (double)weightInput.Value;

            myHatch_.spring.origin.X = getSpringOriginX();
            myHatch_.spring.origin.Y = getSpringOriginY();

            myHatch_.lid.relConnection = (double)lidConnectPosInput.Value/myHatch_.lid.length;
            myHatch_.lid.connectionOffset = (double)lidOffsetInput.Value;
            myHatch_.setAngle(getStartAngle());

            myHatch_.temperature = (double)temperatureInput.Value;

            myHatch_.nSprings = (int)nbrOfSpringsInput.Value;

            myHatch_.startAngle = getStartAngle();
            myHatch_.stopAngle = getStopAngle();
        }

        /*
         * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  
         * Menu bar events
         * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
         */
        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if ( ! saveFormData(saveStateFileName_) )
            {
                notify("Failed to auto save session.");
            }
            if ( ! saveDesignerData(saveDesignerFileName_) )
            {
                notify("Failed to auto save designer info.");
            }
            Application.Exit();
        }

        /*
         * Below some save and open functions. Should write classes, but no time
         *
         * Hence: This is really in need of refactoring.
         */

        private void initializeSessionFiles()
        {
            tempPath_ = Path.Combine(Path.GetTempPath(), "LGP2");
            if (!System.IO.Directory.Exists(tempPath_))
            {
                try
                {
                    System.IO.Directory.CreateDirectory(tempPath_);
                }
                catch (IOException err)
                {
                    string errorString = "Warning:\n\tCould not setup session file.";
                    errorString += "\n\tthis session will not be restorable after exit.";
                    errorString += "\n\tMake sure to save propery.";
                    notify(errorString);
                }
            }
            saveStateFileName_ = Path.Combine(tempPath_, "lastSession.gsp");
            saveDesignerFileName_ = Path.Combine(tempPath_, "lastSessionDesigner.gsp");
        }


        private bool saveFormData(string fileName)
        {
            const string lineFormat = "{0} = {1};";
            try
            {
                System.IO.StreamWriter sw = new System.IO.StreamWriter(fileName);
               
                // Customer and designer data
                sw.WriteLine(string.Format(lineFormat, customerCompanyTextBox.Name, customerCompanyTextBox.Text));
                sw.WriteLine(string.Format(lineFormat, customerNameTextBox.Name, customerNameTextBox.Text));
                sw.WriteLine(string.Format(lineFormat, customerProjectTextBox.Name, customerProjectTextBox.Text));
                sw.WriteLine(string.Format(lineFormat, customerMailTextBox.Name, customerMailTextBox.Text));
               
                sw.WriteLine(string.Format(lineFormat, designerNameTextBox.Name, designerNameTextBox.Text));
                sw.WriteLine(string.Format(lineFormat, designerTelTextBox.Name, designerTelTextBox.Text));
                sw.WriteLine(string.Format(lineFormat, designerMailTextBox.Name, designerMailTextBox.Text));

                // Hatch data
                sw.WriteLine(string.Format(lineFormat, lidLengthInput.Name, ((int)lidLengthInput.Value).ToString()));
                sw.WriteLine(string.Format(lineFormat, cogInput.Name,       ((int)cogInput.Value).ToString()));
                sw.WriteLine(string.Format(lineFormat, weightInput.Name,    ((int)weightInput.Value).ToString()));
               
                sw.WriteLine(string.Format(lineFormat, startAngleInput.Name,    ((int)startAngleInput.Value).ToString()));
                sw.WriteLine(string.Format(lineFormat, openingAngleInput.Name,    ((int)openingAngleInput.Value).ToString()));
               
                sw.WriteLine(string.Format(lineFormat, lidConnectPosInput.Name,    ((int)lidConnectPosInput.Value).ToString()));
                sw.WriteLine(string.Format(lineFormat, lidOffsetInput.Name,    ((int)lidOffsetInput.Value).ToString()));

                sw.WriteLine(string.Format(lineFormat, springOriginXInput.Name, ((int)springOriginXInput.Value).ToString()));
                sw.WriteLine(string.Format(lineFormat, springOriginYInput.Name, ((int)springOriginYInput.Value).ToString()));
               
                sw.WriteLine(string.Format(lineFormat, nbrOfSpringsInput.Name,    ((int)nbrOfSpringsInput.Value).ToString()));

                sw.WriteLine(string.Format(lineFormat, temperatureInput.Name,    ((int)temperatureInput.Value).ToString()));
               
                // Spring
                string springPartNumber = currentSpring_.partNumber;
                sw.WriteLine(string.Format(lineFormat, "springPartNumber", springPartNumber));
               
                // EndFittings
                string endFittingPartNumber = currentEndFittings_[0].partNumber;
                sw.WriteLine(string.Format(lineFormat, "endFittingPartNumber0", endFittingPartNumber));
                endFittingPartNumber = currentEndFittings_[1].partNumber;
                sw.WriteLine(string.Format(lineFormat, "endFittingPartNumber1", endFittingPartNumber));

                // Options for data
                foreach (TextBox box in optionsForm_.customTextBoxes)
                {
                    sw.WriteLine(string.Format(lineFormat, box.Name, box.Text));
                }

                sw.Close();
                return true;
            }
            catch(IOException err)
            {
                notify(err.ToString());
                return false;
            }
        }

        private string lookup(string key, string[] lines)
        {
            // Simple function to read data from saved session file.
            // Assumes indata line-wise on the form key = value;
            foreach (string line in lines)
            {
                string[] pair = line.Split(new char[] {'=',';'});

                // If there are = or ; in the input forms, just
                // grab the first two items in the list...
                if (pair.Length >= 3)
                {
                    if (key == pair[0].Trim())
                    {
                        return pair[1].Trim();
                    }
                }
            }
            return "00";
        }

        private bool saveDesignerData(string fileName)
        {
            const string lineFormat = "{0} = {1};";
            try
            {
                System.IO.StreamWriter sw = new System.IO.StreamWriter(fileName);

                // Customer and designer data
                sw.WriteLine(string.Format(lineFormat, designerNameTextBox.Name, designerNameTextBox.Text));
                sw.WriteLine(string.Format(lineFormat, designerTelTextBox.Name, designerTelTextBox.Text));
                sw.WriteLine(string.Format(lineFormat, designerMailTextBox.Name, designerMailTextBox.Text));

                // Options form data
                foreach (TextBox box in optionsForm_.pageFooterTextBoxes)
                {
                    sw.WriteLine(string.Format(lineFormat, box.Name, box.Text));
                }
                sw.Close();
            }
            catch (IOException err)
            {
                notify(err.ToString());
                return false;
            }
            return true;
        }
 
        private bool openDesignerData(string fileName)
        {
            if (!File.Exists(fileName))
            {
                warning("Did not find saved designer info file.");
                return false;
            }
           string readErrors = "File Open Errors:";
           try
           {
               char[] lineSplit = new char[] { '\r', '\n' };
               System.IO.StreamReader sr = new System.IO.StreamReader(fileName);
               string fileData = sr.ReadToEnd();
               sr.Close();
               string[] lines = fileData.Split(lineSplit, StringSplitOptions.RemoveEmptyEntries);

               designerNameTextBox.Text = lookup(designerNameTextBox.Name, lines);
               designerTelTextBox.Text = lookup(designerTelTextBox.Name, lines);
               designerMailTextBox.Text = lookup(designerMailTextBox.Name, lines);

                // Options form data

               foreach (TextBox box in optionsForm_.pageFooterTextBoxes)
               {
                   string txt = lookup(box.Name, lines);
                   if (txt != "00") box.Text = txt;
               }
           }
           catch
           {
               readErrors += "\nFailed reading designer info. file.";
               readErrors += "\nThis is probably OK";
               readErrors += "\nJust fill in the gaps and it should be rewritten.";
           }

           if (readErrors.Length > 20)
           {
               notify("Errors:\n"+readErrors);
               return false;
           }
           return true;
        }

        private bool openFormData(string fileName)
        {
           string readErrors = "File Open Errors:\n";
           try
           {
               char[] lineSplit = new char[] { '\r', '\n' };
               System.IO.StreamReader sr = new System.IO.StreamReader(fileName);
               string fileData = sr.ReadToEnd();
               sr.Close();
               string[] lines = fileData.Split(lineSplit, StringSplitOptions.RemoveEmptyEntries);

               customerCompanyTextBox.Text = lookup(customerCompanyTextBox.Name, lines);
               customerNameTextBox.Text = lookup(customerNameTextBox.Name, lines);
               customerProjectTextBox.Text = lookup(customerProjectTextBox.Name, lines);
               customerMailTextBox.Text = lookup(customerMailTextBox.Name, lines);

               lidLengthInput.Value = decimal.Parse(lookup(lidLengthInput.Name,lines));
               cogInput.Value = decimal.Parse(lookup(cogInput.Name,lines));
               weightInput.Value = decimal.Parse(lookup(weightInput.Name,lines));

               startAngleInput.Value = decimal.Parse(lookup(startAngleInput.Name,lines));
               openingAngleInput.Value = decimal.Parse(lookup(openingAngleInput.Name,lines));

               lidConnectPosInput.Value = decimal.Parse(lookup(lidConnectPosInput.Name,lines));
               lidOffsetInput.Value = decimal.Parse(lookup(lidOffsetInput.Name,lines));

               springOriginXInput.Value = decimal.Parse(lookup(springOriginXInput.Name,lines));
               springOriginYInput.Value = decimal.Parse(lookup(springOriginYInput.Name,lines));

               nbrOfSpringsInput.Value = int.Parse(lookup(nbrOfSpringsInput.Name,lines));

               temperatureInput.Value = int.Parse(lookup(temperatureInput.Name,lines));

               // Spring
               string springPartNumber = lookup("springPartNumber", lines);
               currentSpring_ = springReader_.springs.getByPartNo(springPartNumber);
               if (currentSpring_ == null)
               {
                   readErrors += "\nCould not find saved spring, setting default";
                   currentSpring_ = availableSprings_[0];
               }
               else
               {
                   try
                   {
                       int springIndex = springReader_.springs.IndexOf(currentSpring_);
                       SpringBox.SetSelected(springIndex, true);
                   }
                   catch { }
               }

               // EndFitting
               string endFittingPartNumber = lookup("endFittingPartNumber0", lines);
               EndFitting e0 = endFittingReader_.endFittings.getByPartNo(endFittingPartNumber);
               if (e0 == null)
               {
                   readErrors += "\nCould not find saved end fitting, setting default.";
                   e0 = new EndFitting();
               }

               currentEndFittings_[0] = e0;
               int e0Index = endFittingReader_.endFittings.IndexOf(e0);
               endFittingRodBox.Select(e0Index,1);

               endFittingPartNumber = lookup("endFittingPartNumber1", lines);
               EndFitting e1 = endFittingReader_.endFittings.getByPartNo(endFittingPartNumber);
               if (e1 == null)
               {
                   toolStripMenuItem1.Text = "\nCould not find saved end fitting, setting default.";
                   e1 = new EndFitting();
               }
               currentEndFittings_[1] = e1;
               //int e1Index = endFittingReader_.endFittings.IndexOf(e1);
               //endFittingRodBox.Select(e1Index, 1);

               // Options form data

               foreach (TextBox box in optionsForm_.customTextBoxes)
               {
                   string txt = lookup(box.Name, lines);
                   if (txt != "00") box.Text = txt;
               }
               updateHatch();

           }
           catch
           {
               readErrors += "\n\nFailed reading file.\nTotally.";
           }

           if (readErrors.Length > 20)
           {
               notify("Errors:\n"+readErrors);
               return false;
           }
           return true;
        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.FileName = customerProjectTextBox.Text;
            saveFileDialog.Filter = "gsp files (*.gsp)|*.gsp";
            saveFileDialog.RestoreDirectory = true;

            if (saveFileDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK
                && saveFileDialog.FileName.Length > 0)
            {
                saveFormData(saveFileDialog.FileName);
            }
        }

        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "gsp files (*.gsp)|*.gsp";
            openFileDialog.FilterIndex = 2;
            openFileDialog.RestoreDirectory = true;
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                openFormData(openFileDialog.FileName);
            }
        }

        private void restoreLastToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (!File.Exists(saveStateFileName_))
            {
                warning("Did not find auto saved state file.");
                return;
            }

            openFormData(saveStateFileName_);
        }

        private void printToolStripMenuItem_Click(object sender, EventArgs e)
        {
            PdfManager pdf = new PdfManager(this);

            bool success = pdf.makePDF("springDesign.pdf");
        }

        private void optionsMenuItem_Click(object sender, EventArgs e)
        {
            optionsForm_.ShowDialog();
        }


        // Simple functions to handle transfer of form input values to
        // useable data. (Input required is e.g. opening angle, but calculations
        // needs actual angle in coord. sys. Further, input values should
        // reflect bitmap coordinate system, whereas calculations are performed
        // in standard coordinates (positive y upwards).

        private double getStartAngle()
        {
            return  -1 * rad((double)startAngleInput.Value);
        }

        private double getStopAngle()
        {
            // Form input is start angle and opening angle
            double oa = rad((double)openingAngleInput.Value);
            return getStartAngle() - oa;
        }

        private double getRelCog()
        {
            return (double)(cogInput.Value / lidLengthInput.Value);
        }

        private double getOpeningDeg()
        {
            return getOpeningDeg(myHatch_.lid.angle);
        }

        public double getOpeningDeg(double a0)
        {
            return deg(-a0 + getStartAngle());
        }

        public double getOpeningDeg2Deg(double a0)
        {
            return -a0 + deg(getStartAngle());
        }

        public double getSpringOriginX()
        {
            return (double)(1 * springOriginXInput.Value);
        }

        public double getSpringOriginY()
        {
            return (double)(-1*springOriginYInput.Value);
        }

        // Access to private data from e.g. PdfManager

        public Bitmap hatchBitmap
        {
            get { return hatchBitmap_; }
        }

        public string tempPath
        {
            get { return tempPath_; }
        }

        //      Easy access to all input boxes through a list of the same.
        public Hashtable formInputData
        {
            get
            {
                Hashtable  boxes = new Hashtable();
                
                boxes.Add(customerCompanyTextBox.Name, customerCompanyTextBox);
                boxes.Add(customerNameTextBox.Name, customerNameTextBox);
                boxes.Add(customerProjectTextBox.Name, customerProjectTextBox);
                boxes.Add(customerMailTextBox.Name, customerMailTextBox);

                boxes.Add(lidLengthInput.Name, lidLengthInput);
                boxes.Add(cogInput.Name, cogInput);
                boxes.Add(weightInput.Name, weightInput);

                boxes.Add(startAngleInput.Name, startAngleInput);
                boxes.Add(openingAngleInput.Name, openingAngleInput);

                boxes.Add(lidConnectPosInput.Name, lidConnectPosInput);
                boxes.Add(lidOffsetInput.Name, lidOffsetInput);

                boxes.Add(springOriginXInput.Name, springOriginXInput);
                boxes.Add(springOriginYInput.Name, springOriginYInput);

                boxes.Add(nbrOfSpringsInput.Name, nbrOfSpringsInput);

                boxes.Add(temperatureInput.Name, temperatureInput);

                return boxes;
            }
        }

        internal Hatch currentHatch
        {
            get { return myHatch_; }
        }

        internal OptionsForm optionsForm
        {
            get { return optionsForm_; }
        }

        internal Image chartImage
        {
            get
            {
                MemoryStream imgStr = new MemoryStream();
                chart1.SaveImage(imgStr, ChartImageFormat.Png);
                Image img = Image.FromStream(imgStr);
                return img;
            }
        }
    }
}
