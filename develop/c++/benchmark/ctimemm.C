
#define TNT_NO_BOUNDS_CHECK

// Example of timing routine
#include <time.h>
#include <iostream>
#include "tnt/tnt.h"
#include "tnt/vec.h"
#include "tnt/cmat.h"
#include "tnt/stopwatch.h"

using namespace std;
using namespace TNT;

template <class MaTRiX>
void timeit(MaTRiX &C, const MaTRiX &A, const MaTRiX &B,
            double resolution_time, double *final_time,
            double *num_cycles)
{
    stopwatch Q;
    long int cycles=1;

    while(1)
    {

        Q.start();


        for (int r=0; r != cycles; r++)
        {
            matmult(C, A, B);
        }
        Q.stop();

        if (Q.read() >= resolution_time) break;

        cycles *= 2;
        Q.reset();
    }

    *final_time = Q.read();
    *num_cycles = (double) cycles;
}




int main(int argc, char *argv[])
{

        if (argc < 2)
        {
            cerr << "timemm: time mutliplcation of two NxN matrices.\n";
            cerr << "Usage: N [resolution-time] \n";
            cerr << "  (resolution-time is optional, defaults to 1.0 sec)\n";
            cerr << "Returns: N  actual-time   num-flops   Mflops/sec.\n";
            exit(1);
        }

        int F = atoi(argv[1]);
	
	for (int i = 1; i <= 30; i+=2){
	  Subscript N = i*F;
	  double resolution_time = 1.0;    // default to 1 sec timing length


	  if (argc > 2)
            resolution_time = atof(argv[2]);

	  Matrix<double> A(N,N), B(N,N), C(N,N);
	  A = 1.0;
	  B = 2.0;

	  double num_reps = 0.0;
	  double actual_time = 0.0;
	  timeit(C, A, B, resolution_time, &actual_time, &num_reps);

	  cout << "N: " << N << "    time:  " << actual_time
	       <<  "   Mflops: " <<  2e-6*N*N*N*num_reps / actual_time << endl;
	}
	  return 0;
}


