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
using System.Text;
using System.ComponentModel;
using System.Collections.Generic;

namespace HatchTest
{

    internal class EndFitting
    {
        /* 
         * Very simple object, containing end fitting info.
         * Should inherit from mechanicalObject, like.
         */

        private readonly double length_;
        private readonly string type_;
        private readonly string name_;
        private string thread_;
        private readonly string partNumber_;
        public readonly List<string> availableThreads_ = new List<string>()
        {
            "Welded",
            "M6",
            "M8"
        };

        public EndFitting(string type, double length, string thread, string partNo)
        {
            length_ = length;
            type_ = type;
            thread_ = thread;
            partNumber_ = partNo;
            name_ = String.Format("{0} {1} ({3,0:f}mm, {2})", type_, partNumber_, thread_, length_);
        }

        public EndFitting()
        {
            length_ = 0.0;
            type_ = "Welded";
            thread_ = "Welded";
            partNumber_ = "0";
            name_ = "Welded";
        }

        public double length
        {
            get { return length_; }
        }

        public string name
        {
            get { return name_; }
        }

        public string type
        {
            get { return type_; }
        }

        public string thread
        {
            get { return thread_; }
            set
            {
                if (availableThreads_.Contains(value))
                {
                    thread_ = value;
                }
            }
        }
        public string partNumber
        {
            get { return partNumber_; }
        }

        public void printAllProperties()
        {
            foreach(PropertyDescriptor descriptor in TypeDescriptor.GetProperties(this))
            {
                string name=descriptor.Name;
                object value=descriptor.GetValue(this);
                // HIDE Console.WriteLine("{0}={1}",name,value);
            }
        }
    }
}
