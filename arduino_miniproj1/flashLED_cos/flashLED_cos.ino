int c;   // declare c as an integer
void setup(){               
  c = 0;
  pinMode(2, OUTPUT);   
}
void loop(){
  int d;
  d = abs(500*cos(100.0 * 3.14 * c)); // time interval
  digitalWrite(2, HIGH);   // set the LED on
  delay(d);              // wait for interval ‘d’
  digitalWrite(2, LOW);    // set the LED off
  delay(d);              // wait for interval ‘d’
  c=c+1;
}
