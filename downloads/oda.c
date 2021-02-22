/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
             ODA: an optimization package using  
                  the orthogonal decomposition  algorithm        
/*  This package handles:
 Unconstrained linear problems (over- or determined ):  LSSLS
 Unconstrained linear problems (undetermined:          MNSLS
 Unconstrained nonlinear problems:                     LSSNLS
 Constrained Linear Problems:                          LSSCLS
 Constrained nonlinear Problems:                       LSSCNL
 Arbitrary objective function:                         ARBITRARY 
*/

/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Users must specify:

1.
Dim_Phi                    : dimension of phi for 
Num_Variable               : # of variable 
Num_Constraints            : # of constraints  

2. Functions FUNF, FUNPHI, DPHIDX, JACOBIAN, HESSIAN, FUNH, and DHDX

3. Initial guess

4. subroutines LSSLS, MNSLS, LSSNLS, LSSCLS, LSSCNL, or ARBITRARY 

For your convenience,
search for the string "USER INPUT", and finish at "END USER INPUT".

To compile the code, use

gcc filename.c -lm

The executable file by default is

a.out


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

/* !!!  PLEASE NOTICE:  !!! 

1. all arrays in C start with index 0.
   Therefore, an mxn matrix A in C have entities as:
   A[0][0],   ...  ,A[0][n-1]
   A[1][0],   ...  ,A[1][n-1]
              ...        
   A[m-1][0], ...  ,A[m-1][n-1]

2. An n-dimensional vector is considered as an nx1 matrix in the program.
   Therefore, an n-dimensional vector v  have entities as:
   v[0][0], v[1][0], ..., v[n-1][0]
        ^        ^               ^
        |________|___ ... _______| USE[0] HERE, B/C C STARTS WITH 0 !!
	
3. Not all subroutines require to specify functions FUNF, FUNPHI,
   DPHIDX, JACOBIAN, HESSIAN, FUNH, and DHDX. However, even in those
   cases, these functions have to be defined. Leave it blank there.

   For example, in subroutine ARBITRARY, FUNPHI and DPHIDX need not be
   given, they should be defined as follows:

   void FUNPHI(int q,int n,double **x,double **f) 
   {  
   NUM_F++; }  

   void DPHIDX(int q,int n,double **x,double **df)
   {
   NUM_DF++;
   } 

*/

/* Subroutines are described as follows */
/* void LSSLS(double **vx, double **Ain,double **vb, int q, int n)
 Unconstrained linear problems: minimum norm solutions for
   over- or determined linear systems
   Ax=b; A:qxn q>n 

   n:    number of design variables 
   q:    dimension of function phi   
   vx:   design variables, an initial guess must be given, the optimum
         solution found will over write the initial values 
   Ain:  A q x n matrix 
   vb:   A q x 1 matrix
*/

/*  void MNSLS(double **vx, double **Cin,double **vd, int ell, int n)
Unconstrained linear problems: minimum norm solutions for
	underdetermined linear systems
     Cx=d; C:ellxn ell<=n 
   n:    number of design variables 
   ell:  number of constraints 
   vx:   design variables, an initial guess must be given, the optimum
         solution found will over write the initial values 
   Cin:  A ell x n matrix
   vd:   A ell x 1 matrix 
*/


/* void LSSNLS(double **f_min,double **xk, double **W, int q,int n,
		      double tol ) 
Unconstrained nonlinear problems
   n:    number of design variables  
   q:    dimension of function phi   
   xk:   design variables, an initial guess must be given, the optimum
         solution found will over write the initial values 
   W:    The weight function  
   tol:  Tolerance 
   The subroutine returns a value of the optimum objective function
   with f_min
   FUNPHI, and DPHIDX must be given.
*/


/* void LSSCLS(double **f_min,double **vx, double **W, double **Ain, double
	    **vb, double **Cin, double **vd,int q, int n, int ell)
   Constrained Linear Problems  
   Solve the least square problem Ax=b 
   subject to Cx=d 

   n:    number of design variables 
   q:    dimension of function phi   
   ell:  number of constraints 
   vx:   design variables, an initial guess must be given, the optimum
         solution found will over write the initial values 
   W:    The weight function   
   Ain:  A q x n matrix 
   vb:   A q x 1 matrix
   Cin:  A ell x n matrix
   vd:   A ell x 1 matrix 
   The subroutine returns a value of the optimum objective function
   with f_min
*/



/*void LSSCNL(double **f_min, double **xk, double **W, int q,int n,int
	    ell,double tol1, double tol2) 
    Constrained nonlinear Problems
    n:    number of design variables 
    q:    dimension of function phi   
    ell:  number of constraints 
    xk:   design variables, an initial guess must be given, the optimum
              solution found will over write the initial values 
    W:    The weight function   
    tol1: tolerance for delta_x 
    tol2: tolerance for delta_g
 
    The subroutine returns a value of the optimum objective function
    with f_min
    FUNPHI, DPHIDX, FUNH, and DHDX must be given.
*/



/* double ARBITRARY (int n, int ell, double **xold, double epsilon1,
		  double epsilon2) 
  Subroutine for an arbitrary objective function
    n:        number of design variables 
    ell:      number of constraints 
    xold:     design variables, an initial guess must be given, the optimum
              solution found will over write the initial values 
    epsilon1: tolerance for delta_x 
    epsilon2: tolerance for delta_g
 
    The subroutine returns a value of the optimum objective function
    with f_min    
    FUNF, JACOBIAN, HESSIAN, FUNH, and DHDX must be given.
*/
/*
void freudenstein(double *k, double input, double *out)
solving the freudenstein euqaiotn
With "k" and "input" given, return two solutions of "out"
k[0] --> k1; k[1]-->k2; k[2]---> k3;
*/
/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
//#include <sys/time.h>
//#include <sys/resource.h>
#define FREE_ARG char*
#define MAX_ITER 100000

/***********USER INPUT ************************************************/
/***********The following must be given by users **********************/

#define Dim_Phi 3 /* dimension of phi for:q */
#define Num_Variable 2 /* # of variable:n */
#define Num_Constraints 1 /* # of constraints:l */
#define DAMPING_FACTOR 1.0 /* play with the damping factor if your
			  programm cannot converge */
