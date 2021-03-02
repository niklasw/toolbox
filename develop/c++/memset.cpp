/* memset example                                                             */
/* g++ -std=c++14 -m64 -o memset memset.cpp                                   */
/* x86_64-w64-mingw32-g++ -std=c++14 -m64 -o memset_mingw memset.cpp          */
#include <stdio.h>
#include <iostream>
#include <string.h>

int main ()
{
  char str[] = "almost every programmer should know memset!";
  memset (str,'-',12);
  puts (str);

  pid_t pid_type = 4234455645;
  mode_t mode_type = 34;
  int normal_int = 4;
  unsigned short usigned = 4;
  long long_int = 4;
  double double_scalar = 35.2;

  int byte = 8;

  std::cout << "pid_t   " << sizeof(pid_type)*byte << std::endl;
  std::cout << "mode_t   " << sizeof(mode_type)*byte << std::endl;
  std::cout << "u short  " << sizeof(usigned)*byte << std::endl;
  std::cout << "int     " << sizeof(normal_int)*byte << std::endl;
  std::cout << "long    " << sizeof(long_int)*byte << std::endl;
  std::cout << "double  " << sizeof(double_scalar)*byte << std::endl;

  return 0;
}
