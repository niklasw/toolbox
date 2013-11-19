//1D-Convection
//du/dt+du/dx=0
//loop over faces
//Euler timestepping & RK timestepping
//Upwind Diff & Central Diff

#include <iostream>
#include <iomanip>
#include "cfd1d.h"

using namespace std;

ScalarField::ScalarField(int size) : N(size)
{
			
	l=1.0;			//Length of domain

	//Initialize Geometry

	for (int i=0;i<=N;i++)
	{
		v[i]=l*i/N;
	}
	for (int i=1;i<=N;i++)
	{
		c[i][0]=i-1;
		c[i][1]=i;
	}
	for (int i=0;i<=N;i++)
	{
		f[i][0]=i;
		f[i][1]=i+1;
	}
	f[N][1]=1;
	f[0][0]=N;

	//Initialize Field

	for (int i=1;i<=N;i++)
	{
		if ((i<=N/2)&&(i>=N/4))
		{
			q[i]=1;
		}
		else
		{
			q[i]=0;
		}
	}

	//Initialize time;
	time=0.0;
	dt=0.5/N; //Set CFL to 0.5
	alfa=1.0; //Set 
	ti_scheme=0;
}

void ScalarField::init()
{
	for (int i=1;i<=N;i++)
	{
		if ((i<=N/2)&&(i>N/4))
		{
			q[i]=1;
		}
		else
		{
			q[i]=0;
		}
	}
	time=0.0;
}

void ScalarField::no_cell(int size)
{

	N=size;
	//Initialize Geometry

	for (int i=0;i<=N;i++)
	{
		v[i]=l*i/N;
	}
	for (int i=1;i<=N;i++)
	{
		c[i][0]=i-1;
		c[i][1]=i;
	}
	for (int i=0;i<=N;i++)
	{
		f[i][0]=i;
		f[i][1]=i+1;
	}
	f[N][1]=1;
	f[0][0]=N;

	//Initialize Field

	for (int i=1;i<=N;i++)
	{
		if ((i<=N/2)&&(i>N/4))
		{
			q[i]=1;
		}
		else
		{
			q[i]=0;
		}
	}
	time=0.0;
	
}

void ScalarField::print_field()
{
	cout << "cell  " << " x      " << "    u      " << endl;
	for (int i=1;i<=N;i++)
	{
		double midpoint=0.5*(v[c[i][0]]+v[c[i][1]]);
		cout << setw(2) << i << fixed << setprecision(4) << setw(10) << midpoint << setw(10) << q[i] << endl;
	}
}	

double ScalarField::flux_function_1(int i,double alfa,double qf[])
{
	int c1=f[i][0];
	int c2=f[i][1];
	
	return alfa*qf[c1]+(1-alfa)*0.5*(qf[c1]+qf[c2]);
}
	
void ScalarField::timestep()
{
		double dqdt1[10000];	//array hold time derivate of q;
		double dqdt2[10000];
		double dqdt3[10000];
		double dqdt4[10000];
		double k1[10000];
		double k2[10000];
		double k3[10000];
		double k4[10000];	
		double q2[10000];
		double q3[10000];
		double q4[10000];

		if (ti_scheme==0) {

		for (int i=1;i<=N;i++)
		{
			dqdt1[i]=0;
		}
		for (int i=0;i<N;i++)	//loop over all faces but the last due to symmetry
		{
			int c1=f[i][0];
			int c2=f[i][1];
			double cell_size=1.0/N;
			dqdt1[c1]=dqdt1[c1]-1/cell_size*(flux_function_1(i,alfa,q));
			dqdt1[c2]=dqdt1[c2]+1/cell_size*(flux_function_1(i,alfa,q));	
		}
		for (int i=1;i<=N;i++)
		{
			q[i]=q[i]+dt*dqdt1[i];
		}	
		}

		else
		{
		
		for (int i=1;i<=N;i++)
		{
			dqdt1[i]=0;
			dqdt2[i]=0;
			dqdt3[i]=0;
			dqdt4[i]=0;
		}
		
		for (int i=0;i<N;i++)	//loop over all faces but the last due to symmetry
		{
			int c1=f[i][0];
			int c2=f[i][1];
			double cell_size=1.0/N;
			dqdt1[c1]=dqdt1[c1]-1/cell_size*(flux_function_1(i,alfa,q));
			dqdt1[c2]=dqdt1[c2]+1/cell_size*(flux_function_1(i,alfa,q));	
		}
		for (int i=1;i<=N;i++)
		{
			k1[i]=dt*dqdt1[i];
		}
		for (int i=1;i<=N;i++)
		{
			q2[i]=q[i]+0.5*k1[i];
		}	



		for (int i=0;i<N;i++)	//loop over all faces but the last due to symmetry
		{
			int c1=f[i][0];
			int c2=f[i][1];
			double cell_size=1.0/N;
			dqdt2[c1]=dqdt2[c1]-1/cell_size*(flux_function_1(i,alfa,q2));
			dqdt2[c2]=dqdt2[c2]+1/cell_size*(flux_function_1(i,alfa,q2));	
		}
		for (int i=1;i<=N;i++)
		{
			k2[i]=dt*dqdt2[i];
		}
		for (int i=1;i<=N;i++)
		{
			q3[i]=q[i]+0.5*k2[i];
		}	


		
		for (int i=0;i<N;i++)	//loop over all faces but the last due to symmetry
		{
			int c1=f[i][0];
			int c2=f[i][1];
			double cell_size=1.0/N;
			dqdt3[c1]=dqdt3[c1]-1/cell_size*(flux_function_1(i,alfa,q3));
			dqdt3[c2]=dqdt3[c2]+1/cell_size*(flux_function_1(i,alfa,q3));	
		}
		for (int i=1;i<=N;i++)
		{
			k3[i]=dt*dqdt3[i];
		}
		for (int i=1;i<=N;i++)
		{
			q4[i]=q[i]+k3[i];
		}


		for (int i=0;i<N;i++)	//loop over all faces but the last due to symmetry
		{
			int c1=f[i][0];
			int c2=f[i][1];
			double cell_size=1.0/N;
			dqdt4[c1]=dqdt4[c1]-1/cell_size*(flux_function_1(i,alfa,q4));
			dqdt4[c2]=dqdt4[c2]+1/cell_size*(flux_function_1(i,alfa,q4));	
		}
		for (int i=1;i<=N;i++)
		{
			k4[i]=dt*dqdt4[i];
		}


		for (int i=1;i<=N;i++)
		{
			q[i]=q[i]+1.0/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]);
		}	
		}

		time=time+dt;	
}

	