/**********************************************************************/
/*********************** END USER INPUT ******************************/

#define MU 2.8
#define MU2 1.1

int NUM_F=0,NUM_Z=0,NUM_DF=0,NUM_H=0,NUM_G=0,NUM_DG=0;


long NR_END=0;
long Q=Dim_Phi,N=Num_Variable,ELL=Num_Constraints;

double FUNF(double **x);
void FUNPHI(int q,int n,double **x,double **f);
void DPHIDX(int q,int n,double **x,double **df);
void JACOBIAN(int n,double **x,double **df);
void HESSIAN(int n,double **x,double **hess);
void FUNH(int n, int ell, double **x, double **g);
void DHDX(int n, int ell, double **x, double **dg);

void LSSLS(double **vx, double **Ain,double **vb, int q, int n);
void MNSLS(double **vx, double **Cin,double **vd, int l, int n);
void LSSNLS(double **f_min,double **xk, double **W, int q,int n, double
	    tol );
void LSSCLS(double **f_min,double **vx, double **W, double **Ain, double **vb, double **Cin, double **vd,int q, int n, int l);
void LSSCNL(double **f_min, double **xk, double **W, int q,int n,int
	    ell,double tol1, double tol2);
double ARBITRARY (int n, int l, double **xold, double epsilon1, double epsilon2);



double **matrix(long nrow,long ncol);
void free_matrix(double **m,long nrow,long ncol );
int **matrix_i(long nrow,long ncol);
void free_matrix_i(int **m,long nrow,long ncol );
void nrerror(char error_text[]);

void I_mat(double **eye_mat, int n);
void mat_copy(double **mA,double **mB, int m, int n);
double vdot( double **a,double **b, int Num_Row);
void mmult(double **mA, double **mB, double **mC, int Num_Row,int
	      Num_Iter, int Num_Column); /* a=bxc*/
void madd(double **mA, double **mB, double scale, double **mC, int
	     m, int n);   /*a=b*scale+c */
void mtrans(double **mA,double **mB, int m, int n); /*a=bT*/
void mscale(double **mA, double scale, double **mB, int m, int n); 
int mat_lu(int n,double **Ain,int **vP );
void mat_backsubs1( int n, double **Ain, double **bin, double **x, int **vP);
void mat_sol_nn(int n,double **Ain,double **bin, double **x);

void hh(int m, int n, double **H, double **Ain);
void backsubs(int m, int n, double **sln, double **HAin, double **Hb);
void hh_sln(int m, int n, double **sln, double **Ain, double **b);

void forsubs(int n, double **sln, double **mL, double **Hb);
void Cholesky (double **chout, double **W, int n);
void mat_sol_chol(int n,double **Ain,double **bin, double **x);
void Gerschgorin (double *bound, double **Ain, int n);
void ak(double **a_k, int n, int p, double **Wk, double **LkT,double **Hess,double **Jaco,double **dx0);
void Lk_dx0(double **L,double **x0,double **Cin,double **din,int p, int n);

void hh_sln(int m, int n, double **sln, double **Ain, double **b);

/******USER INPUT: The objective functions, constraints,  **********/
/********gradient, and HESSIAN given by users  ***********/

double FUNF(double **x){
  /* The objective function: dimension 1x1 */
double sum;

NUM_Z++;
return(sum);
}/* obj */

void JACOBIAN(int n,double **x,double **df)
{
/* Jacobian of FUNF:dimension nx1 */ 

NUM_DF++;
}

void HESSIAN(int n,double **x,double **hess){ 

NUM_H++;
}/* HESSIAN */

void FUNPHI(int q,int n,double **x,double **f)
{
  /* The function phi:dimension qx1  */ 
  f[0][0]=x[0][0]*x[0][0]+x[1][0]*x[1][0]-4;
  f[1][0]=x[0][0]*x[0][0]-x[1][0]*x[1][0]-1;
  f[2][0]=x[0][0]*x[0][0]-2.4*x[1][0];

NUM_F++;
}/*FUNPHI*/

void DPHIDX(int q,int n,double **x,double **df)
{
  /* The gradient of function phi:qxn  */
  df[0][0]=2.0*x[0][0];
  df[0][1]=2.0*x[1][0];

  df[1][0]=2.0*x[0][0];
  df[1][1]=-2.0*x[1][0];

  df[2][0]=2.0*x[0][0];
  df[2][1]=-2.4;

NUM_DF++;
}

void FUNH(int n, int ell, double **x, double **h)
{
  /* Conatraints ellxell */

h[0][0]=x[0][0]+x[1][0]-1.0;

NUM_G++;
}/*FUNH*/

void DHDX(int n, int ell, double **x, double **dh)
{
  /* The gradient of constraints: ellxn */

dh[0][0]=1.0;
dh[0][1]=1.0;



NUM_DG++;
}/*DHDX*/

/**********************************************************************/
/********************END USER INPUT***********************************/


