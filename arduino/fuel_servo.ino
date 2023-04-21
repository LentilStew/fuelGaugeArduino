#include <Servo.h>

#define FUEL_LEFT_CAPACITY 0
#define FUEL_RIGHT_CAPACITY 1
#define FUEL_LEFT_QUANTITY 2
#define FUEL_RIGHT_QUANTITY 3

int fuel_left_cap = 0;
int fuel_right_cap = 0;

Servo left_fuel_servo;
Servo right_fuel_servo;

#define MAX_ANGLE 200
void setup() {
  Serial.begin(9600);   
  left_fuel_servo.attach(10); // attach left servo to pin 10
  right_fuel_servo.attach(11); // attach right servo to pin 11
}

void loop() {
  if (Serial.available() < 0) {
    return;
  }

  String inputString = Serial.readStringUntil('\n');
  
  int commaIndex = inputString.indexOf(',');
  
  if (commaIndex <= 0) {
    return;
  }

  long int key = inputString.substring(0, commaIndex).toInt();
  long int value = inputString.substring(commaIndex + 1).toInt();
  
  Serial.println("FUEL_LEFT_CAPACITY");
  Serial.println(key);

  Serial.println("FUEL_LEFT_QUANTITY");
  Serial.println(value);

  long int new_angle;
  
    switch (key) {
     case FUEL_LEFT_CAPACITY:
        fuel_left_cap = value;
        break;

    case FUEL_RIGHT_CAPACITY:
      fuel_right_cap = value;

      break;

    case FUEL_LEFT_QUANTITY:
      if(fuel_left_cap <= 0){break;}
      Serial.println("Servo izquiero ");
      new_angle = (int)((value * MAX_ANGLE) / fuel_left_cap);
      Serial.println(new_angle);
      
      left_fuel_servo.write(new_angle);
      break;

    case FUEL_RIGHT_QUANTITY:
      if(fuel_right_cap <= 0){break;}
      Serial.println("Servo derecho ");
      
      new_angle = (int)((value * MAX_ANGLE) / fuel_right_cap);
      Serial.println(new_angle);
      
      right_fuel_servo.write(new_angle);
      break;

    default:
        
      Serial.println("invalid code");
      break;
  }
   
}
