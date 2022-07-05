const int buttonCount = 4;
int buttonPins[buttonCount] = {2, 4, 7, 8}; ///Digital.
int potPin = 5; ///Analog.
int buttonReads[buttonCount];

void setup()
{
  Serial.begin(9600);
  for (int i = 0; i < buttonCount; i++) {
    pinMode(buttonPins[i], INPUT);  
  }
  
  pinMode(potPin, INPUT);
  ///2 may mean 2 analog/digital
  ///I want 2 digital => call digitalRead(2).
}

void loop()
{
  int potRead = analogRead(potPin);
  
  int buttonMask = 0;
  
  for (int i = 0; i < buttonCount; i++) {
    buttonReads[i] = digitalRead(buttonPins[i]);
    buttonMask += (buttonReads[i] << i);
  }

  Serial.print(potRead);
  Serial.print(" ");
  Serial.print(buttonMask);
  Serial.print("\n");
  
  delay(25);
}
