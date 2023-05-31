#include <SD.h>
#include<Wire.h>
const int MPU_addr = 0x68; // I2C address of the MPU-6050
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;    // setup the variables for data taking

void setup()
{
  pinMode(10, OUTPUT);  //10 is the critical pin for SD card shield
  SD.begin(10);

  // set up pin for LED
  pinMode(3, OUTPUT);

  // setup for accelerometer
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

//print header of text file for reference
  File out;
  out = SD.open("data.txt", FILE_WRITE);
  out.println("time,AcX,AcY,GyZ");  
  out.close();

// initialize this pin to read the switch position
  pinMode(7, INPUT); 
}



void loop()

{
  
  // if switch is turned, read data. the switch value is stored in the state of pin 7
  if (digitalRead(7) == HIGH) {

    File out;
    unsigned long t;
    t = millis();   // time in milliseconds

    // open file for data taking
    out = SD.open("data.txt", FILE_WRITE);

    if (out)
    {
      // read accelerometer data
      Wire.beginTransmission(MPU_addr);
      Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
      Wire.endTransmission(false);
      Wire.requestFrom(MPU_addr, 14, true); // request a total of 14 registers
      AcX = Wire.read() << 8 | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
      AcY = Wire.read() << 8 | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
      AcZ = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
      Tmp = Wire.read() << 8 | Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
      GyX = Wire.read() << 8 | Wire.read(); // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
      GyY = Wire.read() << 8 | Wire.read(); // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
      GyZ = Wire.read() << 8 | Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

      // print data to file
      out.print(t);
      out.print(",");
      out.print(AcX);
      out.print(",");
      out.print(AcY);
      out.print(",");
      out.println(GyZ);

      // close file
      out.close();

      // flash LED
      digitalWrite(3, HIGH);
      delay(5);
      digitalWrite(3, LOW);

    }

    delay(2);

  } else{
    delay(2);
  }


}
