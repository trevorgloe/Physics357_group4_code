// this code works!! 

#include <SD.h>
void setup()
{
  Serial.begin(9600);
  pinMode(10, OUTPUT); //10 is the critical pin for SD card shield
  SD.begin(10);
}
void loop()
{
    File out;
    int n;
    unsigned long t;
    t = millis();
    n = random(1,100);
    Serial.print(t);
    Serial.print(",");
    Serial.println(n);
    //file names must use 8.3 convention (8 character name, 3 character extension)
    out = SD.open("example.txt", FILE_WRITE);
    if (out)
      {
    out.print(t);
    out.print(",");
    out.println(n);
    out.close();
      }
    /*if (Serial.available() != 0){
      out.close();
      while(1){
        //infinite loop to stop it 
      }
    }
    */
    delay(500);
    
}
