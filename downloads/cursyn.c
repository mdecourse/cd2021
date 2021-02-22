/*************************************************************************/
/**  CURSYN: A software package for curve synthesis, based on           **/
/**      non-parametric cubic splines. Author: Chin-Pun Teng, 2002.     **/
/**    * This code calls the    "ARBITRARY" subroutine of ODA.          **/
/**      Matrices here are represented by vector arrays                 **/
/**      For example, a mXn matrix is a vector of m*n entries.          **/
/**																		**/
/** * Users are required to define their own constraints in fuction g(.)**/ 
/**   and input their first-order derivatives in function G(.).         **/
/** * In the example included here, there are two equality constraints, **/
/**   the curvatures at the two ends, which are set equal to zero. Users**/
/**   can add more contraints, e.g.   the commented contraint three,    **/
/**   which specifies a supporting point of s[10]=92.5.                 **/
/** * The code was modified and validated with the example included by  **/
/**   Shaoping Bai (mspbai@cim.mcgill.ca) On 2004.   Any  feedback on   **/
/**   the programm is appreaciated.                                     **/
/*************************************************************************/


#include "stdio.h"
#include "math.h"
#include "time.h"
//#include <sys/resource.h>

#define SGN(a) (a<=0 ? -(1.) : (1.))
#define RUSAGE_SELF      0         /* calling process */


int I,J,K,N_var; 
#define X          0
#define Y          1
#define Z          2
#define ALL_COLUMNS    (I=0; I<Num_Column; I++)
#define ALL_ROWS       (J=0; J<Num_Row; J++)
#define TINY 1.0e-20;

/* BEGIN USE INPUT */
#define N_spts 30 //total supporting points
#define N_var 28 //number of design variables, N_var=N_spts-2
#define N_consts 2  //number of constraints

#define rho1 90.3009  //radii of starting blending point
#define rhon 76.4477  //radii of end blending point
 
#define ANGLE1 0.1333// the angle of rho1 and x axis
#define ANGLE2 0.1576// the angle of rhon and y axis


/* END USER INPUT */

#define Wi 1.0
#define We 1.0
#define Wj 0.1
#define M_PI 3.14159265	



#define ARRAY_SIZE1 100				//							
#define MATRIX_SIZE1 10000			//    THESE CONSTANTS CAN BE ADJUSTED ACCORDING
#define TOLERANCE1 0.001			//    TO YOUR REQUIREMENTS IN SPECIFYING
#define TOLERANCE2 0.001			//	  CALCULATION ACCURACY		
#define STEP_SIZE 0.3				//

/*#define cst 1.0*/



double *I_mat(double *eye_mat, int n);
void mat_copy(double *mA,double *mB, int m, int n);
double *mmult(double *a, double *b, double *c, int Num_Row,int
	      Num_Iter, int Num_Column); /* a=bxc*/
double *madd(double *a, double *b, double scale, double *c, int
	     Num_Row, int Num_Column);   /*a=b*scale+c */
double *vadd(double *a,double *b,double scale,double *c,int Num_Row);
double *mtrans(double *a,double *b, int Num_Row, int Num_Column); /*a=bT*/
double vdot( double *a,double *b, int Num_Row);
double *vscale(double *a, double scale, double *b, int Num_Row);
double *mscale(double *a, double scale, double *b, int Num_Row, int
	       Num_Column); 
double maximum_norm(double *Ain, int Num_Row, int Num_Column);


/* determined system m=n */
int mat_lu(int n,double *Ain,int *P );
double *mat_backsubs1( int n, double *Ain, double *bin, double *theta, int
		       *P); 
double *mat_sol_nn(int n,double *Ain,double *bin, double *theta);

/* overdetermined system m>n */
void hh(int m, int n, double *H, double *Ain);
double *backsubs(int m,int n, double *sln, double *HAin, double *Hb);
double *hh_sln(int m, int n, double *sln, double *Ain, double *b);

/*====================================================================*/
double *Cholesky (double *chout, double *Wt, int n); 
double ARBITRARY ( int n, int p, double *xold, double epsilon);
double *Gerschgorin (double *bound, double *Ain, int n);
double *ak(double *a_k, int n, int p, double *Wk,double *Hess,double *Jaco,double *dx0);
void Lk_dx0(double *L,double *x0,double *C,double *d,int p, int n);


void vspp(double *s);
void matrix_A(double *mA);
void matrix_B(double *mB, double ang1, double ang2);
void matrix_Ainv_B(double *mA,double *mB, double *mANS, int m);

void matrix_E(double *mE,double ang1, double ang2);
void matrix_F(double *mF);



void spline ( double *Ak,double *Bk,double *Ck,double *Dk,double *s);
double z(double *des_var);
double D_obj(int i, int j,double y,double yp,double ypp);
double DD_obj(int i,int j,int k,double y,double yp,double ypp);
double *Jacobian(double *jaco, double *des_var);
double *Hessian(double *hess, double *des_var);
double *g(double *gv,double *des_var);
double *G(double *Gv,double *des_var);
int getrusage(int who, struct rusage *rusage);

