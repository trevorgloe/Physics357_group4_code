#include <OzIDManager.h>
#include <OzGyroscopeSensor.h>
 
OzIDManager* manager;
OzGyroscopeSensor* mpu6050;
 
void setup()
{
  Serial.begin(115200);
 
  manager = new OzIDManager;
  manager->_sendACK = true;
  manager->_checksum = true;
 
  OzCommunication::setIDManager(manager);
 
  mpu6050 = new OzGyroscopeSensor(); 
 
  int x=1;
  manager->sendLinkSetup();
  manager->PrintWelcomeLine(mpu6050, x++, "MyGyroscope");
}
 
void loop()
{
    OzCommunication::communicate();
    mpu6050->ownLoop();
}
