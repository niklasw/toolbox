#include <iostream>
#include <fstream>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <iomanip>
#include <sys/types.h>
#include <unistd.h>

using namespace std;

void print(const int i, const double f1, const double f2)
{
    cout << setw(10) << i
         << setw(10) << setprecision(4) << f1
         << setw(10) << setprecision(4) << f2 << endl;
}

void print(const int i, const double f1, const double f2, string c)
{
    cout << setw(10) << i
         << setw(10) << setprecision(4) << f1
         << setw(10) << setprecision(4) << f2;

    if (!c.empty())
    {
        cout << right << setw(30) << c << endl;
    }
    else
    {
        cout << endl;
    }
}

void print(const int i, const double f1, const double f2, string c, ofstream& out)
{
    out  << setw(10) << i
         << setw(10) << setprecision(4) << f1
         << setw(10) << setprecision(4) << f2;

    if (!c.empty())
    {
        out << right << setw(30) << c << endl;
    }
    else
    {
        out << endl;
    }
}


int main(int argc, char* argv[])
{
    string qCommand = "ls -ltr"; //"qstat -a | egrep \" P3\""; // | grep P3";

    cout << qCommand << endl;

    FILE *returnValuePtr = popen(qCommand.c_str(),"r");

    if (!returnValuePtr)
    {
        std::cout << qCommand << " Something failed" << endl;
        return -1;
    }
    else
    {
        while (!feof(returnValuePtr))
        {
            char buffer[1024];
            char* linePtr(fgets(buffer, sizeof(buffer), returnValuePtr));
            string line(linePtr);
            string pid = line.substr(0,line.find('.'));
            cout << line << endl;
        }
    }
    cout << "A{A" << qCommand << endl;

    pclose(returnValuePtr);

   // setuid(0);
    return 0;
}


