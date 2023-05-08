
// for SD card:
#include<SD.h>
// for accelerometer:
#include<Wire.h>
const int MPU_addr=0x68;
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ; void setup(){
Wire.begin();
Wire.beginTransmission(MPU_addr);
// PWR_MGMT_1 register
Wire.write(0x6B);
// set to zero (wakes up the GY-521)
Wire.write(0); 
Wire.endTransmission(true); 
Serial.begin(9600);

// print column headers to SD card file
File f;   // SD card file
f = SD.open("accel_data.csv", FILE_WRITE);    // file name on SD card
f.println("AcX AcY AcZ Tmp GyX GyY GyZ");
f.close();

pinMode(10, OUTPUT); //10 is the critical pin for SD card shield
SD.begin(10);
}

void loop(){

// getting accelerometer data:
Wire.beginTransmission(MPU_addr);
Wire.write(0x3B);
Wire.endTransmission(false);
Wire.requestFrom(MPU_addr,14,true);
AcX=Wire.read()<<8|Wire.read();
AcY=Wire.read()<<8|Wire.read();
AcZ=Wire.read()<<8|Wire.read();
Tmp=Wire.read()<<8|Wire.read();
GyX=Wire.read()<<8|Wire.read();
GyY=Wire.read()<<8|Wire.read();
GyZ=Wire.read()<<8|Wire.read(); 

// writing data to SD card:
File f;   // SD card file
f = SD.open("accel_data.csv", FILE_WRITE);    // file name on SD card
 if (f)
      {
f.print(AcX); 
f.print(" "); 
f.print(AcY); 
f.print(" "); 
f.print(AcZ);
f.print(" "); 
f.print(Tmp/340.00+36.53); 
f.print(" "); 
f.print(GyX);
f.print(" "); 
f.print(GyY);
f.print(" "); 
f.println(GyZ);
f.close();

/* //add back in for indicator
// indicator will blink light as each line is written to file 
digitalWrite(5,HIGH);
delay(100);
digitalWrite(5,LOW);
delay(100);
*/ 
      }


/* add this back in if you want to print to serial too 
Serial.print(" "); 
Serial.print(AcX); 
Serial.print(" "); 
Serial.print(AcY); 
Serial.print(" "); 
Serial.print(AcZ);
Serial.print(" "); 
Serial.print(Tmp/340.00+36.53); 
Serial.print(" "); 
Serial.print(GyX);
Serial.print(" "); 
Serial.print(GyY);
Serial.print(" "); 
Serial.println(GyZ);
*/
delay(333); }
