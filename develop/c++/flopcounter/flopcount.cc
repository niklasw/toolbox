
/*

g++ -O3 -funroll-all-loops -mfpmath=sse -march=pentium4 flopcount.cc

*/


#include <iostream>
#include <sys/time.h>

using namespace std;

/**********************************************************************
 * GetClock - get current time (expressed in seconds).
 **********************************************************************/
double GetClock(void)
{
  struct timeval tv;
  gettimeofday(&tv,NULL);
  return ((double)tv.tv_sec+(double)tv.tv_usec*1e-6);
}


int main( int argc, char *argv[] )
{
    double result = 1.0;
    double tmp = 1.0/3;
    int N = 1000000;
    double a;
    double t0 = GetClock();
    for (int i=0; i<N; i++){
        result+=tmp*tmp;
    }
    double t1 = GetClock() - t0;
    cout << "Time =\t" << t1 << " sec" << endl;
    cout << "Flops =\t" << 2*N/t1 << endl;
    cout << result << endl;
}
