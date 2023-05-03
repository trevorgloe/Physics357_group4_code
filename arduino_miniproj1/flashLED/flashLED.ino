int c;
oid setup() {
  // put your setup code here, to run once:
 // int delay = 2000;
  pinMode(2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(2, HIGH);
  delay(20);
  digitalWrite(2, LOW);
  delay(20);
}