double A[N_spts*N_spts],B[N_spts*N_spts],Ain_B[N_spts*N_spts];
double E[N_spts*N_spts],F[N_spts*N_spts],Ein_F[N_spts*N_spts];
double theta[N_spts]/*theta*/,delta_theta;
double Ak[N_spts-1],Bk[N_spts-1],Ck[N_spts-1],Dk[N_spts-1];
double spp[N_spts],kappa[N_spts];
double s[N_spts],constr[N_var],cst;
double des_var[N_var];
int total_iter;
main()
{

int i,j,n,p;
double z_min,tp,cheb_a,cheb_h,xa,yb;
long  diffsec,diffmsec;
time_t time_begin,time_end;
int time_s;//total time in seoonds


double jaco[N_var],hess[N_var*N_var],Gv[N_var*N_consts],gv[N_consts],sp[N_spts];
double check,d_theta;
FILE *fp,*fp2,*fp3,*fp4,*fp5,*fp6,*fp7;

cst=0.01;


time(&time_begin);
//pb=&time_begin;


/* Initial guess */


/* BEGIN USER INPUT */

/* The initial guess can provided in values or a function.*/

for (i=0;i<N_var;i++){
des_var[i]=0.1;}


/*
des_var[0]=89.500000;
des_var[1]=90.879419;
des_var[2]=95.141885;
des_var[3]=101.674295;      //
des_var[4]=104.362237;      // initial guess
des_var[5]=96.631151;       //
.
.
.
.
*/

for (i=0;i<N_spts-2;i++){
tp=(float) (i+1)/((float) N_spts-1.0); 
/* guess fuction */
des_var[i]=sqrt((77.5*cos(tp*M_PI/2.0)+12.0)*(77.5*cos(tp*M_PI/2.0)+12.0)+(63.5*sin(tp*M_PI/2.0)+12.0)*(63.5*sin(tp*M_PI/2.0)+12.0));

s[i+1]=des_var[i];
} 

/* END USER INPUT */

 




s[0]=rho1;
s[N_spts-1]=rhon;
/*for (i=0;i<N_spts;i++){
printf("s(%i)=%f \n",i+1,s[i]); 
}*/

for (i=0;i<N_spts;i++){
tp=(float) (i)/((float) N_spts-1.0); 
theta[i]=ANGLE1+tp*(M_PI/2.0-ANGLE1-ANGLE2);
printf("theta(%i)=%f \n",i+1,theta[i]); 
}  

/*for (i=0;i<N_spts;i++){
tp=(float) i/((float) N_spts-1.0); 
theta[i]=ANGLE1+tp*(M_PI/2.0-ANGLE1-ANGLE2); 
printf("theta(%i)=%f \n",i+1,theta[i]); 
s[i]=rho1+(tp)*(rhon-rho1);
}
for (i=0;i<N_spts-2;i++){
des_var[i]=s[i+1];
}*/
delta_theta=theta[1]-theta[0]; 

printf("delta_theta=%f \n", delta_theta);

/*delta_theta=const*/
matrix_A(A);
matrix_B(B,ANGLE1,ANGLE2);
matrix_Ainv_B(A,B,Ain_B,N_spts);
matrix_E(E,ANGLE1,ANGLE2);
matrix_F(F);
matrix_Ainv_B(E,F,Ein_F,N_spts);

for (i=0;i<N_spts;i++) { 
for (j=0;j<N_spts;j++) { 
printf("Ain_B(%i,%i)=%f;\n",i+1,j+1,Ain_B[i*N_spts+j]);
}}

for (i=0;i<N_spts;i++) { 
for (j=0;j<N_spts;j++) { 
printf("Ein_F(%i,%i)=%f;\n",i+1,j+1,Ein_F[i*N_spts+j]);
}}

//getrusage(RUSAGE_SELF, pb);

n=N_var; /*number of variable */
p=N_consts; /*number of constraints */


for (i=0;i<n;i++) { printf("x_initial(%i)=%f\n",i+1,des_var[i]);}

z_min=ARBITRARY (n,p,des_var,TOLERANCE1);
for (i=0;i<n;i++) { printf("x_opt(%i)=%f\n",i+1,des_var[i]);} 
printf("z_min=%f\n",z_min);


g(gv,des_var);
G(Gv,des_var);
/*Hessian(hess,s); 
Jacobian(jaco,s);    

for (i=0;i<n;i++) { 
  for (j=0;j<n;j++) { printf("hess[%i][%i]=%f\n",i,j,hess[n*i+j]);}}  
 for (j=0;j<n;j++) { printf("jaco[%i]=%f\n",j,jaco[j]);} */
/*for (i=0;i<p;i++) {  
  for (j=0;j<n;j++) { printf("Gv[%i][%i]=%f\n",i,j,Gv[n*i+j]);}}*/   
for (j=0;j<p;j++) { printf("gv[%i]=%f\n",j,gv[j]);} 





vspp(s);
z(des_var); 
for(i=0;i<N_spts-1;i++){ 
printf("Ak(%i)=%f; Bk(%i)=%f; Ck(%i)=%f; Dk(%i)=%f;\n",i+1,Ak[i],i+1,Bk[i],i+1,Ck[i],i+1,Dk[i]);}

/*for (i=0;i<N_spts;i++) { 
  for (j=0;j<N_spts;j++) { printf("A(%i,%i)=%f\n",i+1,j+1,A[N_spts*i+j]);}} 
for (i=0;i<N_spts;i++) { 
  for (j=0;j<N_spts;j++) { printf("B(%i,%i)=%f\n",i+1,j+1,B[N_spts*i+j]);}} 

for (i=0;i<N_spts;i++){
printf("s(%i)=%f\n",i+1,s[i]);
}

for (i=0;i<N_spts;i++){
printf("spp(%i)=%f\n",i+1,spp[i]);
}*/
d_theta=theta[N_spts-1]-theta[N_spts-2];
check=d_theta*spp[N_spts-2]+2*d_theta*spp[N_spts-1]-(6/d_theta*s[N_spts-2]-6/d_theta*s[N_spts-1]+6/tan(M_PI/2+ANGLE2)*s[N_spts-1]);
printf("check%f\n",check);
check=3.0*Ak[N_spts-2]*d_theta*d_theta+2.0*Bk[N_spts-2]*d_theta+Ck[N_spts-2];
check=s[N_spts-1]/check-tan(M_PI/2+ANGLE2);
printf("angle:check%f\n",check);



/*
pe=&time_end;
*/

time(&time_end);
time_s=time_end-time_begin;
printf("User time used: %d sec\n",time_s);


for(i=0;i<N_spts;i++){
 printf("s(%i,1)=%f;\n",i+1,s[i]);}
mmult(sp,Ein_F,s,N_spts,N_spts,1); 
for(i=0;i<N_spts;i++){
 printf("sp(%i,1)=%f;\n",i+1,sp[i]);}
for(i=0;i<N_spts;i++){
 printf("spp(%i,1)=%f;\n",i+1,spp[i]);}


/*Jacobian(jaco,des_var);
for(i=0;i<N_var;i++){
 printf("jaco(%i,1)=%f;\n",i+1,jaco[i]);}*/

/*mmult(sp,Ein_F,s,N_spts,N_spts,1); 
check=D_obj(3,2,s[3],sp[3],spp[3]);
printf("here:D_obj=%f;\n",check);*/


fp = fopen("N_spts.dat","w");
 fprintf(fp,"%i\n",N_spts);
fclose(fp);

fp2 = fopen("theta.dat","w");
for (i=0;i<=N_spts-1;i++){
 fprintf(fp2,"%4.8f\n",theta[i]);
}
fclose(fp2);

fp3 = fopen("x_opt.dat","w");
fprintf(fp3,"supporting points    kappa    spp\n");
fprintf(fp3,"__runing %i s for %i iterations___\n",time_s,total_iter);
for (i=0;i<=N_spts-1;i++){
 fprintf(fp3,"%4.8f   %4.8f   %4.8f\n",s[i],kappa[i],spp[i]);
}

fp4 = fopen("Ak.dat","w");
for (i=0;i<=N_spts-1;i++){
 fprintf(fp4,"%4.8f\n",Ak[i]);
}/*i*/
fclose(fp4);

fp5 = fopen("Bk.dat","w");
for (i=0;i<=N_spts-1;i++){
 fprintf(fp5,"%4.8f\n",Bk[i]);
}/*i*/
fclose(fp5);
fp6 = fopen("Ck.dat","w");
for (i=0;i<=N_spts-1;i++){
 fprintf(fp6,"%4.8f\n",Ck[i]);
}/*i*/
fclose(fp6);



fp7 = fopen("Dk.dat","w");
for (i=0;i<=N_spts-1;i++){
 fprintf(fp7,"%4.8f\n",Dk[i]);
}/*i*/
fclose(fp7);







}/*main*/
/*******************************************************************/
/*************** OBJECTIVE & CONSTRAINT FUNCTIONS ***********************/
double z(double *in_var){
double sp[N_spts],sum,kpa,num,denum,temp;
int k;

sum=0.0;

for (k=0;k<N_spts-2;k++){
s[k+1]=in_var[k];
}

mmult(sp,Ein_F,s,N_spts,N_spts,1);
vspp(s);
for (k=0;k<=N_spts-1;k++){
  /*printf("sp(%i)=%f\n",k+1,sp[k]);*/
num=s[k]*s[k]+2.0*sp[k]*sp[k]-s[k]*spp[k];
temp=sqrt(s[k]*s[k]+sp[k]*sp[k]);
denum=temp*temp*temp;
kpa=num/denum;
kappa[k]=kpa;
printf("kappa(%i)=%2.10f\n",k+1,kappa[k]);

if(k>0 & k<N_spts-1) {
/*printf("k=%i\n",k);*/ sum+=kpa*kpa;}


}/*k*/


return(sum);
}/* obj */

