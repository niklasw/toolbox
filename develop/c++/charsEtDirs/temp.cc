#include <dirent.h>
#include <iostream>
#include <string>
#include <vector>
#include <sys/types.h>
#include <sys/stat.h>

using namespace std;

class dirParser
{
  private:
  	char *root_;
	DIR *dirp_;
	struct dirent *dent_;


  public:

  	/* Constructor */
	dirParser(const string &root)
	{
		root_ = (char*)root.c_str();
		chdir(root_);

  		if ((dirp_ = opendir(root_)) == NULL) {
      		fprintf(stderr, "Could not open dir %s\n", root_);
  		}

	}

/*
	dirParser(const dirParser &fp)
	{
		root_ = fp.root();
	}
*/

	void cd(string &newd)
	{
		root_ = (char*)newd.c_str();
		chdir(root_);

  		if ((dirp_ = opendir(root_)) == NULL) {
      		fprintf(stderr, "Could not open dir %s\n", root_);
  		}

	}

	vector<string> ls()
	{
		vector<string> fvec;
  		while ((dent_ = readdir(dirp_)) != NULL) {
			fvec.push_back(string(dent_->d_name));
  		}
		return fvec;
	}

	bool hasfile( const string &astring)
	{
		bool found = false;
		vector<string> dirContent = ls();
		for (int i=0 ; i< dirContent.size(); i++) {
			if (dirContent[i] == astring) found = true;	
		}
		return found;
	}

	bool isdir(const string &astring)
	{
		bool ok = false;
		struct stat inode;
		if ( stat(astring.c_str(),&inode) != -1 ) {
			ok = S_ISDIR(inode.st_mode);
		}
		return ok;
	}

	vector<string> listdirs()
	{
			cout << "HELLO" << endl;
		vector<string> fvec = ls();
		vector<string> dirs;
		for (int i=0; i<fvec.size(); i++) {
			if ( isdir(fvec[i]) )
				dirs.push_back(fvec[i]);	
		}
		return dirs;
	}

	vector<string> listfiles()
	{
		vector<string> fvec = ls();
		vector<string> files;
		for (int i=0; i<fvec.size(); i++) {
			if ( ! isdir(fvec[i]) )
				files.push_back(fvec[i]);	
		}
		return files;
	}

	char *root() { return root_; }
	char *pwd() { return root_; }


};

int main(int argc, const char **argv) {

	string path("/home/nikwik/tmp");

	if (argc > 1){
		path = argv[1];
	}

	dirParser DP(path);

	vector<string> dirContent = DP.ls();

	for (int i=0 ; i< dirContent.size(); i++) {
		if ( DP.isdir(dirContent[i]) ) cout << "D: ";
		else cout << "F: ";
		cout << dirContent[i] << endl;
	}

	vector<string> files = DP.listdirs();
	
	cout << files.size() << endl;

	for (int i=0 ; i< files.size(); i++) {
		cout << files[i] << endl;
	}
    return 0;
}


/*
  DIR *dirp;
    struct dirent *direntry;

  if ((dirp = opendir(dirname)) == NULL) {
      fprintf(stderr, "Could not open dir %s\n", dirname);
      return 1;
  }

  while ((direntry = readdir(dirp)) != NULL) {
    fprintf(stdout, "%s\n", direntry->d_name);
  }

  closedir(dirp);
*/

