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
using System.Threading.Tasks;
using System.Drawing;


/*
 * NOTE: Angles allways treated as radians
 * Also note: These objects are created without
 * any performance concern whatsoever. The app
 * is not demanding, so I focus on simplicity.
 */

namespace HatchTest
{
        internal class RotationMatrix
        {
            /* Very simple matrix internal class used only for rotation of
             * Vector2D objects. Rotation of a Vector2D as coarsely
             * follows:
             *
             * RotationMatrix rot = new RotationMatrix(angle);
             * rotadedVector = vector.dotProduct(RotationMatrix)
             */
            private readonly double[] elements_;

            public RotationMatrix(double angle)
            {
                elements_ = new double[9];
                double cos = Math.Cos(angle);
                double sin = Math.Sin(angle);
                elements_[0] = cos;
                elements_[1] = -sin;
                elements_[2] = 0.0;
                elements_[3] = sin;
                elements_[4] = cos;
                elements_[5] = 0.0;
                elements_[6] = 0.0;
                elements_[7] = 0.0;
                elements_[8] = 1.0;
            }

            public double get(int i, int j)
            {
                int index = 3 * i + j;
                return elements_[index];
            }
        }

        internal class Vector2D
        {
            /*
             * Class for all 2D vector handling. All 2D objects used
             * rely heavily on a Vector2D. It is not a complete vector
             * algebra definition.
             *
             * A 2D object (Object2D) manipulation in terms of orientation
             * (rotation) information must me managed through it's vector
             * member.
             */

            protected double x_, y_;

            public Vector2D(double x, double y)
            {
                x_ = x; y_ = y;
            }

            public Vector2D(Vector2D v)
            {
                // Copy constructor.
                x_ = v.X;
                y_ = v.Y;
                //// HIDE Console.WriteLine("Vector2D copy CONSTRUCTOR");
            }

            public Vector2D()
            {
                // Setting this to (1,0)...
                x_ = 1;
                y_ = 0;
            }

            public double X
            {
                get { return x_; }
                set { x_ = value; }
            }
            public double Y
            {
                get { return y_; }
                set { y_ = value; }
            }

            public double dotProduct(Vector2D v)
            {
                return x_ * v.X + y_ * v.Y;
            }

            public double crossProduct(Vector2D v)
            {
                return  x_ * v.Y - y_ * v.X;
            }

            public Vector2D dotProduct(RotationMatrix M)
            {
                double x = this.dotProduct(new Vector2D(M.get(0, 0), M.get(0, 1)));
                double y = this.dotProduct(new Vector2D(M.get(1, 0), M.get(1, 1)));
                return new Vector2D(x, y);
            }

            public double length()
            {
                return mag();
            }

            public double mag()
            {
                return Math.Sqrt(Math.Pow(x_, 2) + Math.Pow(y_, 2));
            }

            public void setLength(double newLength)
            {
                double e = newLength / this.length();
                x_ *= e;
                y_ *= e;
            }

            public Vector2D norm()
            {
                // Normalize length. Return (0,0) if length == 0.
                if (length() > 0)
                {
                    return new Vector2D(this.X / length(), this.Y / length());
                }
                else
                {
                    return new Vector2D();
                }
            }

            public double angle()
            {
                return Math.Atan2(y_, x_);
            }

            public void setAngle(double setAngle)
            {
                double l = length();
                x_ = l; y_ = 0;
                rotate(setAngle);
            }

            public void translate(Vector2D v)
            {
                x_ += v.X; y_ += v.Y;
            }

            public void rotate(double angle)
            {
                Vector2D v = dotProduct(new RotationMatrix(angle));
                x_ = v.X;
                y_ = v.Y;
            }

            public UnitVector2D orthogonal()
            {
                UnitVector2D u = new UnitVector2D(this);
                u.rotate(Math.PI / 2);
                return u;
            }

            public Point point()
            {
                int[] coords = new int[2];
                return new Point((int)Math.Round(this.X), (int)Math.Round(this.Y));
            }

            // Common vector operators.

            public static Vector2D operator +(Vector2D a, Vector2D b)
            {
                return new Vector2D(a.X + b.X, a.Y + b.Y);
            }
            public static Vector2D operator -(Vector2D a, Vector2D b)
            {
                return new Vector2D(a.X - b.X, a.Y - b.Y);
            }
            public static Vector2D operator *(double a, Vector2D b)
            {
                return new Vector2D(a * b.X, a * b.Y);
            }
            public static Vector2D operator *(Vector2D b, double a)
            {
                return new Vector2D(a * b.X, a * b.Y);
            }
            public static double operator &(Vector2D a, Vector2D b)
            {
                return a.dotProduct(b);
            }
            public static Vector2D operator &(Vector2D a, RotationMatrix M)
            {
                return a.dotProduct(M);
            }
            public static double operator ^(Vector2D a, Vector2D b)
            {
                return a.crossProduct(b);
            }

        }

        internal class UnitVector2D : Vector2D
        {
            /*
             * A special Vector2D with length 1.0
             */
            public UnitVector2D()
            {
                // Well, let's say the default unit vector is (1,0)
                x_ = 1;
                y_ = 0;
            }

            public UnitVector2D(double angle)
            {
                // Construct with given angle.
                x_ = 1;
                y_ = 0;
                rotate(angle);
            }

            public UnitVector2D(Vector2D v)
            {
                /*
                 * Construct a unit vector by normalizing a
                 * Vector2D
                 */
                Vector2D u = v.norm();
                x_ = u.X;
                y_ = u.Y;
            }

            public UnitVector2D(UnitVector2D u)
            {
                // Copy constructor
                x_ = u.X;
                y_ = u.Y;
            }

        }
}