double *g(double *gv,double *in_var) {
double sp,sum,kappa,num,denum,temp;
double r1,rn;
int k,ki;
r1=rho1;
rn=rhon;

for (k=0;k<N_spts-2;k++){
s[k+1]=in_var[k];
}
vspp(s);
/*for (k=0;k<N_spts;k++){
printf("here:s(%i)=%f\n",k+1,s[k]);
}*/
/*printf("spp(0)=%f,r1=%f,ANGLE1=%f,\n",spp[0],r1,ANGLE1);*/

/*zero curvatures*/

gv[0]=spp[0]-r1-2.0*r1/tan(M_PI/2.0-ANGLE1)/tan(M_PI/2.0-ANGLE1);
//gv[N_spts-1]=spp[N_spts-1]-r2-2.0*r2/tan(M_PI/2.0+ANGLE2)/tan(M_PI/2.0+ANGLE2);
gv[1]=spp[N_spts-1]-rn-2.0*rn/tan(M_PI/2.0+ANGLE2)/tan(M_PI/2.0+ANGLE2);
//gv[2]=s[10]-92.5;



/*convexity conditions*/
/*
for(k=2;k<N_spts-1;k=k+2){
 
	ki=1+k/2;
gv[ki]=s[k]*s[k+1]-2*s[k-1]*s[k+1]*cos(delta_theta)+s[k-1]*s[k]-in_var[N_spts+k-3]*in_var[N_spts+k-3];
printf("here:delta_theta=%f in_var[N_spts+k-3]=%f\n",delta_theta, in_var[N_spts+k-3]);
printf("here:s=[%f,%f,%f],gv(%i)=%f\n",s[k-1],s[k],s[k+1],k+1,gv[k]);
} 
*/
return(gv);
}/*g*/


double *G(double *Gv,double *in_var) {
int k,j;
double sp;

for (k=0;k<N_spts-2;k++){
s[k+1]=in_var[k];
}

vspp(s);

 
  for(k=0;k<=N_consts-1;k++){
  for(j=0;j<=N_var-1;j++){
    Gv[k*N_var+j]=0.0;
  }}


/* BEGIN USER INPUT */

  /*first derivative of constraint 1 */
  for(j=0;j<N_spts-2;j++){
	  Gv[j]=6.0*Ain_B[j+1];
	  }
  /* first derivative of constraint 2*/
  for(j=0;j<N_spts-2;j++){
	  Gv[(N_spts-2)+j]=6.0*Ain_B[N_spts*(N_spts-1)+j+1];
	  }

	/* first derivative of constraint 3*/
  //Gv[(N_spts-2)*2+9]=1;


  /* ENG USER INPUT */


return(Gv);
}/*G*/



double D_obj(int i, int j,double y,double yp,double ypp) {
  /* d kappa_i 
    -----------
     d rho_j   */ 
double temp,num1,num2,num3,denum1,denum2,ans,ans1,ans2;
double Dy,Dyp,Dypp;

if (i==j) {Dy=1.0;}
else {Dy=0.0;}

Dyp=Ein_F[i*N_spts+j];
Dypp=6.0*Ain_B[i*N_spts+j];
temp=sqrt(y*y+yp*yp);
num1=2.0*Dy*y+4.0*Dyp*yp-Dy*ypp-y*Dypp;
denum1=temp*temp*temp;
num2=(y*y+2.0*yp*yp-y*ypp)*(2*Dy*y+2*Dyp*yp);
denum2=temp*temp*temp*temp*temp;
ans=num1/denum1-3.0/2.0*num2/denum2;

/*printf("i=%i,j=%i,y=%f,yp=%f,ypp=%f\n",i,j,y,yp,ypp);
printf("temp=%f\n",temp);*/

return(ans);
}/*d_kappa*/


double DD_obj(int i,int j,int k,double y,double yp,double ypp) {

  /*   d^2 kappa_i 
    -----------------
     d rho_j d rho_k  */ 

double ans,Dyj,Dyk,temp,temp3,temp5,temp7;
double Dypj,Dyppj,Dypk,Dyppk;

if (i==j){Dyj=1.0;}
else {Dyj=0.0;}
if (i==k){Dyk=1.0;}
else {Dyk=0.0;}

Dypj=Ein_F[i*N_spts+j];
Dyppj=6.0*Ain_B[i*N_spts+j];
Dypk=Ein_F[i*N_spts+k];
Dyppk=6.0*Ain_B[i*N_spts+k];
temp=sqrt(y*y+yp*yp);
temp3=temp*temp*temp;
temp5=temp*temp*temp*temp*temp;
temp7=temp*temp*temp*temp*temp*temp*temp;

ans=(2.0*Dyj*Dyk + 4.0*Dypj *Dypk - Dyj*Dyppk - Dyk*Dyppj)/temp3-1.5*((2.0*Dyj*y + 4.0*Dypj*yp - Dyj*ypp - y*Dyppj)*(2.0*Dyk*y + 2.0*Dypk*yp))/temp5-1.5*((2.0*Dyk*y + 4.0*Dypk*yp - Dyk*ypp - y*Dyppk)*(2.0*Dyj*y + 2.0*Dypj*yp))/temp5-1.5*((y*y+2.0*yp*yp- y*ypp)*((2.0*Dyj*Dyk + 2.0*Dypj*Dypk)))/temp5+3.75*((y*y+2.0*yp*yp- y*ypp)*(2.0*Dyj*y + 2.0*Dypj*yp)*(2.0*Dyk*y + 2.0*Dypk*yp))/temp7;;

/*printf("ans1=%10.10f, ans3=%f \n", ans1,ans3);*/
return(ans);
}/*dd_kappa*/


