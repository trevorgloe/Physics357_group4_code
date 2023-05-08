#include <SD.h>
void setup()
{
  Serial.begin(9600);
  pinMode(10, OUTPUT); //10 is the critical pin for SD card shield
  SD.begin(10);
  pinMode(5, OUTPUT);
}
void loop()
{
    File f;
    int n;
    unsigned long t;
    t = millis();
    n = random(1,100);
    Serial.print(t);
    Serial.print(",");
    Serial.println(n);
    //file names must use 8.3 convention (8 character name, 3 character extension)
    out = SD.open("log_random.txt", FILE_WRITE);
    if (out)
      {
      f.print(t);
      f.print(",");
      f.println(n);
      f.close();
      digitalWrite(5,HIGH);
      delay(100);
      digitalWrite(5,LOW);
      delay(100);
      }
    delay(500);
}
