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

    internal class Lid : MechanicalObject
    {
        private double relConnection_;
        private double connectionOffset_;

        public Lid(MechanicalObject ob, double relConn, double conOffset)
            : base(ob)
        {
            relConnection_ = relConn;
            connectionOffset_ = conOffset;
            pen_.Color = Color.Black;
            pen_.Width = 3;
        }

        public Lid(Lid L)
            : base(L)
        {
            // Copy constructor
            relConnection_ = L.relConnection;
            connectionOffset_ = L.connectionOffset;
            pen_.Color = Color.Black;
            pen_.Width = 3;
        }

        public string info()
        {
            string s = "-LID INFO-------------------------------\n";
            s +=       "Lid name   = " + this.name + "\n";
            s +=       "\tLid angle = " + this.angle*180/Math.PI+"\n";
            s +=       "\tLid origin = (" + this.origin.X
                                       +", "+ this.origin.Y+")\n";
            s +=       "\tLid end    = (" + this.end().X
                                     +", "+ this.end().Y+")\n";
            s +=       "\tLid conn pt= (" + this.connectionObject().end().X
                                     +", "+ this.connectionObject().end().Y+")\n";
            return s;
        }


        public Vector2D connection()
        {
            return position(relConnection_);
        }

        public Object2D connectionObject()
        {
            Object2D conn = new Object2D(connectionOffset_, 0, 0.5, position(relConnection_));
            conn.visualScaleFactor = this.visualScaleFactor;
            conn.rotate(this.vector.orthogonal().angle());   
            return conn;
        }

        public void drawConnection(Bitmap bitmap)
        {
            int penWidth = (int) Math.Max(1, pen_.Width - 1);
            Pen pen = new Pen(Color.DarkGray, penWidth);
            connectionObject().draw(bitmap, pen);
        }

        // Access
        public double relConnection
        {
            get { return relConnection_; }
            set { relConnection_ = value; }
        }
        public double connectionOffset
        {
            get { return connectionOffset_; }
            set { connectionOffset_ = value; }
        }

    }
}