double *Jacobian(double *jaco,double *in_var){ 
int i,k;
double sp[N_spts],kappa[N_spts],num,denum,temp;


for(i=0;i<N_var;i++){
   jaco[i]=0.0;
}
for (k=0;k<N_spts-2;k++){
s[k+1]=in_var[k];
}

mmult(sp,Ein_F,s,N_spts,N_spts,1);

for (k=0;k<N_spts;k++){
num=s[k]*s[k]+2.0*sp[k]*sp[k]-s[k]*spp[k];
temp=sqrt(s[k]*s[k]+sp[k]*sp[k]);
denum=temp*temp*temp;
kappa[k]=num/denum;
}/*k*/

for(i=0;i<N_spts-2;i++){
for(k=0;k<N_spts-2;k++){
  jaco[i]=jaco[i]+2*kappa[k+1]*D_obj(k+1,i+1,s[k+1],sp[k+1],spp[k+1]);
    /*printf("i=%i,k=%i\n",i+1,k+1);*/
}}
return(jaco);
}/* Jacobian */ 

double *Hessian(double *hess,double *in_var){ 
double ans,sp[N_spts],kappa[N_spts],num,denum,temp;
int i,j,k;
  for(i=0;i<=N_var-1;i++){
      for(j=0;j<=N_var-1;j++){
	hess[i*N_var+j]=0.0;
      }}

for (k=0;k<N_spts-2;k++){
s[k+1]=in_var[k];
}

mmult(sp,Ein_F,s,N_spts,N_spts,1);
for (k=0;k<N_spts;k++){
num=s[k]*s[k]+2.0*sp[k]*sp[k]-s[k]*spp[k];
temp=sqrt(s[k]*s[k]+sp[k]*sp[k]);
denum=temp*temp*temp;
kappa[k]=num/denum;
}

for(i=0;i<N_spts-2;i++){
for(j=i;j<N_spts-2;j++){
for(k=0;k<N_spts-2;k++){
hess[i*N_var+j]=hess[i*N_var+j]+2.0*D_obj(k+1,i+1,s[k+1],sp[k+1],spp[k+1])*D_obj(k+1,j+1,s[k+1],sp[k+1],spp[k+1])+2.0*kappa[k+1]*DD_obj(k+1,i+1,j+1,s[k+1],sp[k+1],spp[k+1]); }}} 

for(i=0;i<N_var;i++){
for(j=0;j<i;j++){
  hess[j*N_var+i]=hess[i*N_var+j];
}}
/* for(i=0;i<=N_var-1;i++){
      for(j=0;j<=N_var-1;j++){
	printf("hess[%i,%i]=%2.19f\n",i,j,hess[i*N_var+j]);
      }}*/
return(hess);
}/* Hessian */

/************************************************************************/
/******************END: OBJECTIVE & CONSTRAINT FUNCTIONS ****************/


/*******************************************************************/
/*************************** SPLINE FUNCTION ***********************/


void spline ( double *Ak,double *Bk,double *Ck,double *Dk,double *s) {
/*This function calculates all the coefficients of cubic spline functions. 
  Input data are the global variables spp[] and sp[]. Function returns 
  all coefficients  Ak, Bk, Ck, and Dk.
  */
int k;

for (k=0;k<=N_spts-2;k++){
  /*delta_theta=theta[k+1]-theta[k];*/
Ak[k]=1.0/6.0/delta_theta*(spp[k+1]-spp[k]);
Bk[k]=1/2.0*spp[k];
Ck[k]=(s[k+1]-s[k])/delta_theta-1.0/6.0*delta_theta*(spp[k+1]+2.0*spp[k]);
Dk[k]=s[k];
}/*k*/
}/*spline*/


void vspp(double *s){
double s6[N_spts],b[N_spts];
double *s_part;
int i,j;

/*for (j=0;j<N_spts;j++){  
  printf("here:s[%i]=%f\n",j,s[j]);
}*/

s_part=&s[0];
vscale(s6,6.0,s_part,N_spts);
mmult(b,B,s6,N_spts,N_spts,1);
mat_sol_nn(N_spts,A,b, spp);
/*for (i=0;i<N_spts;i++){  
for (j=0;j<N_spts;j++){  
  printf("here:B[%i][%i]=%f\n",i,j,B[i*N_spts+j]);
}}*/


/*for (j=0;j<N_spts;j++){  
  printf("sln[%i]=%f\n",j,spp[j]);
}*/
spline ( Ak,Bk,Ck,Dk,s_part);
/*for (j=0;j<N_spts-1;j++){  
printf("Ak[%i]=%f\t",j,Ak[j]);
printf("Bk[%i]=%f\t",j,Bk[j]);
printf("Ck[%i]=%f\t",j,Ck[j]);
printf("Dk[%i]=%f\n",j,Dk[j]);
}*/
}/*vspp*/
void matrix_A(double *mA){
int i,j;
double a_alpha,alpha1,alpha2;
for(i=0;i<N_spts;i++){
for(j=0;j<N_spts;j++){
mA[N_spts*i+j]=0.0;
}}
mA[0]=2.0*(theta[1]-theta[0]);
mA[1]=(theta[1]-theta[0]);
mA[N_spts*N_spts-2]=(theta[N_spts-1]-theta[N_spts-2]);
mA[N_spts*N_spts-1]=2.0*(theta[N_spts-1]-theta[N_spts-2]);

for(i=1;i<N_spts-1;i++){
alpha1=theta[i]-theta[i-1];
alpha2=theta[i+1]-theta[i];
a_alpha=alpha1+alpha2;

mA[N_spts*i+i-1]=alpha1;
mA[N_spts*i+i]=2.0*a_alpha;
mA[N_spts*i+i+1]=alpha2;
}
for (i=0;i<N_spts;i++){  
for (j=0;j<N_spts;j++){  
  printf("mA(%i,%i)=%f;\n",i+1,j+1,mA[i*N_spts+j]);
}}
}/*matrix_A*/

void matrix_B(double *mB, double ang1, double ang2){
int i,j;
double a_beta,beta1,beta2;
for(i=0;i<N_spts;i++){
for(j=0;j<N_spts;j++){
mB[N_spts*i+j]=0.0;
}}

mB[0]=-1.0/(theta[1]-theta[0])-1.0/(tan(M_PI/2.0-ang1));
mB[1]=1.0/(theta[1]-theta[0]);
mB[N_spts*N_spts-2]=1.0/(theta[N_spts-1]-theta[N_spts-2]);
mB[N_spts*N_spts-1]=-1.0/(theta[N_spts-1]-theta[N_spts-2])+1.0/(tan(M_PI/2.0+ang2));

for(i=1;i<N_spts-1;i++){
beta1=1.0/(theta[i]-theta[i-1]);
beta2=1.0/(theta[i+1]-theta[i]);
a_beta=beta1+beta2;
mB[N_spts*i+i-1]=beta1;
mB[N_spts*i+i]=-a_beta;
mB[N_spts*i+i+1]=beta2;
}

for (i=0;i<N_spts;i++){  
for (j=0;j<N_spts;j++){  
  printf("mB(%i,%i)=%f;\n",i+1,j+1,mB[i*N_spts+j]);
}}
}/*matrix_B*/
void matrix_E(double *mE, double ang1, double ang2){
int i,j;
double a_alpha,alpha1,alpha2;

for(i=0;i<N_spts;i++){
for(j=0;j<N_spts;j++){
mE[N_spts*i+j]=0.0;
}}
mE[0]=tan(M_PI/2.0-ang1);
mE[N_spts*N_spts-1]=tan(M_PI/2.0+ang2);


for(i=1;i<N_spts-1;i++){
mE[N_spts*i+i-1]=delta_theta;
mE[N_spts*i+i]=4.0*delta_theta;
mE[N_spts*i+i+1]=delta_theta;
}
for (i=0;i<N_spts;i++){  
for (j=0;j<N_spts;j++){  
  printf("mE(%i,%i)=%f;\n",i+1,j+1,mE[i*N_spts+j]);
}}
}/*matrix_E*/

