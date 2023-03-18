#include <stdlib.h>
#include <iostream>
#include <vector>
#include <array>

#include "point.h"

using namespace std;

int main(int argc, char** argv)
{
    vector<point> pointField(100);

    for(auto& p: pointField)
    {
        p+=10;
        point p2 = p+1;
        //const_cast<point&>(p)+=10;
        p2+=2;
        point p3 = p2;
        p3 = p2*p3+p;
        cout << p3 << ' ';
        cout << point(p2+p+p2.x()) << endl;
    }

    return 0;
}




