int c;
void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  c = 0;
}

void loop() {
  Serial.print("running");
  if (c%6 == 0){
    Serial.print("green");
    if (digitalRead(2) == HIGH){
      digitalWrite(2, LOW);
    } else if (digitalRead(2) == LOW){
      digitalWrite(2, HIGH);
    }
  }
  if (c%7 == 0){
    Serial.print("red");
    if (digitalRead(3) == HIGH){
      digitalWrite(3, LOW);
    } else if (digitalRead(3) == LOW){
      digitalWrite(3, HIGH);
    }
  }
  c++;
  delay(70);
  Serial.println(c);
}
