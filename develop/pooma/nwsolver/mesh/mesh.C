
/*
    mesh.C
*/

#include "Tiny/Vector.h"
#include "Pooma/Arrays.h"
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <iomanip>

#define vfield Array<2,Vector<2,double> > 
#define varray Array<1,Vector<2,double> > 
#define sfield Array<2,double> 

int DIM = 2;

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

varray readPoints( const char* file )
{
    std::ifstream f(file,std::ios::in);

    Vector<2> tmpV;

    int ni,nj;
    f >> ni >> nj;
    int n = nj*nj;

    varray points(n);
    for (int i=0; i<n; i++)
    {
	f >> tmpV(0) >> tmpV(1);
	points(i) = tmpV;
    }
    return points;
}

void readPoints( varray points, const char* file)
{
    points = readPoints( file );
}


class CV
{
private:
    Array<1, int> pointN_;
    Vector<2> center_;
    //Array<1, Vector<2> > sfvector_;

    void calculateCenter(const varray& points)
    {
       for (int i=0; i<pointN_.size(); i++)
       {
           center_+=points(pointN_(i));
       }
       center_/=pointN_.size();
    }

public:
    // Null constructor:
    CV():pointN_(0), center_(0){}

    // Constructor main:
    CV(Array<1, int> ptN, const varray& points)
    : pointN_(ptN)
    {
        calculateCenter(points);
    }
    // Members
    
    //- access
    const Vector<2> center() {return center_;}
    const Array<1, int> pointN() {return pointN_;}

};

Array<1, CV> constructCVs(const varray& points, int ni, int nj)
{
    Array<1, int> ptN(4);
    int n = ni*nj;
    int nCVs = n-ni-nj;
    Array<1,CV> CVs(nCVs);
    for (int i=0; i<n; i++)
    {    
	if ( ( i%ni != 0 ) && ( i< n-nj ) )
	{
	    ptN(0) = i;
	    ptN(1) = i+1;
	    ptN(2) = i+1+nj;
	    ptN(3) = i+nj;
	    std::cout << i << ptN << std::endl;
	    CVs(i) = CV(ptN, points);
	}
    }
    return CVs;
}

/*--------------------------------------------------------*/

int
main(
    int                 argc,           // argument count
    char*               argv[]          // argument list
){
    Pooma::initialize(argc, argv);

    char* nodeFile = "points";
    varray points = readPoints(nodeFile);
    Array<1, CV> cellList;

    cellList = constructCVs(points,21,21);

    for (int i=0; i< cellList.size(); i++)
    {
	std::cout << cellList(i).center() << std::endl;
    }
    std::cout << points << std::endl;
    Pooma::finalize();
    return 0;
}
