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
using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using NExcel;

namespace HatchTest
{
    internal class ExcelReader
    {
        private string fileName_;
        private Workbook wb_;
        protected Hashtable columnDefs_ = new Hashtable();
        protected string sheetNamePattern_ = ".*";
        protected string typePattern_ = ".*";
        
        public ExcelReader(string fn)
        {
            try
            {
                fileName_ = fn;
                wb_ = Workbook.getWorkbook(fn);
            }
            catch (System.IO.IOException err)
            {
                FATALERROR("Failed to read database.","Exiting!");
            }
        }

        public Workbook wb()
        {
            return wb_;
        }

        public string fileName()
        {
            return fileName_;
        }

        public void close()
        {
            wb_.close();
        }

        public int findSheet()
        {
            int sheetNo = 0;
            foreach (Sheet s in wb().Sheets)
            {
                if (Regex.IsMatch(s.Name, sheetNamePattern_, RegexOptions.IgnoreCase))
                {
                    return sheetNo;
                }
                sheetNo++;
            }

            FATALERROR("findSheet", "No sheet found in database, matching " + sheetNamePattern_);
            return sheetNo;
        }

        protected string getString(Cell[] row, string colDef)
        {
            string value = "";
            try
            {
                int i = (int)columnDefs_[colDef];
                value = row[i].Value.ToString();
            }
            catch(System.IO.IOException err)
            {
                ERROR("getString", "Failed to read value from database: " + colDef);
            }
            return value;
        }

        protected double getDouble(Cell[] row, string colDef)
        {
            double value = 0;
            try
            {
                int i = (int)columnDefs_[colDef];
                value = (double)row[i].Value;
            }
            catch(System.IO.IOException err)
            {
                ERROR("getString", "Failed to read value from database: " + colDef);
            }
            return value;
        }

        protected int getInt(Cell[] row, string colDef)
        {
            int value = 0;
            try
            {
                int i = (int)columnDefs_[colDef];
                value = (int)row[i].Value;
            }
            catch(System.IO.IOException err)
            {
                ERROR("getString", "Failed to read value from database: " + colDef);
            }
            return value;
        }

        public void ERROR(string s0, string s1)
        {
            System.Windows.Forms.MessageBox.Show(String.Format("In ExcelReader::{0}\n{1}\nFailed file: {2}",s0,s1,fileName_));
        }

        public void FATALERROR(string s0, string s1)
        {
            ERROR(s0,s1);
            Environment.Exit(2);
        }
    }

    internal class SpringReader:ExcelReader
    {
        /*
         * An ExcelReader that 1) parses the xls document for
         * sheets named [digit][digit]-[something], like 18-8W.
         * 2) For each sheet, then defining the springs of the
         * actual type (18-8W), gathers spring data from each row
         * starting with a cell containing the spring type string
         * (18-8W)
         */
        protected List<string> springTypes_;
        private SpringList springs_;

        public SpringReader(string fileName)
               : base(fileName)
        {
            typePattern_ = "\\d{2}-.*";

            springTypes_ = new List<string>();
            columnDefs_.Add("type", 0);
            columnDefs_.Add("length", 1);
            columnDefs_.Add("stroke", 2);
            columnDefs_.Add("stiffness", 3);
            columnDefs_.Add("product", 4);
            columnDefs_.Add("thread", 5);
            springs_ = new SpringList();

            readAllAndClose();
        }

        public void getTypes()
        {
            foreach (Sheet s in wb().Sheets)
            {
                if (Regex.IsMatch(s.Name,typePattern_,RegexOptions.IgnoreCase))
                {
                    springTypes_.Add(s.Name);
                }
            }
            if (springTypes_.Count == 0)
            {
                ERROR("getTypes","No spring type sheets found matching "+typePattern_);
            }
        }

        public void readAllAndClose()
        {
            getTypes();
            foreach (string type in springTypes_)
            {
                Sheet sheet = wb().getSheet(type);
                for (int rowi = 0; rowi < sheet.Rows; rowi++)
                {
                    if (sheet.getCell(0, rowi).Value.ToString() == type)
                    {
                        Cell[] row = sheet.getRow(rowi);

                        double length = getDouble(row, "length");
                        double stroke = getDouble(row, "stroke");
                        double stiffness = getDouble(row, "stiffness");
                        string partNo = getString(row, "product");
                        string thread = getString(row, "thread");

                        string name = String.Format("{0} {1}-{2}-{3} {4} ({5})",
                            type, length, stroke, stiffness, partNo, thread);

                        Object2D ob = new Object2D(length,0,0.5,new Vector2D());

                        MechanicalObject mob = new MechanicalObject(ob);

                        Spring spring = new Spring(mob,stroke,stiffness);

                        spring.typeName = type;
                        spring.partNumber = partNo;
                        spring.thread = thread;
                        spring.name = name;

                        springs_.Add(spring);
                    }
                }
            }

            this.close();
        }