main()
{
int i,j,n,q,ell;
double f_min,tp,cheb_a,cheb_h,xa,yb,**x_ini; 
double **phi,**dphi,**h,**dh;

double **z,**W;


n=N; /*number of variable */
ell=ELL; /*number of constraints */
q=Q; /*Dimension of phi */

W=matrix(q,q);
for(i=0;i<q;i++){
for(j=0;j<q;j++){
W[i][j]=0.0;
}
W[i][i]=1.0;
}

z=matrix(1,1);
x_ini=matrix(n,1);

/************USER INPUT: Initial Guess given by users***************/

x_ini[0][0]=0.1;
x_ini[1][0]=0.1;
           

/*******************END USER INPUT ***********************/

for (i=0;i<n;i++) { printf("x_initial(%i)=%f\n",i+1,x_ini[i][0]);}

/***********USER INPUT: The  Subroutine called by users *****************/
LSSCNL(z,x_ini,W,q,n,ell,0.0001,0.0001);
/*******************     END USER INPUT  ***********************/
phi=matrix(q,1);
dphi=matrix(q,n);
h=matrix(ell,1);
dh=matrix(ell,n);

/*FUNPHI(q,n,x_ini,phi);
DPHIDX(q,n,x_ini,dphi);
FUNH(n,ell,x_ini,h);
DHDX(n,ell,x_ini,dh);

for (i=0;i<q;i++) { printf("phi(%i)=%f\n",i+1,phi[i][0]);}
for (i=0;i<q;i++) {
  for (j=0;j<n;j++) { printf("dphi(%i)(%i)=%f\n",i+1,j+1,dphi[i][j]);}}

for (i=0;i<ell;i++) { printf("h(%i)=%f\n",i+1,h[i][0]);}
for (i=0;i<ell;i++) {
  for (j=0;j<n;j++) { printf("dh(%i)(%i)=%f\n",i+1,j+1,dh[i][j]);}} 
 
  */ 

for (i=0;i<n;i++) { printf("x_opt(%i)=%2.16f\n",i+1,x_ini[i][0]);} 
printf("f_min=%2.16f\n",z[0][0]);

if(x_ini[1][0]<0) printf("x_ini[1][0]<0\n");
if(x_ini[1][0]>0) printf("x_ini[1][0]>0\n");
if(x_ini[1][0]==0) printf("x_ini[1][0]=0\n");

free_matrix(W,q,q);
free_matrix(z,1,1);


printf("Number of objective function calls: %d \n",NUM_Z);

/*printf("Number of lesat-square f calls: %d \n",NUM_F);*/
printf("Number of Jacobian calls: %d \n",NUM_DF);  
printf("Number of Hessian calls: %d \n",NUM_H);  
printf("Number of Constraints calls: %d \n",NUM_G-1);
printf("Number of Constraint gradient calls: %d \n",NUM_DG);

}/*main*/

void LSSLS(double **vx, double **Ain,double **vb, int q, int n)
/* Unconstrained linear problems: minimum norm solutions for
   over- or derdetermined linear systems
   Ax=b; A:qxn q>n 

   n:    number of design variables 
   q:    dimension of function phi   
   vx:   design variables, an initial guess must be given, the optimum
         solution found will over write the initial values 
   Ain:  A q x n matrix 
   vb:   A q x 1 matrix
*/
{
    hh_sln(q,n,vx,Ain,vb);

}/*MNSLS*/

void MNSLS(double **vx, double **Cin,double **vd, int ell, int n)
/* Unconstrained linear problems: minimum norm solutions for
	underdetermined linear systems
     Cx=d; C:ellxn ell<=n 
   n:    number of design variables 
   ell:  number of constraints 
   vx:   design variables, an initial guess must be given, the optimum
         solution found will over write the initial values 
   Cin:  A ell x n matrix
   vd:   A ell x 1 matrix 
*/


{
  double **L;
  L=matrix(n,n-ell);
  Lk_dx0(L,vx,Cin,vd,ell,n); 
  free_matrix(L,n,n-ell);
}/*LSSLS*/


void LSSNLS(double **f_min,double **xk, double **W, int q,int n, double tol )
/*Unconstrained nonlinear problems
   n:    number of design variables  
   q:    dimension of function phi   
   xk:   design variables, an initial guess must be given, the optimum
         solution found will over write the initial values 
   W:    The weight function  
   tol:  Tolerance 
   The subroutine returns a value of the optimum objective function
   with f_min
   FUNPHI, and DPHIDX must be given.
*/
{
  int i,counter;
  double **dx,norm_dx;
  double **V,**VF,**Vf,**mVf,**F,**f,**ft,**Wf,**ftWf;
dx=matrix(n,1);
V=matrix(q,q);
VF=matrix(q,n);
Vf=matrix(q,1);
mVf=matrix(q,1);
F=matrix(q,n);
f=matrix(q,1);
ft=matrix(1,q);
Wf=matrix(q,1);
ftWf=matrix(1,1);

norm_dx=100.0;
counter=0;
  while (norm_dx>tol && counter<MAX_ITER)
  {
    Cholesky(V,W,q);
    FUNPHI(q,n,xk,f);
    DPHIDX(q,n,xk,F);
    mmult(VF,V,F,q,q,n);
    mmult(Vf,V,f,q,q,1);
    mscale(mVf,-1.0,Vf,q,1);
    LSSLS(dx,VF,mVf,q,n);
    /*    madd(xk,xk,1.0,dx,n,1); */  /* xk=xk+dx;*/ 
    madd(xk,xk,DAMPING_FACTOR,dx,n,1); 
    norm_dx=sqrt(vdot(dx,dx,n));
    counter++;
    if (counter>=MAX_ITER)
      {
	printf("Exceeds Maximum number of iterations (%d) in LSSNLS\n",MAX_ITER); 
      }
  }

  FUNPHI(q,n,xk,f);
  mmult(Wf,W,f,q,q,1);
  mtrans(ft,f,q,1);
  mmult(ftWf,ft,Wf,1,q,1);
  f_min[0][0]=0.5*ftWf[0][0];
  printf("Number of iterations in LSSNLS: %d\n",counter);

free_matrix(dx,n,1);
free_matrix(V,q,q);
free_matrix(VF,q,n);
free_matrix(Vf,q,1);
free_matrix(mVf,q,1);
free_matrix(F,q,n);
free_matrix(f,q,1);
free_matrix(ft,1,q);
free_matrix(Wf,q,1);
free_matrix(ftWf,1,1);

}/* LSSNLS*/


void LSSCLS(double **f_min,double **vx, double **W, double **Ain, double
	    **vb, double **Cin, double **vd,int q, int n, int ell)
/* Constrained Linear Problems  
   Solve the least square problem Ax=b 
   subject to Cx=d 

   n:    number of design variables 
   q:    dimension of function phi   
   ell:  number of constraints 
   vx:   design variables, an initial guess must be given, the optimum
         solution found will over write the initial values 
   W:    The weight function   
   Ain:  A q x n matrix 
   vb:   A q x 1 matrix
   Cin:  A ell x n matrix
   vd:   A ell x 1 matrix 
   The subroutine returns a value of the optimum objective function
   with f_min
*/

