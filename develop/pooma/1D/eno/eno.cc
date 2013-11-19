
#include "Pooma/Arrays.h"
#include <iostream>

const double x0 =-1;
const double x1 = 1;

int main(int argc, char* argv[])
{
     Pooma::initialize(argc,argv);

     //int size = atoi(argv[0]);
     int size = 100;

     //intervals
     Interval<1> C(1,size-1);
     Interval<1> P(1,size);
     Interval<1> P0(0,size);
     Interval<1> P1(1,size+1);
     Interval<1> F(1,size);

//   mesh
     Array<1, int> cellLabels(size);
     Array<1, int> pointLabels(size+1);
     Array<1, int> faceLabels(size+1);
     Array<1, double> dx(size);
     Array<1, double> cellCentres(size);
     Array<1, double> points(size+1);

     cellLabels = iota(size).comp(0);
     pointLabels = iota(size+1).comp(0);
     faceLabels = pointLabels;

     dx = (x1-x0)/size;
     points = dx*iota(size+1).comp(0);
     cellCentres = 0.5*(points(P1)-points(P0));

//   fields
     Array<1, double> f1(size);
     Array<1, double> f2(size);

     Pooma::finalize();

     return 0;
}
