/*
  Analog input, analog output, serial output

  Reads an analog input pin, maps the result to a range from 0 to 255 and uses
  the result to set the pulse width modulation (PWM) of an output pin.
  Also prints the results to the Serial Monitor.

  The circuit:
  - potentiometer connected to analog pin 0.
    Center pin of the potentiometer goes to the analog pin.
    side pins of the potentiometer go to +5V and ground
  - LED connected from digital pin 9 to ground through 220 ohm resistor

  created 29 Dec. 2008
  modified 9 Apr 2012
  by Tom Igoe

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogInOutSerial
*/
#include <Arduino.h>

const int analogInPin0 = A0;
const int analogInPin1 = A1;
const int analogInPin2 = A2;

int sensorValue0 = 0; // value read from the pot
int outputValue0 = 0; // value output to the PWM (analog out)
int sensorValue1 = 0; // value read from the pot
int outputValue1 = 0; // value output to the PWM (analog out)
int sensorValue2 = 0; // value read from the pot
int outputValue2 = 0; // value output to the PWM (analog out)

void setup()
{
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);

  pinMode(analogInPin0, INPUT);
  pinMode(analogInPin1, INPUT);
  pinMode(analogInPin2, INPUT);
}

void loop()
{

  // read the analog in value:
  sensorValue0 = analogRead(analogInPin0);
  sensorValue1 = analogRead(analogInPin1);
  sensorValue2 = analogRead(analogInPin2);

  outputValue0 = map(sensorValue0, 0, 1023, 0, 100);
  outputValue1 = map(sensorValue1, 0, 1023, 0, 100);
  outputValue2 = map(sensorValue2, 0, 1023, 0, 100);

  // print the results to the Serial Monitor:
  Serial.print(String(outputValue0) + ",");
  Serial.print(String(outputValue1) + ",");
  Serial.print(String(outputValue2));
  Serial.println();

  delay(20);
}