{
  int i,j;
  double **x0,**xu,**u,**L,**V,**VA,**VAL;
  double **Ax0,**bAx0,**vbAx;
  double **f,**ft,**Wf,**ftWf;

x0=matrix(n,1);
xu=matrix(n,1);
u=matrix(n-ell,1);
L=matrix(n,n-ell);
V=matrix(q,q);
VA=matrix(q,n);
VAL=matrix(q,n-ell);
Ax0=matrix(q,1);
bAx0=matrix(q,1);
vbAx=matrix(q,1);
f=matrix(q,1);
ft=matrix(1,q);
Wf=matrix(q,1);
ftWf=matrix(1,1);

  Cholesky(V,W,q);
  Lk_dx0(L,x0,Cin,vd,ell,n);
  mmult(VA,V,Ain,q,q,n);
  mmult(VAL,VA,L,q,n,n-ell);

  mmult(Ax0,Ain,x0,q,n,1);
  madd(bAx0,vb,-1.0,Ax0,q,1);
  mmult(vbAx,V,bAx0,q,q,1);

  /*  if(q> (n-ell)){
    LSSLS(u,VAL,vbAx,q,n-ell);}
  else{
    MNSLS(u,VAL,vbAx,q,n-ell);}*/
  /*printf("q=%i,ell=%i\n\n",q,n-ell);*/
 LSSLS(u,VAL,vbAx,q,n-ell);
  mmult(xu,L,u,n,n-ell,1);
  madd(vx,x0,1.0,xu,n,1);

  mmult(Ax0,Ain,vx,q,n,1);
  madd(f,Ax0,-1.0,vb,q,1);
  mmult(Wf,W,f,q,q,1);
  mtrans(ft,f,q,1);
  mmult(ftWf,ft,Wf,1,q,1);
  f_min[0][0]=0.5*ftWf[0][0];

free_matrix(x0,n,1);
free_matrix(xu,n,1);
free_matrix(u,n-ell,1);
free_matrix(L,n,n-ell);
free_matrix(V,q,q);
free_matrix(VA,q,n);
free_matrix(VAL,q,n-ell);
free_matrix(Ax0,q,1);
free_matrix(bAx0,q,1);
free_matrix(vbAx,q,1);
free_matrix(f,q,1);
free_matrix(ft,1,q);
free_matrix(Wf,q,1);
free_matrix(ftWf,1,1);
}/*LSSCLS*/


void LSSCNL(double **f_min, double **xk, double **W, int q,int n,int
	    ell,double tol1, double tol2) 
{ 
/*Constrained nonlinear Problems*/
/*  n:    number of design variables 
    q:    dimension of function phi   
    ell:  number of constraints 
    xk:   design variables, an initial guess must be given, the optimum
              solution found will over write the initial values 
    W:    The weight function   
    tol1: tolerance for delta_x 
    tol2: tolerance for delta_g
 
    The subroutine returns a value of the optimum objective function
    with f_min
    FUNPHI, DPHIDX, FUNH, and DHDX must be given.
*/

  int counter,i;
  double **dx,norm_dx=100.0,norm_g=100.0;
  double **V,**VF,**Vf,**mVf,**F,**f,**G,**g;
  double **mf,**mg,**ft,**Wf,**ftWf;
  counter=0;

dx=matrix(n,1);
V=matrix(q,q);
VF=matrix(q,n);
Vf=matrix(q,1);
mVf=matrix(q,1);
F=matrix(q,n);
f=matrix(q,1);
G=matrix(ell,n);
g=matrix(ell,1);
mf=matrix(q,1);
mg=matrix(ell,1);
ft=matrix(1,q);
Wf=matrix(q,1);
ftWf=matrix(1,1);

while (norm_dx>tol1 || norm_g>tol2 && counter<MAX_ITER)
  {
    Cholesky(V,W,q);
    FUNPHI(q,n,xk,f);
    DPHIDX(q,n,xk,F);
    FUNH(n,ell,xk,g);
    DHDX(n,ell,xk,G);
    mscale(mf,-1.0,f,q,1);
    mscale(mg,-1.0,g,ell,1);

    LSSCLS(f,dx,W,F,mf, G, mg,q,n,ell);

    /*  for(i=0;i<n;i++){
    printf("dx(%i)=%f \n",i+1,dx[i][0]);
    }*/

    madd(xk,xk,DAMPING_FACTOR,dx,n,1);  
    norm_dx=sqrt(vdot(dx,dx,n));
    norm_g=sqrt(vdot(g,g,ell));

    printf("norm_dx=%2.15f norm_g=%2.15f  \n",norm_dx,norm_g);
    counter++;

    if (counter>=MAX_ITER)
      {
	printf("Exceeds Maximum number of iterations (%d) in LSSCNL\n",MAX_ITER); 
      }
  }
  FUNPHI(q,n,xk,f);
 
  ;
printf("Number of iterations in LSSCNL: %d\n",counter);

free_matrix(dx,n,1);
free_matrix(V,q,q);
free_matrix(VF,q,n);
free_matrix(Vf,q,1);
free_matrix(mVf,q,1);
free_matrix(F,q,n);
free_matrix(f,q,1);
free_matrix(G,ell,n);
free_matrix(g,ell,1);
free_matrix(mf,q,1);
free_matrix(mg,ell,1);
free_matrix(ft,1,q);
free_matrix(Wf,q,1);
free_matrix(ftWf,1,1);

}/*LSSCNL*/



