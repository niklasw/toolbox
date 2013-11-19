#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <unistd.h>



using namespace std;


vector<string> Split(string &str)
{
	string buf;
	stringstream ss(str);
	vector<string> wvec;

	while ( ss >> buf)
		wvec.push_back(buf);
	return wvec;	
}

int main(int argc, char *argv[])
{
	char *curdir="/tmp";
	char *temp;
	unsigned int lint;


	DIR *dir;
	struct dirent *de;
	struct stat status;
	
	chdir(curdir);

	cout << "Current dir is " << get_current_dir_name() << "\n"<< endl;
	char *cwd = get_current_dir_name();

	dir = opendir(cwd);

	while (de = readdir(dir)) {
		char *file = de->d_name;
		lstat(file,&status);
		if (S_ISDIR(status.st_mode)){
			if (( strcmp(file,".") != 0) && ( strcmp(file,"..") != 0 )) {
				chdir(file);
				cout << get_current_dir_name() << endl;
			}
		}
		

	}

	string wlist("vof U p gamma");

	vector<string> wvec = Split(wlist);

	for ( int i=0; i < wvec.size(); i++)
		cout << wvec[i] << endl;

	return 0;
}
