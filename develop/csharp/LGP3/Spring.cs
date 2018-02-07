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
using System.Diagnostics;

namespace HatchTest
{
    internal class Spring : MechanicalObject
    {
        /*
         * Note: For gas springs stiffness_ is the defined, constant,
         * spring force.
         *
         * A Springs maxLength is never changed. The current length
         * is get from Object2D.length
         *
         */
        private readonly double stroke_;
        private readonly double maxLength_;
        private readonly double stiffness_;

        static readonly double refTemp_ = 20;
        private double tempCorrection_ = 0.0035;
        static readonly double progressivness_ = 0.0;

        private double dL_ = 0.0;
        private double friction_ = 0.0;

        private Color colorOk_ = Color.ForestGreen;
        private Color colorErr_ = Color.Red;
        private EndFittingList endFittings_
            = new EndFittingList(new EndFitting(), new EndFitting());

        public Spring(MechanicalObject ob, double stroke, double stiffness)
            : base(ob)
        {
            stroke_ = stroke;
            maxLength_ = ob.length;
            stiffness_ = stiffness;
            pen_.Color = colorOk_;
            pen_.Width = 3;
        }

        public Spring(MechanicalObject ob, string stroke, string stiffness)
            : base(ob)
        {
            stroke_ = Double.Parse(stroke);
            maxLength_ = ob.length;
            stiffness_ = Double.Parse(stiffness);
            pen_.Color = colorOk_;
            pen_.Width = 3;
        }

        public Spring(Spring S)
            : base(S)
        {
            // Copy constructor
            stroke_ = S.stroke;
            maxLength_ = S.maxLength;
            stiffness_ = S.stiffness;
            pen_.Color = colorOk_;
            pen_.Width = 3;
            endFittings_ = S.endFittings;
        }


        public void changeEndFittings(EndFittingList ends )
        {
            endFittings_ = ends;
        }

        public bool compress(double distance)
        {
            // Note: distance is how much shorter than maxMountedLength
            // the spring needs to be. The object length is the
            // Object2D property, that for a Spring is the current
            // length, which has nothing to do with endfittings.

            bool inRange = (distance >= 0) && (distance <= stroke_);

            double targetSpringLength = maxLength_ - distance;

            double newLength = Math.Min
                            (
                                maxLength_,
                                Math.Max(targetSpringLength, this.minLength)
                            );

            // Store this motion's change in length for
            // use in friction force calculation.
            // Compression is negative dL_ (delta length)
            dL_ = newLength - this.length;

            this.length = newLength;

            if (inRange)
            {
                pen_.Color = colorOk_;
            }
            else
            {
                pen_.Color = colorErr_;
            }

            return inRange;
        }

        public Vector2D force()
        {
            return (maxLength_-this.length)*stiffness_
                * new UnitVector2D(this.vector.angle());
        }

        public Vector2D force(double temperature)
        {
            double deltaT = temperature-refTemp_;

            double tempCorrection = 1 + tempCorrection_ * deltaT;

            // Progressive spring force acc. to thesis, eqn 26
            double ratio = (this.length - this.minLength) / stroke_;

            double f = stiffness_ * (1 + progressivness_*(1 - ratio));

            f *= tempCorrection;

            // Wait with adding the friction force. This is handled
            // by the Hatch functions, since need to know the open
            // or close sequence.

            return f * new UnitVector2D(this.vector.angle());
        }

        new public Vector2D end()
        {
            return this.origin + this.currentMountedLength * this.vector.norm();
        }

        // Access
        public double stiffness
        {
            get { return stiffness_; }
        }

        public double stroke
        {
            get { return stroke_; }
        }

        public double maxLength
        {
            get { return maxLength_; }
        }

        public EndFittingList endFittings
        {
            get { return endFittings_; }
        }

        public string endFittingType()
        {
            return this.endFittings[0].type;
        }

        public bool isWelded()
        {
            bool welded = false;
            if (this.endFittingType() == "Welded")
            {
                welded = true;
            }
            return welded;
        }

        public double endLengths
        {
            get { return endFittings_.sumLengths(); }
        }

        public double minLength
        {
           get { return maxLength_-stroke_; }
        }

        public double maxMountedLength
        {
            get { return maxLength_ + this.endLengths; }
        }

        public double minMountedLength
        {
            get { return this.maxMountedLength - stroke_; }
        }

        public double currentMountedLength
        {
            get { return this.length + this.endLengths; }
        }

        public double dL
        {
            get { return dL_; }
        }

        public double friction
        {
            get { return friction_; }
            set { friction_ = value; }
        }

        public double tempCorrection
        {
            get { return tempCorrection_; }
            set { tempCorrection_ = value; }
        }

        public bool inRange(double l)
        {
            return (l < this.maxMountedLength)
                && (l > this.minMountedLength);
        }

        public bool constrainToLid(Lid lid)
        {
            Vector2D required = lid.connectionObject().end() - this.origin;

            setAngle(required.angle());

            double compression = this.maxMountedLength - required.length();

            return compress(compression);
        }

        public void draw(Bitmap bitmap)
        {
            double pistonLength = stroke_+endFittings_[0].length;

            double cylinderLength = this.maxMountedLength - pistonLength;

            Object2D piston = new Object2D(this.currentMountedLength - cylinderLength, 0, 0, this.origin);
            piston.rotate(this.angle);

            Object2D cylinder = new Object2D(cylinderLength, 1, 1, piston.end());
            cylinder.rotate(this.angle);

            cylinder.visualScaleFactor = this.visualScaleFactor;
            piston.visualScaleFactor = this.visualScaleFactor;

            Pen pistonPen = new Pen(pen_.Color, 1);
            cylinder.draw(bitmap, pen_,0,5);
            piston.draw(bitmap, pistonPen,5,0);
        }

        public string info()
        {
            string s = "-SPRING INFO-------------------------------\n";
            s +=       "Spring name   = " + this.name + "\n";
            s +=       "\tSpring angle = " + this.angle*180/Math.PI+"\n";
            s +=       "\tSpring origin = (" + this.origin.X
                                       +", "+ this.origin.Y+")\n";
            s +=       "\tSpring end    = (" + this.end().X
                                       +", "+ this.end().Y+")\n";
            s +=       "\tSpring max len= " + this.maxLength+"\n";
            s +=       "\tSpring min len= " + (this.maxLength - this.stroke)+"\n";
            return s;
        }



    }

}
