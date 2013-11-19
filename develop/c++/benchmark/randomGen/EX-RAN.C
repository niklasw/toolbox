/*************************** EX-RAN.CPP ********************* AgF 2001-11-11 *
*                                                                            *
* Example showing how to use random number generators from class library.    *
*                                                                            *
* Compile for console mode.                                                  *               *
*****************************************************************************/

#include <time.h>               // define time()
#include <conio.h>              // define getch()
#include "randomc.h"            // define classes for random number generators

// include code for one of the random number generators:
#include "mersenne.cpp"         // members of class TRandomMersenne
// or:
// #include "ranrotw.cpp"       // members of class TRanrotWGenerator
// or:
// #include "mother.cpp"        // members of class TRanrotWGenerator

void main() {
  long int seed = time(0);      // random seed
  
  // choose one of the random number generators:
  TRandomMersenne rg(seed);     // make instance of random number generator
  // or:
  // TRanrotWGenerator rg(seed); // make instance of random number generator
  // or:
  // TRandomMotherOfAll rg(seed); // make instance of random number generator
  
  int i;                        // loop counter
  double r;                     // random number
  long int ir;                  // random integer number


  // make random integers in interval from 0 to 99, inclusive:
  printf("\n\nRandom integers in interval from 0 to 99:\n");
  for (i=0; i<40; i++) {
    ir = rg.IRandom(0,99);
    printf ("%6li  ", ir);}

  // make random floating point numbers in interval from 0 to 1:
  printf("\n\nRandom floating point numbers in interval from 0 to 1:\n");
  for (i=0; i<32; i++) {
    r = rg.Random();
    printf ("%8.6f  ", r);}

  // make random bits (Not for TRandomMotherOfAll):
  printf("\n\nRandom bits (hexadecimal):\n");
  for (i=0; i<32; i++) {
    ir = rg.BRandom();
    printf ("%08lX  ", ir);}

  getch();  // wait for user to press any key
  }
