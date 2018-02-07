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
    internal class Hatch
    {
        protected Lid lid_;
        protected Spring spring_;

        private int nSprings_ = 2;
        private double temperature_ = 20;
        private readonly double refTemperature_ = 20;

        private double startAngle_ = 0;
        private double stopAngle_ = 0;
        private bool staysClosed_ = false;
        private double equilibriumAngle_ = 0;

        private HandForces handForces_ = new HandForces();

        // Panic storage
        private double maxSpringDeg_ = 0;
        private double minSpringDeg_ = 0;

        public Hatch(Lid lid, Spring spring)
        {
            // Create new objects, to avoid meddling with
            // SpringList content.
            lid_ = new Lid(lid);
            spring_ = new Spring(spring);
            spring_.constrainToLid(lid_);
        }

        public Hatch(Hatch hatch)
        {
            // Copy constructor
            lid_ = hatch.lid;
            spring_ = hatch.spring;
            spring_.constrainToLid(lid_);
        }

        public string hatchInfo()
        {
            string s = spring.info();
            s +=       lid.info();

            spring.endFittings[0].printAllProperties();
            spring.endFittings[1].printAllProperties();

            return s;
        }

        public bool open(double angle)
        {
            lid_.rotate(angle);
            bool openOK = spring_.constrainToLid(lid_);
            return openOK;
        }

        public int springDirection(double dAlpha)
        {
            /*
             * Returns +1 or -1 depending on elongation/compression
             * of spring during a dAlpha rotation.
             * Yes, this is a bit ugly.
             */
            double l0 = (this.spring.origin
                      - this.lid.connectionObject().end()).length();

            this.open(dAlpha);

            double l1 = (this.spring.origin
                      - this.lid.connectionObject().end()).length();
            return Math.Sign(l1 - l0);
        }

        public bool setAngle(double alpha)
        {
            lid_.setAngle(alpha);
            return spring_.constrainToLid(lid_);
        }

        public double requiredSpringLength()
        {
            return (
                     this.spring.origin
                   - this.lid.connectionObject().end()
                   ).length();
        }

        // Return required (max) length and stroke for possibility to
        // open hatch from angle0 to angle1. Trial and error method...
        public Tuple<double,double> requiredSpringLengths(double angle0, double angle1)
        {
            double currentAngle = this.lid.angle;

            this.setAngle(angle0);

            Vector2D springOrigin = this.spring.origin;

            int nSteps = 100;

            double a0 = angle0; //*Math.PI/180;
            double a1 = angle1; //*Math.PI / 180;

            double delta = (a1-a0)/nSteps;

            double max = (
                             this.lid.connectionObject().end()
                           - this.spring.origin
                         ).length();
            double min =max;

            for (int i = 0; i < nSteps; i++)
            {
                this.open(delta);

                double l = (
                              this.lid.connectionObject().end()
                            - this.spring.origin
                           ).length();

                min = Math.Min(l, min);
                max = Math.Max(l, max);
            }

            this.setAngle(currentAngle);

            Tuple<double, double> result = new Tuple<double, double>(min, max);
            return result;
        }

        public void doMotionSweep(double startAngle)
        {
            // From startAngle, sweep in negative direction until max is reached,
            // then sweep back to max positive direction and collect force vs angle.
            //
            // Also calculates equilibrium angle and checks if lid stays closed or not.

            handForces_.clear();

            double maxDeg = 0;
            double minDeg = 0;

            double deltaRad = Math.PI/360;

            double savedAngle = this.lid.angle;

            this.setAngle(startAngle);

            // Calculate opeining hand force at start angle;
            // if it is positive, lid will stay closed.
            staysClosed_ = (this.handForce(1) > 0.0);

            // sweep to max negative direction
            // go no furhter than -175 degrees
            while (this.open(-deltaRad))
            {
                if (this.lid.deg < -175) break;
            }
            maxDeg = this.lid.deg;

            // Sweep back to max positive direction
            // and calculate resulting hand force.
            //
            // Go no further than +175 degrees

            while (this.open(deltaRad))
            {
                double currentAngle = this.lid.angle;

                if (this.angleIsBetweenStops(currentAngle))
                {
                    handForces_.deg.Add(this.lid.deg);
                    handForces_.open.Add(this.handForce(1));
                    handForces_.close.Add(this.handForce(-1));
                }

                if (this.lid.deg > 175) break;
            }

            minDeg = this.lid.deg;

            // Restore to start position
            this.setAngle(savedAngle);

            // If no possible angle with current lid,
            // do not return empty forceMap
            if (handForces_.deg.Count == 0)
            {
                handForces_.deg.Add(this.lid.deg); // NOTE! degrees in forceMap_
                handForces_.open.Add(this.handForce(1));
                handForces_.close.Add(this.handForce(-1));
            }

            maxSpringDeg_ = maxDeg;
            minSpringDeg_ = minDeg;

            findEquilibriumAngle();
        }

        public void findEquilibriumAngle()
        {
            double maxForce = handForces_.open.Max();
            double minForce = handForces_.open.Min();

            if (maxForce * minForce > 0)
            {
                // Same sign. No equlibrium. Set to something recognizable
                equilibriumAngle_ = 1e6;
            }
            else
            {
                for (int i = 1; i < handForces_.deg.Count; i++)
                {
                    /* 
                     * Here, wee loop through handForces_ in positive index direction.
                     * Since the calculational coordinate system is inverted compared
                     * to the "GUI" dito, the following loop, that finds the last
                     * signChange in the handForces_, actually sets equilibrium to the
                     * first occurence in the GUI cs.
                     */
                    bool signChange = handForces_.open[i]*handForces_.open_[i-1] <= 0;
                    if (signChange)
                    {
                        equilibriumAngle_ = SpringForms.rad(handForces_.deg_[i]);
                    }
                }
            }
        }

        public bool rangeTest(double startAngle, double deltaAngle)
        {
            // From startAngle, sweep in negative direction until max is reached,

            int nSteps = 60;

            double deltaRad = deltaAngle * Math.PI / (180*nSteps);

            double savedAngle = this.lid.angle;

            this.setAngle(startAngle);

            bool passed = false;

            for (int i = 0; i <= nSteps; i++)
            {
                passed = this.open(deltaRad);
            }

            // Restore to start position
            this.setAngle(savedAngle);

            return passed;
        }

        public bool angleIsBetweenStops(double a0)
        {
            if ( startAngle_ < stopAngle_ )
            {
                return (a0 < stopAngle_) && (a0 > startAngle_);
            }
            else if (startAngle_ > stopAngle_ )
            {
                return (a0 > stopAngle_) && (a0 < startAngle_);
            }
            return false;
        }

        public double handForce(int openOrClose)
        {
            // According to thesis the friction adds to force when spring
            // compresses only. This is somewhat funny, but implemens it
            // anyway. The thesis code did the addition of friction force
            // completely wrong! (They Explicitly added friction force to
            // hand force!?)
            
            double ff = Math.Max(Math.Sign(-openOrClose*this.spring.dL),0) * this.spring.friction;

            Vector2D frictionForce = new Vector2D(ff, 0);
            frictionForce.setAngle(this.spring.angle);

            Vector2D springForce = this.spring.force(temperature_) + frictionForce;

            Vector2D g = new Vector2D(0, 9.81); // Up or down in bitmap??
            double Mg = this.lid.momentFromGravity(g);
            double Ms =this.lid.moment
            (
               this.nSprings * springForce,
               this.lid.connectionObject().end()
            );

            return this.lid.endReactionForce(Mg + Ms);
        }

        public void draw(Bitmap bitmap)
        {
            spring_.draw(bitmap);
            lid_.draw(bitmap);
            lid_.drawConnection(bitmap);
        }

        public void drawShadow(Bitmap bitmap, double angle)
        {
            Object2D tmpOb = new Object2D(lid_.length,0,0,lid_.origin);
            tmpOb.visualScaleFactor = this.lid.visualScaleFactor;
            tmpOb.setAngle(angle);
            tmpOb.draw(bitmap, new Pen(Color.LightGray));
        }

        public void drawLimits(Bitmap bitmap)
        {
            Object2D tmpOb = new Object2D(lid_.length/6, 0, 0, lid_.origin);
            tmpOb.visualScaleFactor = this.lid.visualScaleFactor;
            tmpOb.setAngle(SpringForms.rad(minSpringDeg_));
            tmpOb.draw(bitmap, new Pen(Color.DarkBlue));
            tmpOb.setAngle(SpringForms.rad(maxSpringDeg_));
            tmpOb.draw(bitmap, new Pen(Color.DarkCyan));
        }


        public Lid lid
        {
            get { return lid_; }
        }

        public Spring spring
        {
            get { return spring_; }
            set
            {
               spring_ = value;
               spring_.constrainToLid(lid_);
            }
        }

        public int nSprings
        {
            get { return nSprings_; }
            set { nSprings_ = value;}
        }

        public double temperature
        {
            get { return temperature_; }
            set { temperature_ = value; }
        }

        public bool staysClosed
        {
            get { return staysClosed_; }
        }

        public double equilibriumAngle
        {
            get { return equilibriumAngle_; }
        }

        public double selfOpeningDeg
        {
            get { return (-equilibriumAngle_+startAngle_)*180/Math.PI; }
        }

        public double referenceTemperature
        {
            get { return refTemperature_; }
        }

        public double minSpringDeg
        {
            get { return minSpringDeg_; }
        }

        public double maxSpringDeg
        {
            get { return maxSpringDeg_; }
        }

        public HandForces handForces
        {
            get { return handForces_; }
        }

        public double startAngle
        {
            get { return startAngle_; }
            set { startAngle_ = value; }
        }

        public double stopAngle
        {
            get { return stopAngle_; }
            set { stopAngle_ = value; }
        }

        public void changeSpring(Spring s)
        {
            // Doing what I can to copy thins and avoid refs
            // which elude me.
            Vector2D o = new Vector2D(spring_.origin);
            //spring_ = new Spring(s);
            spring_ = s;
            spring_.origin = o;
            spring_.constrainToLid(lid_);
        }
    }
}
