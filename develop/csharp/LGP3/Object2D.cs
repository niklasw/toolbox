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
using System.ComponentModel;

namespace HatchTest
{

    internal class Object2D
    {
        /* 
         * A kind of general 2D object (rod-like) with length, mass, cog and origin.
         * It can be drawn on a bitmap.
         * Orientaion and length is kept as a Vector2D and all transformations
         * are made via the Vector2D.
         * 
         * Spring and Lid inherits this class.
         */
        private double mass_;
        private double relCog_;
        private double visualScaleFactor_ = 0.2;
        private Vector2D origin_;
        protected Vector2D v_;

        protected Pen pen_;

        public Object2D(double length, double mass, double relCog, Vector2D origin)
        {
            mass_ = mass;
            relCog_ = relCog;
            origin_ = origin;
            v_ = new Vector2D(length,0);
            pen_ = new Pen(Color.Black, 1);
        }

        public Object2D(string length, string mass, string relCog, Vector2D origin)
        {
            try
            {
                mass_ = Double.Parse(mass);
                relCog_ = Double.Parse(relCog);
                origin_ = origin;
                double l = Double.Parse(length);
                v_ = new Vector2D(l, 0);
            }
            catch(FormatException)
            {
                // HIDE Console.WriteLine("Object parameter not valid. Could not create Object2D.");
            }
            pen_ = new Pen(Color.Black, 1);
        }

        public Object2D(Object2D ob)
        {
            // Copy constructor
            mass_ = ob.mass;
            relCog_ = ob.relCog;
            origin_ = ob.origin;
            v_ = ob.vector;
            pen_ = new Pen(Color.Black, 1);
            // // HIDE Console.WriteLine("Object2D copy constr.");
        }

        public Object2D()
        {
            mass_ = 1;
            relCog_ = 0.5;
            origin_ = new Vector2D(0, 0);
            v_ = new Vector2D();
            pen_ = new Pen(Color.Black, 1);
        }

        public Vector2D position(double fraction)
        {
            return origin_ + fraction * v_;
        }

        public Vector2D end()
        {
            return origin_ + v_;
        }

        public void rotate(double alpha)
        {
            v_.rotate(alpha);
        }

        public void setAngle(double alpha)
        {
            v_.setAngle(alpha);
        }

        public void scale(double fraction)
        {
            v_ *= fraction;
        }

        /*
         * Make object longer, in both ends.
         
        public void extend(double a, double b)
        {
            // Do not move origin.
            //origin_ = origin_ + a * v_.norm();
            v_.setLength(v_.length()+a+b);
        }
         */

        // Access

        public Vector2D origin
        {
            get { return origin_; }
            set { origin_ = value; }
        }

        public double angle
        {
            get { return v_.angle(); }
        }

        public double deg
        {
            get { return v_.angle()*180/Math.PI; }
        }

        protected Vector2D vector
        {
            get { return v_; }
        }

        public double length
        {
            get { return v_.length(); }
            set { v_.setLength(value); }
        }

        public void setLength(double newLength)
        {
            v_.setLength(newLength);
        }

        public double mass
        {
            get { return mass_; }
            set { mass_ = value; }
        }

        public double relCog
        {
            get { return relCog_; }
            set { relCog_ = value; }
        }

        public Vector2D cog()
        {
            return position(relCog_);
        }

        public double visualScaleFactor
        {
            get { return visualScaleFactor_; }
            set { visualScaleFactor_ = value; }
        }

        public double moment(Vector2D force, Vector2D P)
        {
            /*
             * moment around origin from force vector acting at
             * point P.
             * Evaluated as cross product M = (Force x Lever)
             */
            return force.crossProduct(P-this.origin);
        }

        public double momentFromGravity(Vector2D g)
        {
            Vector2D cog = position(relCog_);
            return moment(mass_ * g, cog);
        }

        public double reactionForce(double M, Vector2D P, UnitVector2D u)
        {
            /*
             * If moment M is applied around origin what is
             * the reaction force at position P in direction u
             *
             * Note that unitMomenP will be zero, only if P = (0, 0)
             */
            double unitMomentP = moment(u, P);

            double fP = 0.0;
            if ( unitMomentP != 0 )
            {
                fP = M / unitMomentP;
            }
            else
            {
                string message = string.Format("{0}\n{1}",
                    "Error in Object2D::reactionForce:",
                    "Action force probably through or at origo.");

                System.Windows.Forms.MessageBox.Show(message);
            }
            return fP;
        }

        public double endReactionForce(double M)
        {
            /* Orthogonal reaction force at end point
             * given the moment M arond origo
             */
            return reactionForce(M, end(), this.vector.orthogonal());
        }

        public void translate(Vector2D translation)
        {
            origin_ += translation;
        }

        public void setOrigin(Vector2D newOrigin)
        {
            origin_ = newOrigin;
        }

        public Object2D copyTranslate(Vector2D translation)
        {
            Object2D ob = new Object2D(this);
            ob.translate(translation);
            return ob;
        }

        public void draw(Bitmap bitmap, Pen p, float end0 = 0, float end1 = 0)
        {
            Size size = bitmap.Size;
            Graphics graphics = Graphics.FromImage(bitmap);

            graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;

            Vector2D centering = new Vector2D(size.Width / 4, size.Height / 2);

            Vector2D o = origin_ * visualScaleFactor_ + centering;
            Vector2D e = end() * visualScaleFactor_ + centering;
            
            graphics.DrawLine(p, o.point(), e.point());

            if (end0 > 0)
            {
                float x = (float) o.X - end0 / 2;
                float y = (float) o.Y - end0 / 2;
                graphics.DrawEllipse(p, x, y, end0, end0);
            }
            if (end1 > 0)
            {
                float x = (float) e.X - end1 / 2;
                float y = (float) e.Y - end1 / 2;
                graphics.DrawEllipse(p, x, y, end1, end1);
            }
        }

        public void draw(Bitmap bitmap, float end0 = 0, float end1 = 0)
        {
            draw(bitmap, pen_, end0, end1);
        }


        public void selectPen(Pen pen)
        {
            pen_ = pen;
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