double ARBITRARY (int n, int ell, double **xold, double epsilon1,
		  double epsilon2) {
/*========Subroutine for an arbitrary objective function =====*/
/*  n:        number of design variables 
    ell:      number of constraints 
    xold:     design variables, an initial guess must be given, the optimum
              solution found will over write the initial values 
    epsilon1: tolerance for delta_x 
    epsilon2: tolerance for delta_g
 
    The subroutine returns a value of the optimum objective function
    with f_min
    FUNF, JACOBIAN, HESSIAN, FUNH, and DHDX must be given.
*/

int i,j,k,iter;
double f_min,mu,tp;
double **Gv,**gv,**Wk2,**delta_x,**xnew,**a_k,**Wk;
double **Lk,**hess,**jaco,**mgv,**dx0,**eye;
double lower,upper;
double **Vk,**Lkt,**LtH,**LtHL,**du_k,**Lk_ti_du_k;
double norm_H,bound[3],tol1,tol2,*s_part,**LkT,**check7; 

Gv=matrix(ell,n);
gv=matrix(ell,1);
Wk2=matrix(n,n);
delta_x=matrix(n,1);
xnew=matrix(n,1);
a_k=matrix(n-ell,1);
Wk=matrix(n,n);
Lk=matrix(n,n-ell);
LkT=matrix(n-ell,n);
LtH=matrix(n-ell,n);
LtHL=matrix(n-ell,n-ell);
hess=matrix(n,n);
jaco=matrix(n,1);
dx0=matrix(n,1);
mgv=matrix(ell,1);
eye=matrix(n,n);
Vk=matrix(n,n);

du_k=matrix(n-ell,1);
Lk_ti_du_k=matrix(n,1);


for (i=0;i<n;i++) {delta_x[i][0]=0.0;}

iter=1;
tol1=100.0;
tol2=100.0;

JACOBIAN(n,xold,jaco); 
DHDX(n,ell,xold,Gv);
FUNH(n,ell,xold,gv); 

while (tol1>epsilon1 | tol2>epsilon2)  { 
for (i=0;i<n;i++) {
for (j=0;j<n;j++) {   
hess[i][j]=0.0;}}

HESSIAN(n,xold,hess);

mscale(mgv,-1.0,gv,ell,1); 
Lk_dx0(Lk,dx0,Gv,mgv,ell,n); 
/*for (i=0;i<n;i++) {
  printf("dx0(%d)=%f\n",i+1,dx0[i][0]);}*/
Gerschgorin(bound,hess,n); 
lower=bound[0];

printf("lower=%f upper=%f bandwidth=%f \n",lower,bound[1],bound[1]-lower);

 if (lower==0.0) {

 for(i=0;i<n;i++){
  for(j=0;j<n;j++){
  if(i==j)  Wk[i][j]=hess[i][j]+MU2;
  else Wk[i][j]=hess[i][j]; }}
}
if (lower>0.0) {
  mat_copy(Wk,hess,n,n);
}

if (lower<0.0) {
mu=MU;
tp=mu*lower;
  for(i=0;i<n;i++){
  for(j=0;j<n;j++){
  if(i==j)    Wk[i][j]=hess[i][j]-tp;
  else Wk[i][j]=hess[i][j]; }}

}  
/*for (i=0;i<n;i++) {
for (j=0;j<n-ell;j++) {   
  printf("Lk(%d,%d)=%f\n",i+1,j+1,Lk[i][j]);}}*/
mtrans(LkT,Lk,n,n-ell);
mmult(LtH,LkT,Wk,n-ell,n,n);
mmult(LtHL,LtH,Lk,n-ell,n,n-ell);
/*for (i=0;i<n-ell;i++) {
for (j=0;j<n-ell;j++) {   
printf("LtHL(%d,%d)=%f\n",i+1,j+1,LtHL[i][j]);}}*/
ak(a_k,n,ell,LtHL,LkT,hess,jaco,dx0);
/*for (i=0;i<n-ell;i++) {printf("a_k(%d)=%f\n",i+1,a_k[i][0]);}*/ 
/*a_k=-du_k*/
mmult(Lk_ti_du_k,Lk,a_k,n,n-ell,1);
madd(delta_x,dx0,-1.0,Lk_ti_du_k,n,1);
madd(xnew,xold,1.0,delta_x,n,1);

/*for (i=0;i<n;i++) {printf("xnew(%d)=%f\n",i+1,xnew[i][0]);} */

JACOBIAN(n,xnew,jaco);
DHDX(n,ell,xnew,Gv);
FUNH(n,ell,xnew,gv);

mat_copy(xold,xnew,n,1);
iter=iter+1;
tol1=sqrt(vdot(delta_x,delta_x,n));
tol2=sqrt(vdot(gv,gv,ell));
printf("tol1=%f\t tol2=%f\n\n",tol1,tol2); 
} /*while*/

f_min=FUNF(xnew);


printf("f_min=%f \n",f_min);

printf("\n Number of iterations :%d\n",iter-1);
/*************Check normality condition************/
/*printf("\nNormality Condition:\n");
HESSIAN(n, xnew,hess);
JACOBIAN(n,xnew,jaco);
DHDX(n,ell,xnew,Gv); 
FUNH(n,ell,xnew,gv); 
mscale(mgv,-1.0,gv,ell,1); 
Lk_dx0(Lk,dx0,Gv,mgv,ell, n); 
LkT=matrix(n-ell,n);
check7=matrix(n-ell,1);
mtrans(LkT,Lk,n,n-ell); 
mmult(check7, LkT,jaco, n-ell,n,1);
for (i=0;i<n-ell;i++) {printf("\n Check[%d]=%f\n",i,check7[i][0]);}
free_matrix(LkT,n-ell,n);
free_matrix(check7,n-ell,1);*/
/*************END: normality condition************/

free_matrix(Gv,ell,n);
free_matrix(gv,ell,1);
free_matrix(Wk2,n,n);
free_matrix(delta_x,n,1);
free_matrix(xnew,n,1);
free_matrix(a_k,n,1);
free_matrix(Wk,n,n);
free_matrix(Lk,n,n-ell);
free_matrix(hess,n,n);
free_matrix(jaco,n,1);
free_matrix(dx0,n,1);
free_matrix(mgv,ell,1);
free_matrix(eye,n,n);
free_matrix(Vk,n,n);
free_matrix(LkT,n-ell,n);
free_matrix(LtH,n-ell,n);
free_matrix(LtHL,n-ell,n-ell);
free_matrix(du_k,n-ell,1);
free_matrix(Lk_ti_du_k,n,1);

return(f_min);
} /*ARBITRARY*/



/********************Matrix Operation Subroutines **********************/

double **matrix(long nrow,long ncol)
{
long i,nrl=0,ncl=0,nrh=nrow+nrl-1,nch=ncol+ncl-1;
double **m;
/*allocate pointers to rows*/
m=(double **)malloc((size_t)((nrow+NR_END)*sizeof(double*)));
if (!m) nrerror("allocation failure 1 in matrix()");
m +=NR_END;
m -=nrl;
/*allocate rows and set pointers to them*/
m[nrl]=(double *)malloc((size_t)((nrow*ncol+NR_END)*sizeof(double)));
if (!m[nrl]) nrerror("allocation failure 2 in matrix()");
m[nrl] +=NR_END;
m[nrl] -=ncl;

for(i=nrl+1;i<=nrh;i++) m[i]=m[i-1]+ncol;
/* return pointer to array of pointers to rows*/
return m;

}/* matrix */

