
#include "blitz/array.h"

using namespace blitz;
using namespace std;


int main()
{

	int size0 = 10;
	int size1 = 20;
	Range RfI(1,size0-1);
	Range RfJ(1,size1-1);
	Array<float, 2> X(size0,size1), f1(size0,size1), f2(size0,size1);
	Array<float,1> dx(size0-1), dy(size1-1);


	firstIndex I;
	secondIndex J;

	dx = 0.01;
	dy = 0.005;

	

	f1 = I/(1.0+J);


	cout << f1 << endl;

	return 0;
}
