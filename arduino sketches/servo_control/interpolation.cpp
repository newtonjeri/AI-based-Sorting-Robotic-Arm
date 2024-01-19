#include <stdio.h>
#include <math.h>
#include "interpolation.h"
char send[30];

double quintic_interpolation::determinant_of_matrix(double mat[3][3])
{


  //This method uses crammers rule to find the variables in the equation

  double ans;

  ans = mat[0][0] * (mat[1][1] * mat[2][2] - mat[2][1] * mat[1][2])
    - mat[0][1] * (mat[1][0] * mat[2][2] - mat[1][2] * mat[2][0])
    + mat[0][2] * (mat[1][0] * mat[2][1] - mat[1][1] * mat[2][0]);

  return ans;

}

void quintic_interpolation::solve(double coeff[3][4], double* x, double* y, double* z)
{


  //This function finds the solution for the system of linear equations
  
  double d[3][3] = {
    { coeff[0][0], coeff[0][1], coeff[0][2]},
    { coeff[1][0], coeff[1][1], coeff[1][2]},
    { coeff[2][0], coeff[2][1], coeff[2][2]}
  };

  //matrix d1 using coeff as given in crammer's rule

  double d_1[3][3] = {
    { coeff[0][3], coeff[0][1], coeff[0][2]},
    { coeff[1][3], coeff[1][1], coeff[1][2]},
    { coeff[2][3], coeff[2][1], coeff[2][2]},
  };

  //matrix d2 using coeff as given in crammers rule

  double d_2[3][3] = {
    { coeff[0][0], coeff[0][3], coeff[0][2]},
    { coeff[1][0], coeff[1][3], coeff[1][2]},
    { coeff[2][0], coeff[2][3], coeff[2][2]},
  };

  //matrix d3 using coeff as givem in crammers rule

  double d_3[3][3] = {
    { coeff[0][0], coeff[0][1], coeff[0][3]},
    { coeff[1][0], coeff[1][1], coeff[1][3]},
    { coeff[2][0], coeff[2][1], coeff[2][3]},
  };

  //calculating determinants of of matrices d, d_1, d_2, d_3
  double D = determinant_of_matrix(d);
  double D_1 = determinant_of_matrix(d_1);
  double D_2 = determinant_of_matrix(d_2);
  double D_3 = determinant_of_matrix(d_3);


  //printf("the value of D is %f\r\n", D);
  //printf("the value of D_1 is %f\r\n", D_1);
  //printf("the value of D_2 is %f\r\n", D_2);
  //printf("the value of D_3 is %f\r\n", D_3);

  //Case 1
  if (D != 0)
  {
    // coeff have a unique solution. Apply crammers rule
    *x = D_1 / D;
    *y = D_2 / D;
    *z = D_3 / D;

    //printf("the value of X is %f\r\n", *x);
    //printf("the value of Y is %f\r\n", *y);
    //printf("the value of Z is %f\r\n", *z);

  }

  //case 2
  else if (D_1 == 0 && D_2 == 0 && D_3 == 0)
  {}
    //Debug.UART_SendString("Infinite solutions\r\n");
  else if (D_1 != 0 || D_2 != 0 || D_3 != 0)
  {}
    //Debug.UART_SendString("No solutions\r\n");


}


