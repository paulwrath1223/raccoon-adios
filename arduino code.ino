#include <Wire.h>
// #include <LiquidCrystal_I2C.h>
#include <Servo.h>

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;


float x = 90.0;
float y = 90.0;

int dx = 0;
int dy = 0;

char cx;
char cy;

const int pFactor = 300; // represents the inverse of the movement speed. (higher is slower)



// LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

Servo servoX;  // on pin 9
Servo servoY;  // on pin 10

void setup() {
    Serial.begin(115200);
    // lcd.init();                      // initialize the lcd
    // lcd.backlight();
    servoX.attach(9);  // attaches the servo on pin 9 to the servo object
    servoY.attach(10);
    servoX.write(x);
    servoY.write(y);
}

void loop() {
    recvWithEndMarker();
    updateDxDy();

    if(dx==2)
    {
      dx = -1;
    }
    if(dy==2)
    {
      dy = -1;
    }

    if((x + (float(dx)/pFactor) <= 180.0 ) && (x + (float(dx)/pFactor) >= 0.0))
    {
      x += (float(dx)/pFactor);
    }
    if((y + (float(dy)/pFactor) <= 180.0) && (y + (float(dy)/pFactor) >= 0.0))
    {
      y += (float(dy)/pFactor);
    }

    // lcd.setCursor(0,0);
    // lcd.print("dx: ");
    // lcd.setCursor(5,0);
    // lcd.print(dx);
    // lcd.setCursor(0,1);
    // lcd.print("dy: ");
    // lcd.setCursor(5,1);
    // lcd.print(dy);

    servoX.write(int(x));
    servoY.write(int(y));                 // sets the servo position according to the scaled value
}

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}

void updateDxDy() {
    if (newData == true) {
        cx = receivedChars[0];
        cy = receivedChars[1];

        dx = String(cx).toInt();
        dy = String(cy).toInt();
        newData = false;
    }
}