void free_matrix(double **m, long nrow,long ncol)
{
long nrl=0,ncl=0;
  free((FREE_ARG)(m[nrl]+ncl-NR_END));
  free((FREE_ARG)(m+nrl-NR_END));
}/* free_matrix */

void nrerror(char error_text[])
{
fprintf(stderr,"Run time error\n");
fprintf(stderr,"%s\n",error_text);
fprintf(stderr,"Exit the system\n");
exit(1);

}/* nrerror */


int **matrix_i(long nrow,long ncol)
{
long i,nrl=0,ncl=0,nrh=nrow+nrl-1,nch=ncol+ncl-1;
int **m;
/*allocate pointers to rows*/
m=(int **)malloc((size_t)((nrow+NR_END)*sizeof(int*)));
if (!m) nrerror("allocation failure 1 in matrix()");
m +=NR_END;
m -=nrl;
/*allocate rows and set pointers to them*/
m[nrl]=(int *)malloc((size_t)((nrow*ncol+NR_END)*sizeof(int)));
if (!m[nrl]) nrerror("allocation failure 2 in matrix()");
m[nrl] +=NR_END;
m[nrl] -=ncl;

for(i=nrl+1;i<=nrh;i++) m[i]=m[i-1]+ncol;
/* return pointer to array of pointers to rows*/
return m;

}/* matrix_i */

void free_matrix_i(int **m, long nrow,long ncol)
{
long nrl=0,ncl=0;
  free((FREE_ARG)(m[nrl]+ncl-NR_END));
  free((FREE_ARG)(m+nrl-NR_END));
}/* free_matrix_i */



/*=============================== I matrix ============================*/
void I_mat(double **eye_mat, int n) {
int i,j;
for(i=0;i<n;i++) {
for(j=0;j<n;j++) {
eye_mat[i][j]=0.0;}
eye_mat[i][i]=1.0;}
} /* eye */
/*============================ mat_copy =============================*/
void mat_copy(double **mA,double **mB, int m, int n) {
int i,j;
for(i=0;i<m;i++) {
for(j=0;j<n;j++) {
mA[i][j]=mB[i][j];}}

}/*mat_copy*/
/********************************* vdot() *******************************/
  /*   Vector dot product */
double vdot(double **a,double **b, int n)
 
{
 int i; 
 double result=0.0;
 for (i=0; i<n; i++) { 
 result += a[i][0]*b[i][0] ;
 }
 return(result);
}

/********************************* madd() *********************************
   addition or subtraction of two matrices
*/   
void madd(double **mA, double **mB, double scale, double **mC, int m, int n)
{
int i,j; 

for(i=0;i<m;i++){
for(j=0;j<n;j++){
  mA[i][j]=mB[i][j]+scale*mC[i][j];}}
}/* madd */
/********************************* mtrans() *********************************
   transpose of a matrix
*/
void mtrans(double **mAT,double **mA, int m, int n)
{
int i,j; 

for(i=0;i<n;i++){
for(j=0;j<m;j++){
  mAT[i][j]=mA[j][i];}}

}/* mtrans */
/********************************* mmult() *********************************
   Matrix multiplication of a matrix
*/  /*checked !!*/
/*a=b*c*/
void mmult(double **mA,double **mB,double **mC, int Num_Row,int
               Num_Iter, int Num_Column) 
{
int I,J,K;
        for (I=0; I<Num_Row; I++)
        for (J=0; J<Num_Column; J++)
        for (K=0, mA[I][J]=0.0; K<Num_Iter; K++)
                {
                mA[I][J] += mB[I][K] * mC[K][J];
                }

}/*mmult2*/


/********************************* mscale() *********************************
   Scaler multiplication of a matrix
*/
void mscale(double **mA, double scale, double **mB, int m, int n)
{
 int i,j; 
for(i=0;i<m;i++){
for(j=0;j<n;j++){
  mA[i][j]=scale*mB[i][j];}}

}/* mscale */
/*=========================  LU Decomposition  ========================*/

int mat_lu(int n,double **Ain,int **vP )
{
  int	i, j, k;
  int	maxi, tmp;
  double c, c1;
  int	p;

  for (p=0,i=0; i<n; i++)
    {
      vP[i][0] = i;
    }

  for (k=0; k<n; k++)
    {
      /*--- partial pivoting ---*/
      for (i=k, maxi=k, c=0.0; i<n; i++)
	{
	  c1 = fabs( Ain[vP[i][0]][k] );
	  if (c1 > c)
	    {
	      c = c1;
	      maxi = i;
	    }
	}

      /*row exchange, update permutation vector*/
      if (k != maxi)
	{
	  p++;
	  tmp = vP[k][0];
	  vP[k][0] = vP[maxi][0];
	  vP[maxi][0] = tmp;
	}

      /* suspected singular matrix */
      if ( Ain[vP[k][0]][k] == 0.0 )
	return (-1);

      for (i=k+1; i<n; i++)
	{
	  /* --- calculate m(i,j) --- */
	  Ain[vP[i][0]][k] = Ain[vP[i][0]][k] / Ain[vP[k][0]][k];
		
	  /*--- elimination ---*/
	  for (j=k+1; j<n; j++)
	    {
	      Ain[vP[i][0]][j] -= Ain[vP[i][0]][k] * Ain[vP[k][0]][j];
	    }
	}
    }
return (p);
} /* mat_lu */

void mat_backsubs1( int n, double **Ain, double **bin, double **x, int **vP) 
{
  int i, j, k;
  double  sum;

  for (k=0; k<n; k++)
    {
      for (i=k+1; i<n; i++)
	bin[vP[i][0]][0] -= Ain[vP[i][0]][k] * bin[vP[k][0]][0];
    }

  x[n-1][0] = bin[vP[n-1][0]][0] / Ain[vP[n-1][0]][n-1];
  for (k=n-2; k>=0; k--)
    {
      sum = 0.0;
      for (j=k+1; j<n; j++)
	{
	  sum += Ain[vP[k][0]][j] * x[j][0];
	}
      x[k][0] = (bin[vP[k][0]][0] - sum) / Ain[vP[k][0]][k];
    }
}/* mat_backsubs1 */

