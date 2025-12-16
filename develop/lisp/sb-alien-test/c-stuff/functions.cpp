
#include <iostream>
#include <math.h>
#include <cmath>

extern "C" float circle_area(const float radius);
extern "C" float circle_circumference(const float radius);

float circle_area(const float radius)
{
    return M_PI * pow(radius, 2);
}

float circle_circumference(const float radius)
{
    return M_PI * radius * 2;
}

/*
int main(const int argc, char** argv)
{
    std::cout << circle_area(5) << std::endl;
    std::cout << circle_circumference(5) << std::endl;
    return 0;
}
*/
