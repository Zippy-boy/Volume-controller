#include <Arduino.h>

const int analogInPin0 = A0;
const int analogInPin1 = A1;
const int analogInPin2 = A2;
const int analogInPin3 = A3;
const int analogInPin4 = A4;

int sensorValue0 = 0; 
int outputValue0 = 0; 
int sensorValue1 = 0; 
int outputValue1 = 0; 
int sensorValue2 = 0; 
int outputValue2 = 0;
int sensorValue3 = 0;
int outputValue3 = 0;
int sensorValue4 = 0;
int outputValue4 = 0;

void setup()
{
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);

  pinMode(analogInPin0, INPUT);
  pinMode(analogInPin1, INPUT);
  pinMode(analogInPin2, INPUT);
  pinMode(analogInPin3, INPUT);
  pinMode(analogInPin4, INPUT);
}

void loop()
{

  // read the analog in value:
  sensorValue0 = analogRead(analogInPin0);
  sensorValue1 = analogRead(analogInPin1);
  sensorValue2 = analogRead(analogInPin2);
  sensorValue3 = analogRead(analogInPin3);
  sensorValue4 = analogRead(analogInPin4);

  outputValue0 = map(sensorValue0, 0, 1023, 0, 100);
  outputValue1 = map(sensorValue1, 0, 1023, 0, 100);
  outputValue2 = map(sensorValue2, 0, 1023, 0, 100);
  outputValue3 = map(sensorValue3, 0, 1023, 0, 100);
  outputValue4 = map(sensorValue4, 0, 1023, 0, 100);

  // print the results to the Serial Monitor:
  Serial.print(String(outputValue0) + ",");
  Serial.print(String(outputValue1) + ",");
  Serial.print(String(outputValue2));
  Serial.println();

  delay(20);
}
