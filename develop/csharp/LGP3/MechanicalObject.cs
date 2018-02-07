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
using System.Drawing;

namespace HatchTest
{

    internal class MechanicalObject : Object2D
    {
        protected string name_;
        protected string typeName_;
        protected string partNumber_;
        protected string thread_;

        public MechanicalObject(Object2D ob)
            : base(ob.length, ob.mass, ob.relCog, ob.origin)
        {
            name_ = "";
            partNumber_ = "";
            thread_ = "";
            typeName_ = "";
        }

        public MechanicalObject(MechanicalObject M)
            : base(M)
        {
            name_ = M.name;
            partNumber_ = M.partNumber;
            thread_ = M.thread;
            typeName_ = M.typeName;
        }

        public string name
        {
           get{ return name_;}
           set{ name_ = value;}
        }
        public string partNumber
        {
            get{ return partNumber_; }
            set{ partNumber_ = value; }
        }
        public string thread
        {
            get { return thread_; }
            set { thread_ = value; }
        }
        public string typeName
        {
            get {return typeName_;}
            set { typeName_ = value;}
        }
    }

}
