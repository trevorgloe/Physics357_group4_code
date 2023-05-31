/*
 * Created by ArduinoGetStarted, https://arduinogetstarted.com
 *
 * Arduino - Ultrasonic Sensor HC-SR04
 *
 * Wiring: Ultrasonic Sensor -> Arduino:
 * - VCC  -> 5VDC
 * - TRIG -> Pin 9
 * - ECHO -> Pin 8
 * - GND  -> GND
 *
 * Tutorial is available here: https://arduinogetstarted.com/tutorials/arduino-ultrasonic-sensor
 */

int trigPin = 5;    // TRIG pin
int echoPin = 4;    // ECHO pin

float time_us; 
float distance = 24.6 * 2;    // cm
float duration_us;
float c;
void setup() {
  // begin serial port
  Serial.begin (9600);

  // configure the trigger pin to output mode
  pinMode(trigPin, OUTPUT);
  // configure the echo pin to input mode
  pinMode(echoPin, INPUT);
}

void loop() {
  // generate 10-microsecond pulse to TRIG pin
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // measure duration of pulse from ECHO pin
  duration_us = pulseIn(echoPin, HIGH);
  c = distance/duration_us*pow(10,4);

  // calculate the distance
 

  // print the value to Serial Monitor
  /*Serial.print("duration: ");
  Serial.print(duration_us);
  Serial.println(" us");
  Serial.print("distance: ");
  Serial.print(distance_cm);
  Serial.println(" cm");*/
  Serial.print("c = ");
  Serial.println(c);

  delay(1000);
}