void mat_sol_nn(int n,double **Ain,double **bin, double **x) {
int **vP/*,i,j*/;
double **mA;
vP=matrix_i(n,1);
mA=matrix(n,n);
mat_copy(mA,Ain,n,n);
mat_lu( n, mA, vP );
mat_backsubs1(n, mA, bin, x, vP); 
free_matrix(mA,n,n);
free_matrix_i(vP,n,1);
}/* mat_sol_nn */
/*===================== forward substitution ============================*/
void forsubs(int n, double **sln, double **mL, double **Hb){

int i,j,k;
double sum;
for (i=0;i<n;i++){
  sln[i][0]=0.0;}


for (i=0;i<n;i++) {  
  sum=0.0;
   for (k=0;k<i;k++) { /*amy*/
    sum=sum+mL[i][k]*sln[k][0]; /*intf("sum=%f\n",sum);*/
   }
   sln[i][0]=(Hb[i][0]-sum)/mL[i][i]; 
}/*j*/

}/*forsubs*/

/* ===================== Cholesky ===================== */
void Cholesky (double **Vout, double **W, int n)
{
int i,j, k, p;
double sum1,sum2,**V;


V=matrix(n,n);
for (i=0;i<n; i++){
for (j=0;j<n; j++){
V[i][j]=0.0;
}}

for (k=0;k<n;k++){
  sum1=0.0; 
    for (p=0;p<=k-1;p++) {
    sum1=sum1+V[k][p]*V[k][p];}
  V[k][k]=sqrt(W[k][k]-sum1);
   for (i=k+1;i<n;i++){  /*amy*/
  sum2=0.0;
  for (p=0;p<=k-1;p++) {
     sum2=sum2+V[i][p]*V[k][p]; }
  V[i][k]=(W[i][k]-sum2)/V[k][k];}
}/*k*/

mtrans(Vout,V,n,n);
free_matrix(V,n,n);
} /* Cholesky */
void mat_sol_chol(int n,double **Ain,double **bin, double **x) {
int i,j;
double **mV,**mVT,**y;
mV=matrix(n,n);
mVT=matrix(n,n);
y=matrix(n,1);

Cholesky(mV,Ain,n);
mtrans(mVT,mV,n,n);
/*for(i=0;i<n;i++)   {
for(j=0;j<n;j++)   {
  printf("Ain(%d,%d)=%f\n",i+1,j+1,Ain[i][j]);
}}
for(i=0;i<n;i++)   {
for(j=0;j<n;j++)   {
  printf("mV(%d,%d)=%f\n",i+1,j+1,mV[i][j]);
}}

for(j=0;j<n;j++)   {
  x[j][0]=1.0;printf("herebin(%d)=%f\n",j+1,bin[j][0]); 
}*/
forsubs(n,y,mVT,bin);
backsubs(n,n,x,mV,y);
/*for(j=0;j<n;j++)   {
  printf("herex(%d)=%f\n",j+1,x[j][0]); 
}*/
free_matrix(mV,n,n);
free_matrix(mVT,n,n);
free_matrix(y,n,1);
}/* mat_sol_chol */


/*==========================  Gerschgorin ============================*/
/* Gerschgorin: The Matrix has to be square.*/
void Gerschgorin (double *bound, double **Ain, int n) {
double sign,**v_lower,**v_upper,**r,lower,upper;
int i,j;

v_lower=matrix(n,1);
v_upper=matrix(n,1);
r=matrix(n,1);


for (i=0;i<n;i++){ 
v_lower[i][0]=0.0; 
v_upper[i][0]=0.0;}


  for (i=0;i<n;i++){
    r[i][0]=0.0;
    for (j=0;j<n;j++){
      if (j!=i) {
	if (Ain[i][j]>=0.0) sign=1.0;
	else sign=-1.0;
	r[i][0]=r[i][0]+sign*(Ain[i][j]);}
	    }/*j*/
    v_lower[i][0]=Ain[i][i]-r[i][0];
    v_upper[i][0]=Ain[i][i]+r[i][0];
  }/*i*/

  lower=v_lower[0][0];
  upper=v_upper[0][0];
  for (i=0;i<n;i++){
    if (v_lower[i][0]<lower)  {lower=v_lower[i][0];}
    if (v_upper[i][0]>upper)  {upper=v_upper[i][0];}
  }/*i*/
bound[0]=lower;
bound[1]=upper;
bound[2]=upper-lower;

free_matrix(v_lower,n,1);
free_matrix(v_upper,n,1);
free_matrix(r,n,1);

}/* Gerschgorin */


/*============================ ak ===================================*/

void ak(double **a_k, int n, int p, double **Wk,double **LkT,double
	**Hess,double **Jaco,double **dx0)  
{ 
double **tp1,**b,**Hdx0;
int i,j;
tp1=matrix(n,1);
b=matrix(n-p,1);
Hdx0=matrix(n,1);
mmult(Hdx0,Hess,dx0,n,n,1);
madd(tp1, Hdx0, 1, Jaco, n, 1);
mmult(b,LkT,tp1,n-p,n,1);
mat_sol_chol(n-p,Wk,b,a_k);
/*for (i=0;i<n-p;i++){    printf("b(%d)=%f\n",i+1,b[i][0]);}
for (i=0;i<n-p;i++) {
  for (j=0;j<n-p;j++) {printf("Wk(%d,%d)=%f\n",i+1,j+1,Wk[i][j]);}}
for (i=0;i<n-p;i++)  {    printf("a_k(%d)=%f\n",i+1,a_k[i][0]);}*/ 

free_matrix(tp1,n,1);
free_matrix(b,n-p,1);
free_matrix(Hdx0,n,1);



}/*ak*/


