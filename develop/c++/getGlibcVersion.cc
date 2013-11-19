#include <stdlib.h>
#include <iostream>
#include <stdio.h>
#include <gnu/libc-version.h>

using namespace std;

int main (void)
{
    const int size=int(10e4);

    double * q;
    q = new double[size];

    double sum = 0;
    for (int i=0; i<size; i++)
    {
        q[i] = i*1.0;
        sum+=q[i];
    }
    cout << "Summa = "<< sum << endl;
    
    puts (gnu_get_libc_version ()); return 0;
}
