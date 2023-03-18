#include <iostream>
#include <fstream>
#include <filesystem>
#include <string.h>

using namespace std;

int main(const int argc, const char** argv)
{
    if (argc > 1)
    {
        cout << "Number of args = " << argc << endl;
    }

    int counter = 0;

    while (counter < argc)
    {
        const char* arg = argv[counter];
        if(counter++, strlen(arg) > 1)
        {
            cout << "what?  " << counter <<  " " << arg << endl;
        }
    }

    filesystem::copy("/tmp/tt","./tt");

    /* -------------------- */

    string inp1;
    string inp2;
    string str("Пароход медленно проходит мимо");

    getline(cin, inp1);
    getline(cin, inp2);

    cout << inp1 << endl;
    cout << inp2 << endl;
    cout << str  << endl;

    ofstream fh("output.txt");
    fh << str+inp2 << endl;
    fh.close();
}