void matrix_F(double *mF){
int i,j;
double a_beta,beta1,beta2;
for(i=0;i<N_spts;i++){
for(j=0;j<N_spts;j++){
mF[N_spts*i+j]=0.0;
}}

mF[0]=1.0;
mF[N_spts*N_spts-1]=1.0;

for(i=1;i<N_spts-1;i++){
mF[N_spts*i+i-1]=-3.0;
mF[N_spts*i+i]=0.0;
mF[N_spts*i+i+1]=3.0;
}

for (i=0;i<N_spts;i++){  
for (j=0;j<N_spts;j++){  
  printf("mF(%i,%i)=%f;\n",i+1,j+1,mF[i*N_spts+j]);
}}
}/*matrix_F*/

/*******************************************************************/
/***********************END: SPLINE FUNCTION************************/

/*======================= arbitrary =================================*/

double ARBITRARY (int n, int p, double *xold, double epsilon) {
	/* This function is taken from ODA */

int i,j,k,iter,w_counter;
double z_min,mu;
double Gv[N_consts*N_var],gv[N_consts],gv2[N_consts],Wk2[N_var*N_var];
double delta_x[N_var], xnew[N_var],a_k[N_var],Wk[N_var*N_var];
double Lk[N_var*(N_var-N_consts)];
double hess[N_var*N_var],jaco[N_var],dx0[N_var];

double mgv[N_consts],lower,upper,eye[N_var*N_var];
double Vk[N_var*N_var],du_k1[N_var*(N_var-N_consts)],du_k2[N_var],du_k3[N_var-N_consts],du_k[N_var-N_consts],Lk_ti_du_k[N_var];
double norm_H,bound[3],tol1,tol2,*s_part,check; 

for (i=0;i<n;i++) {delta_x[i]=xold[i];xnew[i]=xold[i];}

iter=1;
tol1=100.0;
tol2=100.0;

w_counter=0.0;
while (tol1>TOLERANCE1 | tol2>TOLERANCE2)  { 
/*while (iter<400 )  { */


for (i=0;i<n;i++) {
for (j=0;j<n;j++) {   
hess[(n)*i+j]=0.0;}}
/*s_part=&xold[0];
vspp(s_part);*/ 

for(i=0;i<N_spts-2;i++){
s[i+1]=xnew[i];
}
vspp(s);
/*check=z(des_var);
printf("z=%f,\n",check);*/
/*for(i=0;i<N_spts;i++){
printf("here: s[%i]=%f \n",i,s[i]);
}*/

Hessian(hess, xnew);
Jacobian(jaco,xnew);
G(Gv,xnew);
g(gv,xnew);
mscale(mgv,-1.0,gv,p,1);
Lk_dx0(Lk,dx0,Gv,mgv,p,n);

/*for (i=0;i<n;i++) {
for (j=0;j<n-p;j++) {        
  printf("Lk(%d,%d)=%f\n",i+1,j+1,Lk[(n-p)*i+j]);}}*/
/*for (i=0;i<n;i++) {
for (j=0;j<n;j++) {        
  printf("hess(%d,%d)=%f\n",i+1,j+1,hess[n*i+j]);}}*/
Gerschgorin(bound,hess,n); 
lower=bound[0];
/*mu=1.0-0.00001/lower;*/
/*norm_H=maximum_norm(hess, n,n);
printf("Norm of  H=%f\n" ,norm_H);*/

mu=1.01;
printf("lower=%f\t upper=%f \t width=%f\n",bound[0],bound[1],bound[2]);
I_mat(eye,n);


if (lower==0.0) {
mscale(Wk2,1.0, eye, n,n); 
madd(Wk, hess,0.0001, Wk2,n,n);/*printf("Hessian (psd )stabilized\n");*/ }
if (lower>0.0) {mat_copy(Wk,hess,n,n);}

if (lower<0.0) {
mscale(Wk2,mu*lower, eye, n,n);
madd(Wk, hess,-1.0, Wk2,n,n);
printf("Hessian stabilized\n"); 
/*Gerschgorin(bound,Wk,n); lower2=bound[0];
printf("After: lower=%f\t upper=%f \t
width=%f\n\n",lower2,bound[1],bound[2]);*/
} /*(lower<0.0)*/

/*norm_H=maximum_norm(Wk, n,n);
printf("Norm of updated H=%f\n" ,norm_H);*/


/*for (i=0;i<p;i++) {
 for (j=0;j<n;j++) {        
  printf("Gv[%d][%d]=%f\n",i+1,j+1,Gv[(n)*i+j]);}}  */

/*for (i=0;i<n;i++) {printf("dx0[%d]=%2.10f\n",i,dx0[i]);}*/

/*mtrans(LkT,Lk,n,n-p);
printf("\nNormality Condition:\n"); 
mmult(check7, LkT,jaco, n-p,n,1); 
for (i=0;i<n-p;i++) {printf("\n Check[%d]=%f\n",i,check7[i]);}*/


Cholesky (Vk, Wk,n);
ak(a_k,n,p,Wk,hess,jaco,dx0);


mmult(du_k1,Vk,Lk,n,n,n-p);  /* Vk:nxn;Lk:nx(n-p) du_k1:nx(n-p) */
mmult(du_k2,Vk,a_k,n,n,1); /* a_k:nx1 du_k2:nx1*/

hh_sln(n, n-p, du_k3 ,du_k1, du_k2); /*overdetermined*//*du_k3:n-px1*/
mscale(du_k,-1.0,du_k3,n-p,1);  /* du_k:(n-p)x1 */
mmult(Lk_ti_du_k,Lk,du_k,n,n-p,1);
madd(delta_x,dx0,1.0,Lk_ti_du_k,n,1);
madd(xnew,xold,STEP_SIZE,delta_x,n,1);
mat_copy(xold,xnew,n,1);
g(gv2,xnew);

for (i=0;i<n;i++) {printf("xnew[%d]=%f\n",i,xnew[i]);}

iter=iter+1;
tol1=sqrt(vdot(delta_x,delta_x,n));
tol2=sqrt(vdot(gv2,gv2,p));

/*for (i=0;i<n;i++) {
printf("delta_x[%i]=%f\n",i,delta_x[i]); 
} */

/*for (i=0;i<p;i++) {
printf("gv2[%i]=%f\n",i,gv2[i]); 
}*/

/*tol1=0.0; tol2=0.0;
for (i=0;i<n;i++) 
{tol1=tol1+delta_x[i]*delta_x[i];
tol2=tol2+gv2[i]*gv2[i];
printf("delta_x[%i]=%f,gv2[%i]=%f\n",i,delta_x[i],i,gv2[i]);
printf("tol1=%f\t tol2=%f\n\n",tol1,tol2);
}*/
printf("tol1=%f\t tol2=%f\n\n",tol1,tol2);

/*vspp(s);
z(s); 
for(i=0;i<N_spts-1;i++){ 
printf("Here :Ak[%i]=%f  Bk[%i]=%f  Ck[%i]=%f  Dk[%i]=%f \n",i,Ak[i],i,Bk[i],i,Ck[i],i,Dk[i]);}*/

/*w_counter=w_counter+1; 
if (w_counter>=1000)    
{  
tol1=TOLERANCE1;   
tol2=TOLERANCE2;   
printf("Number of iterations exceeds given maximum value.\n");  
}  */  

} /*while*/ 

/*mmult(Lk_ti_du_k,Lk,du_k,n,n-p,1);
madd(Lua,Lk_ti_du_k,1.0,a_k,n,1);*/

for(i=0;i<N_spts-2;i++){
s[i+1]=xnew[i];
}

vspp(s);

z_min=z(xnew);


printf("z_min=%f \n",z_min);
/*check normality condition*/


/*printf("\nNormality Condition:\n");
Hessian(hess, xnew); 
Jacobian(jaco,xnew); 
G(Gv,xnew);
g(gv,xnew);
mscale(mgv,-1.0,gv,p,1); 
Lk_dx0(Lk,dx0,Gv,mgv,p, n); 
mtrans(LkT,Lk,n,n-p);
mmult(check7, LkT,jaco, n-p,n,1);
for (i=0;i<n-p;i++) {printf("\n Check[%d]=%f\n",i,check7[i]);}*/


total_iter=iter-1;
printf("\n Number of iterations :%d\n",iter-1);

return(z_min);
} /*ARBITRARY*/







