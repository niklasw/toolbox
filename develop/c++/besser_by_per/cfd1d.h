//1D-Convection
//du/dt+du/dx=0
//loop over faces
//Euler timestepping
//Upwind Diff.

#ifndef SCALARFIELD_H
#define SCALARFIELD_H

class ScalarField {
public:
	ScalarField (int size);
	void print_field();
	double flux_function_1(int i,double alfa,double q[]);
	void no_cell(int size);
	void init();
	void timestep();

	double v[10000];		//array holding vertex x coordinates
	int c[10000][2];		//array holing cell vertex references
	int f[10000][2];		//array holding faces cells references
	double q[10000];		//array holding solution;
	double l;		//Length of domain
	int N;			//Number of cells
	double alfa;		//Blending between CD and UD
	double time;
	double dt;		//timestep size
	int ti_scheme;		//time integration scheme (0=Euler forward, 1=RK4)

};

#endif 
