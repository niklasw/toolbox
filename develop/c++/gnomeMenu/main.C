#include <stdio.h>
#include <iostream>
#include <string>
#include <sys/types.h>
#include <dirent.h>
#include <list>
#include <unistd.h>

using namespace std;

template <class T>
class LIST : public list<T>
{
public:
    LIST<T>::iterator iter;
    void print(){
	for (iter = begin(); iter != end(); ++iter){
	    cout << *iter << endl;
	}
    }
    int length(){
	int length = 0;
	for (iter = begin(); iter != end(); ++iter){
	    length++;
	}
	return length;
    }
};

bool checkArgs(int argc, char* argv[])
{
    bool out = true;
    if ( argc != 2 ){
	cout << "Arg error"<< endl;
	out = false;
    }
    return out;
}

LIST<char*> listDir(char* dir)
{
    DIR* d = opendir(dir);
    dirent* dp;
    char* fileName = "noFile";
    LIST<char*> dirList;
    while (dp = readdir(d)) {
	fileName = dp -> d_name;
	if (fileName[0] == '.') continue;
	dirList.push_back(fileName);
    }
    if (dirList.length() == 0){
	dirList.push_back(fileName);
    }
    closedir(d);
    return dirList;    
}

int main(int argc, char* argv[])
{
    if (! checkArgs(argc,argv)) exit(0);

    char* root = argv[1];
    LIST<char*> dirList = listDir (root);
    dirList.print();
    cout << dirList.length()<< endl;
    return 0;
}