        public SpringList springs
        {
            get{ return springs_; }
        }
    }

    internal class EndFittingReader:ExcelReader
    {
        /* ExcelReader that finds the sheet name matching
         * "end.*fittings". Then parses each line with first
         * cell matching "end.*".
         */
        
        new private readonly string typePattern_ = "end.*";
        protected List<string> springTypes_;
        private EndFittingList endFittings_;

        public EndFittingReader(string fileName)
               : base(fileName)
        {
            sheetNamePattern_ = "end.*fittings.*";
            springTypes_ = new List<string>();
            columnDefs_.Add("type", 1);
            columnDefs_.Add("product", 3);
            columnDefs_.Add("thread", 4);
            columnDefs_.Add("length", 5);
            columnDefs_.Add("boltDiam", 6);
            endFittings_ = new EndFittingList();

            readAllAndClose();
        }

        public void readAllAndClose()
        {
            endFittings_.Clear();
            endFittings.Add(new EndFitting()); // Add one default (welded)
            Sheet sheet = wb().getSheet(findSheet());
            for (int rowi = 0; rowi < sheet.Rows; rowi++)
            {
                string rowName = sheet.getCell(0, rowi).Value.ToString();

                if (Regex.IsMatch(rowName, typePattern_,RegexOptions.IgnoreCase))
                {
                    Cell[] row = sheet.getRow(rowi);

                    double length = getDouble(row, "length");
                    string type = getString(row, "type");
                    string partNo = getString(row, "product");
                    string thread = getString(row, "thread");

                    EndFitting end = new EndFitting(type,length,thread,partNo);

                    endFittings_.Add(end);
                }
            }

            this.close();
        }

        public EndFittingList endFittings
        {
            get { return endFittings_; }
        }
    }

    public struct Corrections
    {
        public double friction;
        public double tempCorrection;

        public Corrections(double f, double t)
        {
            friction = f;
            tempCorrection = t;
        }
    }
    internal class CorrectionsReader : ExcelReader
    {
        private Dictionary<string, Corrections> correctionsDict_;

        public CorrectionsReader(string fileName)
            : base(fileName)
        {
            sheetNamePattern_ = "corrections.*";
            typePattern_ = "correction.*";

            columnDefs_.Add("type", 1);
            columnDefs_.Add("friction", 2);
            columnDefs_.Add("temperature", 3);

            correctionsDict_ = new Dictionary<string, Corrections>();

            readAllAndClose();
        }

        public void  readAllAndClose()
        {
            correctionsDict_.Clear();
            Sheet sheet = wb().getSheet(findSheet());
            correctionsDict_.Add("Zero", new Corrections(0,0));

            for (int rowi = 0; rowi < sheet.Rows; rowi++)
            {
                string rowName = sheet.getCell(0, rowi).Value.ToString();

                if (Regex.IsMatch(rowName, typePattern_, RegexOptions.IgnoreCase))
                {
                    Cell[] row = sheet.getRow(rowi);

                    string type = getString(row, "type");
                    double friction = getDouble(row, "friction");
                    double tempCoeff = getDouble(row, "temperature");

                    correctionsDict_.Add(type, new Corrections(friction,tempCoeff));
                }
            }

            this.close();
        }

        public Dictionary<string,Corrections> dict
        {
            get { return correctionsDict_; }
        }

        public Corrections getCorrections(string type)
        {
            // Fetch the friction for a spring type
            // matching a key in friction dictionary.
            string matchKey = "NoMatch";
            foreach (string key in correctionsDict_.Keys)
            {
                if (Regex.IsMatch(type, key+".*", RegexOptions.IgnoreCase))
                {
                    matchKey = key;
                    break;
                }
            }

            if (correctionsDict_.ContainsKey(matchKey))
            {
                return correctionsDict_[matchKey];
            }
            else
            {
                string message =
                    String.Format("Missing key in corrections dictionary: {0}\nCorrections set to 0.0!", type);
                ERROR("getCorrections", message);
                return new Corrections(0,0);
            }
        }

        public double getFriction(string type)
        {
            Corrections corrs = getCorrections(type);
            return corrs.friction;
        }

        public double getTempCorrection(string type)
        {
            Corrections corrs = getCorrections(type);
            return corrs.tempCorrection;
        }
    }
}
