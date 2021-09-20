#include <Servo.h>

int x = 90;
int y = 90;
int dx = 0;
int dy = 0;

Servo servoX;  // on pin 9
Servo servoY;  // on pin 10

char* in     = "0,0";
String input = "0,0"

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  servoX.attach(9);  // attaches the servo on pin 9 to the servo object
  servoY.attach(10);
  servoX.write(90);
  servoY.write(90);
}

void loop() {
  while(Serial.available() == 0)
  {}

  input = Serial.readString();
  dx = int(input[0]);
  dy = int(input[2]);
  Serial.println(dx+","+dy);


  if(dx==2)
  {
    dx = -1;
  }
  if(dy==2)
  {
    dy = -1;
  }

  if((x + dx<=180)&&(x + dx>=0))
  {
    x += dx;
  }
  if((y + dy<=180)&&(y + dy>=0))
  {
    y += dy;
  }


  servoX.write(x);
  servoY.write(y);                 // sets the servo position according to the scaled value
}
