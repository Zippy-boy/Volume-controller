#include <Arduino.h>

const int analogInPin0 = A0;

void setup()
{
  Serial.begin(9600);
  pinMode(analogInPin0, INPUT);
}

void loop()
{
  int sensorValue0 = analogRead(analogInPin0);
  int mappedValue = map(sensorValue0, 0, 1023, 0, 100);

  
  Serial.print(mappedValue);
  Serial.print(", 0, 0");      
  Serial.println();

  delay(20);
}