/*=============================== eye ===============================*/
 double *I_mat(double *eye_mat, int n) {
int i,j;
for(i=0;i<n;i++) {
for(j=0;j<n;j++) {
eye_mat[n*i+j]=0.0;}
eye_mat[n*i+i]=1.0;}
return(eye_mat);
} /* eye */
/*============================ mat_copy =============================*/
void mat_copy(double *mA,double *mB, int m, int n) {
int i,j;
for(i=0;i<m;i++) {
for(j=0;j<n;j++) {
  
  mA[n*i+j]=mB[n*i+j];}}

}/*mat_copy*/

/********************************* vdot() *********************************
   Vector dot product
*/
double vdot(double *a,double *b, int Num_Row)
 
{
 int J; 
 double result;
 result=0.0;
 for ALL_ROWS { 
 result =  a[J] * b[J] + result ;
 }
 return(result);
}


/********************************* vadd() *********************************
   Vector addition or subraction
*/
double *vadd(double *a,double *b,double scale,double *c, int Num_Row)
{
int I,J,K; 
 for ALL_ROWS {

 a[J] =  b[J] + scale * c[J] ;
  }
 return(a);
}


/********************************* madd() *********************************
   addition or subtraction of two matrices
*/   /* 3x3-CHECK */
double *madd(double *a, double *b, double scale, double *c, int Num_Row, int Num_Column)
{
int I,J,K; 
 for ALL_COLUMNS {
   vadd(&a[Num_Row*I],&b[Num_Row*I],scale,&c[Num_Row*I],Num_Row); 
 }
 return(a);
}

/********************************* mtrans() *********************************
   transpose of a matrix
*/
double *mtrans(double *a,double *b, int Num_Row, int Num_Column)
{
/* use size of matrix b for all_rows & all_columns */
int I,J,K; 
 K = 0;
 for ALL_COLUMNS {
   for ALL_ROWS { 
    a[K] = b[I+J*Num_Column];
    K = K + 1;
   }
 }
 return(a);
}

/********************************* mmult() *********************************
   Matrix multiplication 
*/  /*checked !!*/
/*a=b*c*/
double *mmult(double *a,double *b,double *c, int Num_Row,int Num_Iter, int Num_Column)
{
int I,J,K; 
 for ALL_ROWS {
   for ALL_COLUMNS { 
     a[Num_Column*J+I]=0; /*  initial value MUST be assigned! */
     for (K=0;K<Num_Iter;K++) {     
      a[Num_Column*J+I] += b[Num_Iter*J+K] * c[Num_Column*K+I];
      /*printf("a[%i]=%f,\tb[%i]=%f\t,c[%i]=%f\n",Num_Column*J+I,a[Num_Column*J+I],Num_Iter*J+K,b[Num_Iter*J+K],Num_Column*K+I,c[Num_Column*K+I]);*/
     }
   }
 }
 return(a);
}
/********************************* vscale() *********************************
   Multiplication of a vector by a scalar
*/
double *vscale(double *a, double scale, double *b, int Num_Row)
{
  int J; 
 for ALL_ROWS {

 a[J] =  scale * b[J] ;

 }
 return(a);
}


/********************************* mscale() *********************************
  Multiplication of a matrix by a scalar
*/
double *mscale(double *a, double scale, double *b, int Num_Row, int Num_Column)
{
  /*int I,J;*/ 
 for ALL_ROWS {

 vscale(&a[Num_Column*J],scale,&b[Num_Column*J],Num_Column) ;

 }
 return(a);
}



/*=========================  LU Decomposition  ========================*/

int mat_lu(int n,double *Ain,int *P )
{
	int	i, j, k;
	int	maxi, tmp;
	double	c, c1;
	int	p;

	for (p=0,i=0; i<n; i++)
		{
		P[i] = i;
		}

	for (k=0; k<n; k++)
	{
	/*--- partial pivoting ---*/
	for (i=k, maxi=k, c=0.0; i<n; i++)
		{
		c1 = fabs( Ain[n*P[i]+k] );
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
		tmp = P[k];
		P[k] = P[maxi];
		P[maxi] = tmp;
		}

	/*
	*	suspected singular matrix
	*/
	if ( Ain[n*P[k]+k] == 0.0 )
		return (-1);

	for (i=k+1; i<n; i++)
		{
		/*
		* --- calculate m(i,j) ---
		*/
		Ain[n*P[i]+k] = Ain[n*P[i]+k] / Ain[n*P[k]+k];

		/*--- elimination ---*/
		for (j=k+1; j<n; j++)
			{
			Ain[n*P[i]+j] -= Ain[n*P[i]+k] * Ain[n*P[k]+j];
			}
		}
	}

	return (p);
}

