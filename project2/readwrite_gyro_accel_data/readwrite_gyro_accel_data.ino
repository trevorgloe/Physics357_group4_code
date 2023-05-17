#include <SD.h>
#include<Wire.h>
const int MPU_addr = 0x68; // I2C address of the MPU-6050
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;


void setup()

{

  Serial.begin(9600);

  pinMode(10, OUTPUT); //10 is the critical pin for SD card shield

  SD.begin(10);

  pinMode(3, OUTPUT);
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  File out;
  out = SD.open("data.txt", FILE_WRITE);
  out.println("time,AcX,AcY,GyZ"); //print header of text file for reference
  out.close();

  pinMode(7, INPUT); // initialize this pin to read the switch position

}



void loop()

{

  //int switch;

  Serial.println(digitalRead(7));
  
  // if switch is turned, read data. the switch value is stored in the state of pin 7
  if (digitalRead(7) == HIGH) {

    File out;

    unsigned long t;

    t = millis();

    Serial.println(t);

    //Serial.print(",");

    //Serial.println(n);

    //file names must use 8.3 convention (8 character name, 3 character extension)

    out = SD.open("data.txt", FILE_WRITE);

    if (out)

    {

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
      Serial.print("AcX = "); Serial.print(AcX);
      Serial.print(" | AcY = "); Serial.print(AcY);
      Serial.print(" | GyZ = "); Serial.println(GyZ);

      out.print(t);

      out.print(",");

      //out.println(n);
      out.print(AcX);
      out.print(",");
      out.print(AcY);
      out.print(",");
      out.println(GyZ);

      out.close();

      digitalWrite(3, HIGH);

      delay(5);

      digitalWrite(3, LOW);

      //delay(10);

    }

    delay(2);

  } else{
    delay(2);
  }


}
