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
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace HatchTest
{
    /*
     * Need to refactor this into a templated internal class I
     * suppose
     */

    internal class SpringList : List<Spring>
    {
        public SpringList()
            : base()
        {
        }

        public void applyFriction(CorrectionsReader F)
        {
            foreach (Spring s in this)
            {
                s.friction = F.getFriction(s.typeName);
            }
        }

        public void applyCorrections(CorrectionsReader F)
        {
            // Probably bad way to do this, but friction
            // came in late in the project. Thus: Quick and dirty

            foreach (Spring s in this)
            {
                Corrections corrs = F.getCorrections(s.typeName);
                s.friction = corrs.friction;
                s.tempCorrection = corrs.tempCorrection;
            }
        }

        public SpringList filterInRange(double minLength, double maxLength)
        {
            // Filter using maxLength. End fittings must be taken care of in
            // minLength and maxLength arguments.

            SpringList filtered = new SpringList();

            foreach (Spring s in this)
            {
                if
                (
                    (s.maxLength >= maxLength)
                 && (s.minLength <= minLength)
                )
                {
                    filtered.Add(s);
                }
            }
            return filtered;
        }

        public SpringList filterByThread(String threadName)
        {
            SpringList filtered = new SpringList();

            foreach (Spring s in this)
            {
                if ( s.thread == threadName || threadName == "All")
                {
                    filtered.Add(s);
                }
            }

            return filtered;
        }

        public List<string> getNames()
        {
            List<string> stringNames = new List<string>(0);

            foreach (Spring s in this)
            {
                stringNames.Add(s.name);
            }
            return stringNames;
        }

        public Spring getByPartNo(string partNo)
        {
            foreach (Spring s in this)
            {
                if (s.partNumber == partNo)
                {
                    return s;
                }
            }
            return null;
        }

        public int getIndexByPartNumber(string partNo)
        {
            int index = -1;
            for (int i = 0; i < this.Count; i++)
            {
                if (this[i].partNumber == partNo)
                {
                    index = i;
                }
            }
            return index;
        }

        public SpringList M6
        {
            get { return this.filterByThread("M6"); }
        }

        public SpringList M8
        {
            get { return this.filterByThread("M8"); }
        }

        public SpringList Welded
        {
            get { return this.filterByThread("Welded"); }
        }
    }

/*
 *
 */

    internal class EndFittingList : List<EndFitting>
    {
         public EndFittingList()
            : base()
        {
        }
         public EndFittingList filter(String key, String expr)
         {
             EndFittingList filtered = new EndFittingList();

             foreach (EndFitting s in this)
             {
                 String value = typeof(Spring).GetMethod(key).Invoke(s, null).ToString();

                 if (Regex.IsMatch(value, expr, RegexOptions.IgnoreCase))
                 {
                     filtered.Add(s);
                 }
             }
             return filtered;
         }

         public EndFittingList(EndFitting e0, EndFitting e1)
             : base()
         {
             // Constuct list of capacity for 2 end fittings only.
             this.Capacity = 2;
             this.Add(e0);
             this.Add(e1);
         }

         public List<string> getNames()
         {
             List<string> stringNames = new List<string>(0);

             foreach (EndFitting s in this)
             {
                 stringNames.Add(s.name);
             }
             return stringNames;
         }

         public EndFittingList filterByThread(String threadName)
         {
             EndFittingList filtered = new EndFittingList();

             foreach (EndFitting e in this)
             {
                 if (e.thread == threadName || threadName == "All")
                 {
                     filtered.Add(e);
                 }
             }

             return filtered;
         }

        public EndFitting getByPartNo(string partNo)
        {
            foreach (EndFitting e in this)
            {
                if (e.partNumber == partNo)
                {
                    return e;
                }
            }
            return null;
        }

        public int getIndexByPartNumber(string partNo)
        {
            int index = -1;
            for (int i = 0; i < this.Count; i++)
            {
                if (this[i].partNumber == partNo)
                {
                    index = i;
                }
            }
            return index;
        }

        public double sumLengths()
        {
           double sum = 0;
           foreach (EndFitting e in this)
           {
               sum += e.length;
           }
           return sum;
        }

    }

    internal class HandForces
    {
        public List<double> deg_;
        public List<double> open_;
        public List<double> close_;

        public HandForces()
        {
            deg_ = new List<double>();
            open_ = new List<double>();
            close_ = new List<double>();
        }

        public HandForces(List<double> deg, List<double> open, List<double> close)
        {
            deg_ = new List<double>();
            open_ = new List<double>();
            close_ = new List<double>();

            deg_.AddRange(deg);
            open_.AddRange(open);
            close_.AddRange(close);
        }

        public HandForces(HandForces hf)
        {
            deg_ = new List<double>();
            open_ = new List<double>();
            close_ = new List<double>();

            deg_.AddRange(hf.deg);
            open_.AddRange(hf.open);
            close_.AddRange(hf.close);
        }

        public void clear()
        {
            deg_.Clear();
            open_.Clear();
            close_.Clear();
        }

        public List<double> deg
        {
            get { return deg_; }
            set
            {
                deg_.Clear();
                deg_.AddRange(value);
            }            
        }

        public List<double> open
        {
            get { return open_; }
            set
            {
                open_.Clear();
                open_.AddRange(value);
            }
        }

        public List<double> close
        {
            get { return close_; }
            set
            {
                close_.Clear();
                close_.AddRange(value);
            }
        }
    }
}
