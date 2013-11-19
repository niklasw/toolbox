/*
** minMaxComponent
**
** Usage: minMaxComponent <source file>
**        (where <source file> is a GUISE file with
**        expanded lists, i.e. no curly braces).
**
** Tool for extracting the min and max values of the individual components
** of a volume scalar or volume vector field (and its cell numbers) from a GUISE file. 
**
** Version 1.0, written 2003-03-26 by Magnus Berglund, magnus.berglund@foi.se
**
*/
#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
using namespace std;

int
main(int argc, char *argv[])
{
    if(argc != 2){
	cout << "Syntax error" << endl;
	cout << "Usage: minMaxComponent <source file>" << endl;
	exit(EXIT_FAILURE);
    }

    ifstream sourceFile(argv[1]);

    if(!sourceFile){
	cout << "Source file, " << argv[1] << ", does not exist" << endl;
	exit(EXIT_FAILURE);
    }

    string buf;

    // check if GUISE file
    sourceFile >> buf >> buf; 
    
//    if(buf != "GUISE"){
//	cout << "Source file, " << argv[1] << ", is not a GUISE file" << endl;
//	exit(EXIT_FAILURE);	
//    }
//
    // check if scalar field or vector field
    sourceFile >> buf >> buf; 
    if((buf != "volScalarField") && (buf != "volVectorField")){
	cout << "Source file does not contain neither a scalar nor a vector field" << endl;
	exit(EXIT_FAILURE);	
    }

    char c;
    sourceFile.get(c);
    while(c != ']') sourceFile.get(c); // Eat rest of file header

    if(buf == "volScalarField"){
	double offset;
	sourceFile >> offset;

	int noOfValues;
	sourceFile >> noOfValues;

	sourceFile.get(c);            
	while(c != '(') sourceFile.get(c); // Eat until left parenthesis found

	double min = 1.0e+499;
	double max = -1.0e+499;
	double value = 0.0;
	int minCell = 0; 
	int maxCell = 0;
	for(int i=1; i<=noOfValues; ++i){
	    sourceFile >> value;
	    if(value < min){ 
		min = value;
		minCell = i;
	    }
	    if(value > max){
		max = value;
		maxCell = i;
	    }
	}
	cout << "Minimum value is " << min+offset << " in cell " << minCell << endl;
	cout << "Maximum value is " << max+offset << " in cell " << maxCell << endl;
    }

    if(buf == "volVectorField"){
	double offsetX, offsetY, offsetZ;

	sourceFile.get(c);
	while(c != '(') sourceFile.get(c); // Eat until left parenthesis found

	sourceFile >> offsetX;
	sourceFile >> offsetY;
	sourceFile >> offsetZ;
	sourceFile.get(c);            // Eat right parenthesis

	int noOfValues;
	sourceFile >> noOfValues;

	sourceFile.get(c); 
	while(c != '(') sourceFile.get(c); // Eat until left parenthesis found 

	double minX, maxX, valueX,
	       minY, maxY, valueY,
	       minZ, maxZ, valueZ;
	minX = minY = minZ = 1.0e+499;
	maxX = maxY = maxZ = -1.0e+499;
	
	int minCellX, maxCellX,
	    minCellY, maxCellY,
	    minCellZ, maxCellZ;
	minCellX = maxCellX = minCellY = maxCellY = minCellZ = maxCellZ = 0;

	for(int i=1; i<=noOfValues; ++i){
	    sourceFile.get(c);
	    while(c != '(') sourceFile.get(c); // Eat until left parenthesis found

	    sourceFile >> valueX;
	    sourceFile >> valueY;
	    sourceFile >> valueZ;

	    if(valueX < minX){ 
		minX = valueX;
		minCellX = i;
	    }
	    if(valueX > maxX){
		maxX = valueX;
		maxCellX = i;
	    }
	    if(valueY < minY){ 
		minY = valueY;
		minCellY = i;
	    }
	    if(valueY > maxY){
		maxY = valueY;
		maxCellY = i;
	    }
	    if(valueZ < minZ){ 
		minZ = valueZ;
		minCellZ = i;
	    }
	    if(valueZ > maxZ){
		maxZ = valueZ;
		maxCellZ = i;
	    }
	}
	cout << "Minimum x-component is " << minX+offsetX << " in cell " << minCellX << endl;
	cout << "Maximum x-component is " << maxX+offsetX << " in cell " << maxCellX << endl;
	cout << "Minimum y-component is " << minY+offsetY << " in cell " << minCellY << endl;
	cout << "Maximum y-component is " << maxY+offsetY << " in cell " << maxCellY << endl;
	cout << "Minimum z-component is " << minZ+offsetZ << " in cell " << minCellZ << endl;
	cout << "Maximum z-component is " << maxZ+offsetZ << " in cell " << maxCellZ << endl;
    }

    return 0;
}
