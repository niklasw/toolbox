#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>


using namespace std;

string testfun( const string &sss )
{
	return sss;
}

int main(int argc, char *argv[])
{

	cout << "Hello" << endl;

	string s1;
	char *c1 = "niklas";
	char *c2 = "wikstrom";
	char *c3;
	string s3;
	s1 = c1;
	string s2(c2);


	c3 = (char*) s1.c_str();

	cout << "Hello " << s1 << " " << s2 <<  endl;
	cout << "chars " << c3 << endl;
	return 0;
}
