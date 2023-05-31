// ultrasonic sensor: 
int trigPin = 5;    // TRIG pin
int echoPin = 4;    // ECHO pin
float time_us; 
float distance = 24.6 * 2;    // cm, distance to target times 2
float duration_us;
float c;

// LCD: 
#include <LiquidCrystal.h>
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// temp sensor: 
#include <Adafruit_Sensor.h>
#include <dht.h>
dht DHT;
#define DHT11_PIN 13

void setup() {
  // begin serial port
  Serial.begin (9600);

  // ultrasonic sensor: 
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // LCD:
  lcd.begin(16, 2);
  lcd.print("begin! <3");
  delay(3000);
}

void loop() {
  //ultrasonic data: 
/*  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);*/
  float d = 0;
  // measure duration of pulse from ECHO pin
  for (int i=0; i < 30; i++){
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    d = d + pulseIn(echoPin, HIGH);
    /*Serial.print(pulseIn(echoPin, HIGH));
    Serial.print("i=");
    Serial.print(i);
    Serial.print("; d=");
    Serial.println(d);*/
    delay(100);
  }
  duration_us = d/30.0;
//Serial.print("duration avg= ");
  //Serial.println(duration_us);
  // calculate speed of sound: 
  c = distance/duration_us * pow(10, 4);

  // Temperature sensor
  int chk = DHT.read11(DHT11_PIN);
  /*Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  delay(1000);*/

 // LCD: 
 lcd.setCursor(0,0);
 lcd.print("c=");
 lcd.print(c);
 lcd.print("m/s");
 lcd.setCursor(0,1);
 lcd.print("temp=");
 lcd.print(DHT.temperature);
 lcd.print(" C");

}