double *mat_backsubs1( int n, double *Ain, double *bin, double *x, int *P) 

{
        int     i, j, k;
        double  sum;

        for (k=0; k<n; k++)
                {
                for (i=k+1; i<n; i++)
                        bin[P[i]] -= Ain[n*P[i]+k] * bin[P[k]];
                }

        x[n-1] = bin[P[n-1]] / Ain[n*P[n-1]+(n-1)];
        for (k=n-2; k>=0; k--)
                {
                sum = 0.0;
                for (j=k+1; j<n; j++)
                        {
                        sum += Ain[n*P[k]+j] * x[j];
                        }
                x[k] = (bin[P[k]] - sum) / Ain[n*P[k]+k];
                }

        return (x);
}

double *mat_sol_nn(int n,double *Ain,double *bin, double *x) {
int P[ARRAY_SIZE1]/*,i,j*/;
double mA[MATRIX_SIZE1];
mat_copy(mA,Ain,n,n);
/*printf("n=%i\n",n);
for (i=0;i<n;i++) { 
  for (j=0;j<n;j++) {printf("Ain[%i][%i]=%f\n",i,j,Ain[n*i+j]);}}*/

        mat_lu( n, mA, P );
        mat_backsubs1(n, mA, bin, x, P);

	/*for (i=0;i<n;i++) {printf("bini[%i]=%f\n",i,bin[i]);}*/
return(x);

}


void matrix_Ainv_B(double *Ain,double *Bin, double *mANS, int n){
int i,j;
int P[ARRAY_SIZE1];
double mA[MATRIX_SIZE1];
double b[ARRAY_SIZE1],x[ARRAY_SIZE1];

mat_copy(mA,Ain,n,n);
for (i=1;i<n;i++){
for(j=0;j<n;j++) {
mANS[i*n+j]=0.0;}}
mat_lu( n, mA, P );

for (i=0;i<n;i++){
for(j=0;j<n;j++) b[j]=Bin[j*n+i];
	mat_backsubs1(n, mA, b, x, P);
for(j=0;j<n;j++) mANS[j*n+i]=x[j];
} /*i*/


}/* matrix_Ainv_B */



/*===================================================================*/
/*===================== maximum_norm ================================*/

double maximum_norm(double *Ain, int Num_Row, int Num_Column){
double ans, mA[MATRIX_SIZE1];
int i,j;
ans=Ain[0];
mat_copy(mA,Ain,Num_Row,Num_Column);
for (i=0;i<Num_Row;i++){
for (j=0;j<Num_Column;j++){
if (mA[Num_Column*i+j]<0.0) mA[Num_Column*i+j]=-mA[Num_Column*i+j];
if (mA[Num_Column*i+j]>ans) ans=mA[Num_Column*i+j];
}}

return(ans);
}/* maximum_norm */

/*===================================================================*/
/*======================== Householder:matrix =======================*/
void hh(int m, int n, double *H, double *Ain) {
	/* Subroutine producing an upper-triangular matrix out fo a rectangular 
	matrix of mXn, with m>n, using Householder reflections */
int i,j,k;
double u[MATRIX_SIZE1],a[ARRAY_SIZE1],alpha[ARRAY_SIZE1];
double sign_ak,dot_akm,up[MATRIX_SIZE1],beta[ARRAY_SIZE1],upb[MATRIX_SIZE1],eye[MATRIX_SIZE1];
double Hk[MATRIX_SIZE1],Ht[MATRIX_SIZE1],A[MATRIX_SIZE1],At[MATRIX_SIZE1],ut[MATRIX_SIZE1];


mat_copy(A,Ain,m,n);
I_mat(eye,m);
I_mat(H,m);

for (i=0;i<m;i++) {
  u[i]=0.0; }  /*u:mx1*/

/*for (i=0;i<m;i++) {
    for (j=0;j<n;j++) {
      printf("Ain(%i,%i)=%2.10f;\n",i+1,j+1,A[n*i+j]);}}*/

/*printf(" hh: m=%i, n=%i \n",m,n);*/
for (k=0;k<n;k++) {
  for (i=0;i<m;i++) {a[i]=A[n*i+k];/*printf("\n a[%i]=%f \n",i,a[i]);*/}
  if (a[k]>=0.0) sign_ak=1.0;
  else  sign_ak=-1.0;
  dot_akm=0.0;
  for (j=k;j<m;j++){
    dot_akm=dot_akm+a[j]*a[j];/*printf("\n j=%i, dot_akm=%f\n",j,dot_akm);*/} 

  alpha[k]=sign_ak*sqrt(dot_akm);
  for (j=0;j<k;j++) {
    u[j]=0.0;}
  u[k]=a[k]+alpha[k];
  /*printf("dot_akm=%f",dot_akm);
  printf("alpha[%d]=%f\n",k,alpha[k]); 
  printf("a[%d]=%2.9f,alpha[%d]=%2.9f\n",k,a[k],k,alpha[k]);*/
  for (j=k+1;j<m;j++) {
    u[j]=a[j];}

  

  beta[k]=alpha[k]*u[k]; 
  mtrans(ut,u,m,1);  
  mmult(up,u,ut,m,1,m); /*u=ut*/
  /*for (i=0;i<m;i++) { for (j=0;j<m;j++) {
    printf("up[%d][%d]=%f\n",i,j,up[m*i+j]);}} 
  printf("beta[%d]=%f\n",k,beta[k]);*/
  mscale(upb,1.0/beta[k],up,m,m);
  madd(Hk,eye,-1.0,upb,m,m);

  for (i=0;i<m;i++) {
    for (j=0;j<m;j++) {
      Ht[m*i+j]=H[m*i+j];}}
  for (i=0;i<m;i++) {
    for (j=0;j<n;j++) {
      At[n*i+j]=A[n*i+j];}}
  mmult(H,Hk,Ht,m,m,m);
  mmult(A,Hk,At,m,m,n); /* VIP !! Update A in each loop */

}/*k*/


} /*hh*/		       
/*===================================================================*/

/*===================== Backsubstitution ============================*/


