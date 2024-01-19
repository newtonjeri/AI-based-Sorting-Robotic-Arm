#include <Servo.h>
#include <string.h>
#include "interpolation.h"


//delcare init thetas
float init_theta_11 = 90, init_theta_21 = 90, init_theta_31 = 90, init_theta_41 = 90;

int joint_1;
int joint_2;
int joint_3;
int joint_4;
int gripper_1;


String data_positions[5];

char buff[20];

// Declare the Arduino pin where each servo is connected
#define BASE_WAIST_SERVO_PIN 11
#define WAIST_LINK1_SERVO_PIN 12
#define L1_L2_SERVO_PIN 13
#define L2_GRIPPER_BASE_SERVO_PIN 5
#define GRIPPER_SERVO_PIN 2

// Define the start configuration of the joints
#define BASE_WAIST_START 90       // base_servo
#define WAIST_L1_START 90         // sholder  /* OKAY /* positive is anticlockwise while facing sgoulder servo zero is laying on the base towards the front
#define L1_L2_START 90            // Elbow   /* positive is clockwise facing the shoulder servo zero is parallel facig upwards
#define L2_GRIPPER_BASE_START 90  // wrist /* positive is anticlockwis while facing shoulder servo, zero is 90 degree acing right
#define GRIPPER_START 0           // 0 closing, 90 Opening

// Register the servo motors of each joint
Servo base_waist_servo;
Servo waist_link1_servo;
Servo link1_link2_servo;
Servo link2_gripperbase_servo;
Servo gripper;

uint8_t idx = 0;
uint8_t val_idx = 0;
char value[4] = "0\0\0\0";
char chr;
String data;
//char data[20];

/*
  This function moves a given servo smoothly from a given start position to a given end position.
  The movement can be both clockwise or counterclockwise based on the values assigned to
  the start position and end position
*/
void reach_goal(Servo& motor, int goal) {
  if (goal >= motor.read()) {
    // goes from the start point degrees to the end point degrees
    for (int pos = motor.read(); pos <= goal; pos += 1) {
      motor.write(pos);
      delay(5);
    }
  } else {
    // goes from the end point degrees to the start point degrees
    for (int pos = motor.read(); pos >= goal; pos -= 1) {
      motor.write(pos);
      delay(5);
    }
  }
}

void setup() {
  // Attach and Initialize each Servo to the Arduino pin where it is connected
  base_waist_servo.attach(BASE_WAIST_SERVO_PIN);
  waist_link1_servo.attach(WAIST_LINK1_SERVO_PIN);
  link1_link2_servo.attach(L1_L2_SERVO_PIN);
  link2_gripperbase_servo.attach(L2_GRIPPER_BASE_SERVO_PIN);
  gripper.attach(GRIPPER_SERVO_PIN);

  // Set a common start point for each joint
  // This way, the start status of each joint is known
  base_waist_servo.write(BASE_WAIST_START);
  waist_link1_servo.write(WAIST_L1_START);
  link1_link2_servo.write(L1_L2_START);
  link2_gripperbase_servo.write(L2_GRIPPER_BASE_START);
  gripper.write(GRIPPER_START);

  // Start the Serial communication with ROS
  Serial.begin(9600);
}

void loop() {
  Serial.flush();
  if (Serial.available()) {
    while(!Serial.available());
    data_positions[0] = Serial.readStringUntil('\n');
    Serial.println(data_positions[0]);
    
    // while(!Serial.available());
    // data_positions[1] = Serial.readStringUntil('\n');
    // Serial.println(data_positions[1]);
    
    // while(!Serial.available());
    // data_positions[2] = Serial.readStringUntil('\n');
    // Serial.println(data_positions[2]);
    
    // while(!Serial.available());
    // data_positions[3] = Serial.readStringUntil('\n');
    // Serial.println(data_positions[3]);

    // while(!Serial.available());
    // data_positions[4] = Serial.readStringUntil('\n');
    // Serial.println(data_positions[4]);
    
    //Serial.println(data);
    // base-waist motor
    //Serial.println(data.length());
    for(int j =0; j < 1; j ++)
    {
      data = data_positions[j];
    for (int i = 0; i < data.length(); i++) {
      chr = data[i];

      if (chr == 'a') {
        idx = 0;
        val_idx = 0;
      }
      // waist-link1 motor
      else if (chr == 'b') {
        idx = 1;
        val_idx = 0;
      }
      // link1-link2 motor
      else if (chr == 'c') {
        idx = 2;
        val_idx = 0;
      }
      // link2-gripper base motor
      else if (chr == 'd') {
        idx = 3;
        val_idx = 0;
      }
      // gripper motor
      else if (chr == 'e') {
        idx = 4;
        val_idx = 0;
      }
      // Separator
      else if (chr == ',') {
        int val = atoi(value);
        if (idx == 0) {
          //reach_goal(base_waist_servo, val);
          joint_1 = val;
        } else if (idx == 1) {
          //reach_goal(waist_link1_servo, val);
          joint_2 =  val;
        } else if (idx == 2) {
          //reach_goal(link1_link2_servo, val);
          joint_3 =  val;
        } else if (idx == 3) {
          //reach_goal(link2_gripperbase_servo, val);
          joint_4 =  val;
        } else if (idx == 4) {

          //Serial.println(val);
          if ((val > 80))
          {
            val = 80;
          }
          if (val < 0)
          {
            val = 0;
          }
          //reach_goal(gripper, val);
          gripper_1 = val;
        }

        // reset the angle
        value[0] = '0';
        value[1] = '\0';
        value[2] = '\0';
        value[3] = '\0';
        value[4] = '\0';
      }
      // Plain number
      else {
        value[val_idx] = chr;
        //Serial.print("%c ", value[val_idx]);
        val_idx++;
      }
    }
    //Serial.println("Hello, Done");
    Serial.flush();


    //interpolation

    quintic_interpolation quintic_theta_1( 0, 400, init_theta_11, joint_1, 0, 0, 0, 0);
    quintic_interpolation quintic_theta_2( 0, 400, init_theta_21, joint_2, 0, 0, 0, 0);
    quintic_interpolation quintic_theta_3( 0, 400, init_theta_31, joint_3, 0, 0, 0, 0);
    quintic_interpolation quintic_theta_4( 0, 400, init_theta_41, joint_4, 0, 0, 0, 0);


    for (int i = 0; i <= 400; i = i + 10)
    {

      int deg = (int)(quintic_theta_1.current_point(i));
      //base_servo.write(deg);
      reach_goal(base_waist_servo, deg);

      deg = (int)(quintic_theta_2.current_point(i));
      //shoulder_servo.write(deg);
      reach_goal(waist_link1_servo, deg);

      deg = (int)(quintic_theta_3.current_point(i));
      //elbow_servo.write(deg);
      reach_goal(link1_link2_servo, deg);

      deg = (int)(quintic_theta_4.current_point(i));
      //wrist_servo.write(deg);
      reach_goal(link2_gripperbase_servo, deg);

      //Serial.print(".");


    }
    reach_goal(gripper, gripper_1);
    Serial.println();
    init_theta_11 = joint_1, init_theta_21 = joint_2, init_theta_31 = joint_3, init_theta_41 = joint_4;
    Serial.println(".");


  }
  }

}

// a179,b3,c90,d90,e0,z