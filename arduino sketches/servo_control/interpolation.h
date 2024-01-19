#pragma once


class quintic_interpolation
{

  private:

  double coeff[3][4] = {
    { 2, -1, 3, 9},
    { 1, 1, 1, 6},
    { 1, -1, 1, 2},
  };
  double initial_time = 0, final_time = 0, initial_pos = 0, final_pos = 0, initial_velocity = 0, final_velocity = 0, initial_accelartion = 0, final_acceleration = 0;
  double x, y, z;

  public:
  
  double values[200];
  quintic_interpolation(double _initial_time, double _final_time, double _initial_pos, double _final_pos, double _initial_velocity, double _final_velocity, double _initial_accelartion, double _final_acceleration);
  double determinant_of_matrix(double mat[3][3]);
  void solve(double coeff[3][4], double* x, double* y, double* z);
  void points(void);
  void velocity(void);
  void acceleration(void);
  double current_point(double current_time);
};