quintic_interpolation::quintic_interpolation(double _initial_time, double _final_time, double _initial_pos, double _final_pos, double _initial_velocity, double _final_velocity, double _initial_accelartion, double _final_acceleration)
{

  initial_time = _initial_time;
  final_time = _final_time; 
  initial_pos = _initial_pos; 
  final_pos = _final_pos;
  initial_velocity = _initial_velocity;
  final_velocity = _final_velocity;
  initial_accelartion = _initial_accelartion;
  final_acceleration = _final_acceleration;


  //printf("initial time = %f\r\n", initial_time);
  //printf("final time = %f\r\n", final_time);
  //printf("initial position = %f\r\n", initial_pos);
  //printf("final position = %f\r\n", final_pos);
  //printf("InitiaL velocity = %f\r\n", initial_velocity);
  //printf("final velocity = %f\r\n", final_velocity);
  //printf("initial acceleration = %f\r\n", initial_accelartion);
  //printf("final acceleration = %f\r\n", final_acceleration);
  /*
  coeff[3][4] = {
    { (double)powf(final_time, 3),  (double)powf( final_time, 4),  (double)powf( final_time, 5),  (double)(final_pos - initial_pos - initial_velocity*final_time - initial_accelartion*powf( final_time, 2))},
    { (double)(3*powf( final_time, 2)),  (double)(4*powf(final_time, 3)), (double)(5*powf( final_time, 4)), (double)(final_velocity - initial_velocity - 2*initial_accelartion*final_time)},
    { (double)(6*final_time), (double)(12*pow( final_time, 2)), (double)(20*pow( final_time, 3)), (double)(final_acceleration - 2*initial_accelartion)},
  };
  */

  coeff[0][0] = (double)powf(final_time, 3);
  coeff[0][1] = (double)powf(final_time, 4);
  coeff[0][2] = (double)powf(final_time, 5);
  coeff[0][3] = (double)(final_pos - initial_pos - initial_velocity * final_time - initial_accelartion * powf(final_time, 2));
  coeff[1][0] = (double)(3 * powf(final_time, 2));
  coeff[1][1] = (double)(4 * powf(final_time, 3));
  coeff[1][2] = (double)(5 * powf(final_time, 4));
  coeff[1][3] = (double)(final_velocity - initial_velocity - 2 * initial_accelartion * final_time);
  coeff[2][0] = (double)(6 * final_time);
  coeff[2][1] = (double)(12 * pow(final_time, 2));
  coeff[2][2] = (double)(20 * pow(final_time, 3));
  coeff[2][3] = (double)(final_acceleration - 2 * initial_accelartion);
  
  solve(coeff, &x, &y, &z);

}

void quintic_interpolation::points(void)
{

  

  double current_point = 0; 
  //printf("t = %f, current point = %f\r\n", initial_time, current_point);
  //printf("final time = %f\r\n", final_time);
  for (initial_time; initial_time < (final_time + 0.001); initial_time++)
  {

    current_point = initial_pos + initial_velocity * initial_time + initial_accelartion * powf(initial_time, 2) + x * powf(initial_time, 3) + y * powf(initial_time, 4) + z * powf(initial_time, 5);
    //sprintf(send," %d, %d\r\n", (int)initial_time, (int)(current_point * 1000));
    //Debug.UART_SendString(send);
    

  }

}


void quintic_interpolation::velocity(void)
{

  double current_point = 0;
  initial_time = 0;
  for (initial_time; initial_time < (final_time + 0.001); initial_time++)
  {

    current_point = initial_velocity + 2 * initial_accelartion * initial_time + 3 * x * powf(initial_time, 2) + 4 * y * powf(initial_time, 3) + 5 * z * powf(initial_time, 4);
    //printf(" %f, %f\r\n", initial_time, current_point);
    //values[(int)initial_time] = current_point;

  }


}




void quintic_interpolation::acceleration(void)
{

  double current_point = 0;
  initial_time = 0;
  for (initial_time; initial_time < (final_time + 0.001); initial_time++)
  {

    current_point = 2 * initial_accelartion + 6 * x * initial_time + 12 * y * powf(initial_time, 2) + 20 * z * powf(initial_time, 3);
    //printf(" %f, %f\r\n", initial_time, current_point);
    //values[(int)initial_time] = current_point;

  }


}

double quintic_interpolation::current_point(double current_time)
{
  
  double current_point = 0;
  current_point = initial_pos + initial_velocity * current_time + initial_accelartion * powf(current_time, 2) + x * powf(current_time, 3) + y * powf(current_time, 4) + z * powf(current_time, 5);
  
  return current_point;
  
}
