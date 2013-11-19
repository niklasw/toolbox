/*
    Niklas is testing basic things with POOMA
*/

#include "Tiny/Vector.h"
#include "Pooma/Arrays.h"
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <iomanip>

// The size of each side of the domain.
const int N = 100, M=10;
// Specify the interior of the domain
Interval<1> I(1, N-2), J(1, M-2);
Interval<2> interiorDomain(I,J);

class gradient0
{
public:
    template <class C>
    inline
    typename C::Element_t
    operator()(const C& c, int i, int j) const{
    return c.read(i+1)-c.read(i-1);
    }
    inline int lowerExtent(int) const { return 1; }
    inline int upperExtent(int) const { return 1; }
private:
};

class gradient1
{
public:
    template <class C>
    inline
    typename C::Element_t
    operator()(const C& c, int i, int j) const{
    return c.read(j+1)-c.read(j-1);
    }
    inline int lowerExtent(int) const { return 1; }
    inline int upperExtent(int) const { return 1; }
private:
};

Array<2, Vector<2,double> > grad(const Array<2> &A, const Interval<2> &D)
{
    Interval<1> I = D[0];
    Interval<1> J = D[1];
    Array<2, Vector<2> > B(D);
    B.comp(0) = A(I+1,J)-A(I-1,J);
    B.comp(1) = A(I,J+1)-A(I,J-1);
    return B;
}

template <class D>
void writeData(const D& data, char* file){
    std::ofstream of1(file, std::ios::app);
    of1 << data << std::endl;
    of1.close();
    return;
}

void clearFile(char* file){
    std::ofstream of1(file);
    of1 << "";
    of1.close();
    return;
}


////////////////////////////////////////////////////////

int
main(
    int                 argc,           // argument count
    char*               argv[]          // argument list
){
    // Initialize POOMA.
    Pooma::initialize(argc, argv);

    // The array we'll be solving for
    Array<2> V(N, M);
    V = 0.0;

    // The right hand side of the equation (spike in the center)
    Array<2> b(N, M);
    b = 0.0;
    b(N/2, M/2) = -1.0;

    // Iterate 200 times
    for (int iteration=0; iteration<200; ++iteration)
    {
        V(I,J) = 0.25*(V(I+1,J) + V(I-1,J) + V(I,J+1) + V(I,J-1) - b(I,J));
    }

    // Create grid coords
    Array<1> X(N);
    Array<1> Y(M);
    X = 0;
    Y = 0;

    const float dx = 0.1;
    const float dy = 0.2;
    const Vector<2, float> dr(dx,dy);

    X = dx*iota(N).comp(0);
    Y = dy*iota(M).comp(0);

    // Make a simple gradient thing
    Array<2> W(N,M);
    W = sin(0.05*iota(N,M).comp(0))*sin(0.01*iota(N,M).comp(1));
    Array<2, Vector<2> > gradW(N,M);

    // Try stencil implementation of "grad"
    // Stencil<gradient0> gradX;
    // Stencil<gradient1> gradY;

    gradW(interiorDomain) = grad(W,interiorDomain);
   
    // Try arrays of vectors

    Array<2,Vector<2,double> > U(N,M);
    U.comp(0) = sin(0.05*iota(N,M).comp(0));
    U.comp(1) = cos(0.05*iota(N,M).comp(0));

    // Print out the results
    char* dataFile1="outData";
    clearFile(dataFile1);

    writeData("X",dataFile1);
    writeData(X,dataFile1);
    writeData("Y",dataFile1);
    writeData(Y,dataFile1);

    writeData("W",dataFile1);
    writeData(W,dataFile1);

    writeData("gradW",dataFile1);
    writeData(gradW.comp(0),dataFile1);
    writeData(gradW.comp(1),dataFile1);
    //////////////////////////////////////////

    // Clean up POOMA and report success.
    Pooma::finalize();
    return 0;
    //////////////////////////////////////////
}
