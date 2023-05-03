void setup()
{
  pinMode(2, OUTPUT);  // enable output on the LED pin
}

void loop()
{
  int rate = analogRead(A0); // read the analog input
  digitalWrite(2, HIGH);   // set the LED on
  delay(rate);             // wait duration dependent on light level
  digitalWrite(2, LOW);    // set the LED off
  delay(rate);             // wait again
}
