#include <iostream>
#include <fstream>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <iomanip>

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

int main(int argc, char* argv[])
{

    float fl0 = 0;
    float fl1 = 0;
    int   i  = 0;
    string comment;

    std::ifstream fh("data.txt");

    string tmpstr;
    char* nEnd;

    while(getline(fh,tmpstr))
    {
        try
        {
            i  = strtol(tmpstr.c_str(),&nEnd,10);
            fl0 = strtof(nEnd,&nEnd);
            fl1 = strtof(nEnd,&nEnd);
            comment = nEnd;
        }
        catch(...)
        {
            cout << "Failed to parsed line '" << tmpstr << "'" << endl;   
        }

        print(i,fl0/13,fl1, comment);
    }
}