/* ===================== Lk_dx0 ========================*/
void Lk_dx0(double **L,double **x0,double **Cin,double **din,int p, int n)
{

int np,i,j;

double **H,**Ht,**Ct,**E,**C,**Hcp,**Up,**Upt,**y,**d,**eye_m;

np=n-p; 
H=matrix(n,n);
Ht=matrix(n,n);
C=matrix(p,n);
Ct=matrix(n,p);
E=matrix(n,np);
Hcp=matrix(n,p);
Up=matrix(p,p);
Upt=matrix(p,p);
y=matrix(n,1);
d=matrix(p,1);
eye_m=matrix(np,np);

mat_copy(C,Cin,p,n);
mat_copy(d,din,p,1);

for (i=0;i<n;i++){
   x0[i][0]=0.0;
  for (j=0;j<np;j++){
    L[i][j]=0.0;}}/*L:nxnp*/

mtrans(Ct,C,p,n); /*C:p*n*/
hh(n,p,H,Ct); /*H:nxn*/ 

I_mat(eye_m, np);

for (i=0;i<p;i++) {
  for (j=0;j<np;j++) {
    E[i][j]=0.0;
  }}

for (i=0;i<np;i++) {
  for (j=0;j<np;j++) {
    E[p+i][j]=eye_m[i][j];}}
    
mtrans(Ht,H,n,n);
mmult(L,Ht,E,n,n,np); /*L:nxnp*/
mmult(Hcp,H,Ct,n,n,p); /*Hcp:nxp*/

for (i=0;i<p;i++) {
  for (j=0;j<p;j++) {
    Up[i][j]=Hcp[i][j];}}

mtrans(Upt,Up,p,p);

mat_sol_nn(p,Upt,d,y);
for (i=p;i<n;i++) { y[i][0]=0.0;}
mmult(x0,Ht,y,n,n,1);

free_matrix(H,n,n);
free_matrix(Ht,n,n);
free_matrix(C,p,n);
free_matrix(Ct,n,p);
free_matrix(E,n,np);
free_matrix(Hcp,n,p);
free_matrix(Up,p,p);
free_matrix(Upt,p,p);
free_matrix(y,n,1);
free_matrix(d,p,1);
free_matrix(eye_m,np,np);

}
/*===================================================================*/


/*======================== Householder:matrix =======================*/
/* overdetermined system m>n */
void hh(int m, int n, double **H, double **Ain) {
int i,j,k;
double **u,**a,**alpha,**beta;
double sign_ak,dot_akm,**up,**upb,**eye;
double **Hk,**Ht,**A,**At,**ut;

u=matrix(m,1);
ut=matrix(1,m);
a=matrix(m,1);
alpha=matrix(m,1);
beta=matrix(m,1);
A=matrix(m,n);
At=matrix(m,n); /* not A^T !! */
eye=matrix(m,m);
Hk=matrix(m,m); 
Ht=matrix(m,m); /* not H^T !! */
up=matrix(m,m); 
upb=matrix(m,m); 


mat_copy(A,Ain,m,n);
I_mat(eye,m);
I_mat(H,m);

for (i=0;i<m;i++) {
  u[i][0]=0.0; }  /*u:mx1*/

 for (k=0;k<n;k++) {
    for (i=0;i<m;i++) {a[i][0]=A[i][k];}
 if (a[k][0]>=0.0) sign_ak=1.0;
  else  sign_ak=-1.0;
 dot_akm=0.0;
   for (j=k;j<m;j++){
    dot_akm=dot_akm+a[j][0]*a[j][0];} 

   alpha[k][0]=sign_ak*sqrt(dot_akm);
  for (j=0;j<k;j++) {
    u[j][0]=0.0;}
  u[k][0]=a[k][0]+alpha[k][0];

  for (j=k+1;j<m;j++) {
    u[j][0]=a[j][0];}

  

  beta[k][0]=alpha[k][0]*u[k][0]; 
  mtrans(ut,u,m,1); 
  mmult(up,u,ut,m,1,m); /*u=ut*/

  mscale(upb,1.0/beta[k][0],up,m,m);
  madd(Hk,eye,-1.0,upb,m,m);

  for (i=0;i<m;i++) {
    for (j=0;j<m;j++) {
      Ht[i][j]=H[i][j];}} /* Ht is not H^T !! */
  for (i=0;i<m;i++) {
    for (j=0;j<n;j++) {
      At[i][j]=A[i][j];}} /* At is not H^T !! */
  mmult(H,Hk,Ht,m,m,m);
  mmult(A,Hk,At,m,m,n); /* VIP !! Update A in each loop */

}/*k*/

free_matrix(u,m,1);
free_matrix(ut,1,m);
free_matrix(a,m,1);
free_matrix(alpha,m,1);
free_matrix(beta,m,1);
free_matrix(A,m,n);
free_matrix(At,m,n); /* not A^T !! */
free_matrix(eye,m,m);
free_matrix(Hk,m,m); 
free_matrix(Ht,m,m); /* not H^T !! */
free_matrix(up,m,m); 
free_matrix(upb,m,m); 

} /*hh*/		       
/*===================================================================*/
/*===================== Backsubstitution ============================*/
void backsubs(int m, int n, double **sln, double **HAin, double **Hb){
int i,j,k;
double sum;
for (i=0;i<n;i++){
  sln[i][0]=0.0;}
for (j=0;j<n;j++) {
  i=n-1-j;
  sum=0.0;
   for (k=i+1;k<n;k++) { /*amy*/
    sum=sum+HAin[i][k]*sln[k][0]; /*printf("sum=%f\n",sln[k]);*/
}
  sln[i][0]=(Hb[i][0]-sum)/HAin[i][i]; 
}/*j*/

}/*backsubs*/
/*======================== Householder:sln (m>n only )=============*/
void hh_sln(int m, int n, double **sln, double **Ain, double **b) {
double **H,**HAin,**Hb;
int i,j;
H=matrix(m,m);
HAin=matrix(m,n);
Hb=matrix(m,1);

hh( m, n,  H,  Ain);
mmult(HAin,H,Ain,m,m,n);
mmult(Hb,H,b,m,m,1);


/*for(i=0;i<m;i++){
for(j=0;j<n;j++){

printf("Ain(%i,%i)=%2.12f\n",i+1,j+1,Ain[i][j]);
}}

for(i=0;i<m;i++){
printf("b(%i,1)=%2.12f\n",i+1,b[i][0]);
}

for(i=0;i<n;i++){
printf("Hb[%i]=%2.12f",i+1,Hb[i][0]);
}*/


backsubs(m,n, sln, HAin, Hb);


free_matrix(H,m,m);
free_matrix(HAin,m,n);
free_matrix(Hb,m,1); 

}/* Householder:sln */