double *backsubs(int m, int n, double *sln, double *HAin, double *Hb){
int i,j,k;
double sum;
for (i=0;i<n;i++){
  sln[i]=0.0;}
for (j=0;j<n;j++) {
  i=n-1-j;
  sum=0.0;
  for (k=i+1;k<=n;k++) {
    sum=sum+HAin[n*i+k]*sln[k];}
  /*printf("sum=%f\n",sln[k]);*/
  sln[i]=(Hb[i]-sum)/HAin[n*i+i];
}/*i*/
return(sln);
}/*backsubs*/
/*======================== Householder:sln (m>n only )=============*/
double *hh_sln(int m, int n, double *sln, double *Ain, double *b) {
double H[MATRIX_SIZE1],HAin[MATRIX_SIZE1],Hb[MATRIX_SIZE1];
/*int i,j;*/
hh( m, n,  H,  Ain);
mmult(HAin,H,Ain,m,m,n);
mmult(Hb,H,b,m,m,1);
/*for (i=0;i<m;i++) {
  for (j=0;j<n;j++) { 
    printf("HAin[%d][%d]=%f\n",i,j,HAin[n*i+j]);}}*/
backsubs(m,n, sln, HAin, Hb); /* must be a square matrix */
/*for (j=0;j<m;j++) { 
  printf("Hb[%d]=%f\n",j,Hb[j]);}*/
return(sln);
}/* Householder:sln */

/*========================== Cholesky ===============================*/

double *Cholesky (double *chout, double *W, int n)
{
int i,j, k, p;
double sum1,sum2,ch[MATRIX_SIZE1];

for (i=0;i<n; i++){
for (j=0;j<n; j++){
ch[n*i+j]=0.0;
}}

for (k=0;k<n;k++){
  sum1=0.0; 
  for (p=0;p<=k-1;p++) {
    sum1=sum1+ch[n*k+p]*ch[n*k+p];}
  ch[n*k+k]=sqrt(W[n*k+k]-sum1);
  for (i=k+1;i<=n;i++){
  sum2=0.0;
  for (p=0;p<=k-1;p++) {
    sum2=sum2+ch[n*i+p]*ch[n*k+p];}
    ch[n*i+k]=(W[n*i+k]-sum2)/ch[n*k+k];}
}/*k*/


mtrans(chout,ch,n,n);
return(chout);
} /* Cholesky */

/*===================================================================*/


/*==========================  Gerschgorin ============================*/
/* Gerschgorin: The Matrix has to be square.*/
double *Gerschgorin (double *bound, double *Ain, int n) {
double sign,v_lower[ARRAY_SIZE1],v_upper[ARRAY_SIZE1],r[ARRAY_SIZE1],lower,upper;
int i,j;


for (i=0;i<n;i++){ 
v_lower[i]=0.0; 
v_upper[i]=0.0;}


  for (i=0;i<n;i++){
    r[i]=0.0;
    for (j=0;j<n;j++){
      if (j!=i) {
	if (Ain[n*i+j]>=0.0) sign=1.0;
	else sign=-1.0;
	r[i]=r[i]+sign*(Ain[n*i+j]);}
	    }/*j*/
    v_lower[i]=Ain[n*i+i]-r[i];
    v_upper[i]=Ain[n*i+i]+r[i];
  }/*i*/

  lower=v_lower[0];
  upper=v_upper[0];
  for (i=0;i<n;i++){
    if (v_lower[i]<lower)  {lower=v_lower[i];}
    if (v_upper[i]>upper)  {upper=v_upper[i];}
  }/*i*/
bound[0]=lower;
bound[1]=upper;
bound[2]=upper-lower;



return(bound);
}/* Gerschgorin */
/*===================================================================*/
/*============================ ak ===================================*/

double *ak(double *a_k, int n, int p, double *Wk,double *Hess,double
	  *Jaco,double *dx0) { 
double b[N_var],Hdx0[N_var];
/*int i,j;*/
mmult(Hdx0,Hess,dx0,n,n,1);
madd(b, Hdx0, 1, Jaco, n, 1);
mat_sol_nn(n,Wk,b,a_k);
/*for (i=0;i<n;i++) {
  for (j=0;j<n;j++) {printf("Wk[%d][%d]=%f\n",i,j,Wk[n*i+j]);}}*/
return(a_k);
}/*ak*/
/*===================================================================*/
/*========================== Lk_dx0 =================================*/

void Lk_dx0(double *L,double *x0,double *Cin,double *din,int p, int n)
{

int np,i,j;

double H[N_var*N_var],Ht[N_var*N_var],Ct[N_var*N_consts];
double E[N_var*(N_var-N_consts)],C[N_var*N_consts];
 double Hcp[N_var*N_consts],Up[N_consts*N_consts],Upt[N_consts*N_consts];
double y[N_var],d[N_consts],eye_m[MATRIX_SIZE1];
/*double check1[(N_var-N_consts)*(N_var-N_consts)];*/
 
np=n-p;
mat_copy(C,Cin,p,n);
mat_copy(d,din,p,1);

for (i=0;i<n;i++){
   x0[i]=0.0;
  for (j=0;j<np;j++){
    L[np*i+j]=0.0;}}/*L:nxnp*/

mtrans(Ct,C,p,n); /*C:p*n*/
hh(n,p,H,Ct);  /*H:nxn*/ 

/*printf("\n n=%i, p=%i \n",n,p);*/


/*for (i=0;i<n;i++) {
  for (j=0;j<p;j++) {
    printf("Ct(%i,%i)=%2.15f \n",i+1,j+1,Ct[i*p+j]);}} */
/*for (i=0;i<n;i++) {
  for (j=0;j<n;j++) {
    printf("H[%i][%i]=%f \n",i,j,H[i*n+j]);}}*/

I_mat(eye_m, np);

for (i=0;i<p;i++) {
  for (j=0;j<np;j++) {
    E[np*i+j]=0.0;
  }}

for (i=0;i<np;i++) {
  for (j=0;j<np;j++) {
    E[p*np+np*i+j]=eye_m[np*i+j];}}

mtrans(Ht,H,n,n);
mmult(L,Ht,E,n,n,np); /*L:nxnp*/
mmult(Hcp,H,Ct,n,n,p); /*Hcp:nxp*/

for (i=0;i<p;i++) {
  for (j=0;j<p;j++) {
    Up[p*i+j]=Hcp[p*i+j];}}

mtrans(Upt,Up,p,p);

mat_sol_nn(p,Upt,d,y);
for (i=p;i<n;i++) { y[i]=0.0;}
mmult(x0,Ht,y,n,n,1);

/*for (i=0;i<n;i++) {
  for (j=0;j<np;j++) { 
    printf("L[%i][%i]=%f \n",i,j,L[i*np+j]);}}*/


/*for (i=0;i<p;i++) {
  for (j=0;j<p;j++) { 
    printf("Upt[%i][%i]=%f \n",i,j,Upt[i*p+j]);}} 


for (j=0;j<n;j++) { 
    printf("y[%i]=%f\n",j,y[j]);
  } 
for (j=0;j<n;j++) { 
    printf("x0[%i]=%f\n",j,x0[j]); 
  }*/
/*mmult(check1,Cin,x0,n,n,1);

  for (j=0;j<np;j++) {
    printf("check1[%i]=%f\n",j,check1[j]);
  }*/
/*for (i=0;i<n;i++) {
  for (j=0;j<np;j++) { 
    printf("L[%i][%i]=%f \n",i,j,L[i*np+j]);}}*/

}
/*===================================================================*/