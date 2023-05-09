// this code works!! 

// for SD card:
#include <SD.h>

// for accelerometer: 
#include<Wire.h>
const int MPU_addr=0x68;  // I2C address of the MPU-6050
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;

void setup()
{
  Serial.begin(9600);
  // for SD card:
  pinMode(10, OUTPUT); //10 is the critical pin for SD card shield
  SD.begin(10);
  // for accelerometer:
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Serial.begin(9600);
  File out;
  out = SD.open("example.txt", FILE_WRITE);
  out.println(" t AcX AcY AcZ Tmp GyX GyY GyZ");
  out.close();
}
void loop()
{
    // for SD card:
    File out;
    unsigned long t = millis();
    
    // read accelerometer: 
    Wire.beginTransmission(MPU_addr);
    Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
    AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
    AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

    //file names must use 8.3 convention (8 character name, 3 character extension)
    out = SD.open("example.txt", FILE_WRITE);
    if (out)
      {
        out.print(t);
        out.print(" ");
        out.print(AcX);
        out.print(" ");
        out.print(AcY);
        out.print(" ");
        out.print(AcZ);
        out.print(" ");
        out.print(Tmp);
        out.print(" ");
        out.print(GyX);
        out.print(" ");
        out.print(GyY);
        out.print(" ");
        out.print(GyZ);
        out.println(" ");
        Serial.println("line saved");
        out.close();
      }
    if (Serial.available() != 0){
      while(1){
        //infinite loop to stop it 
      }
    }
    
    delay(500);
    
}
