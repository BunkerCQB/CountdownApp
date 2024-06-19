
const int buttonPinOne = 6;  
const int buttonPinTwo = 5;  
const int ledOne = 10;
const int ledTwo = 9;

int buttonStateOne = 0;
int buttonStateTwo = 0;  

long lastPressed = -(10 * 1000);  

void setup() {
  pinMode(buttonPinOne, INPUT);
  pinMode(buttonPinTwo, INPUT);

  pinMode(ledOne, OUTPUT);
  pinMode(ledTwo, OUTPUT);
  
  digitalWrite(ledOne, HIGH);  
  digitalWrite(ledTwo, HIGH);  

  Serial.begin(9600);
}

void loop() {
  // read the state of the pushbutton value:
  buttonStateOne = digitalRead(buttonPinOne);
  buttonStateTwo = digitalRead(buttonPinTwo);

  // check if the button is pressed and it's been more than 2 seconds since the last press
  if ((buttonStateOne == HIGH || buttonStateTwo == HIGH) && (millis() - lastPressed >= 10 * 1000)) {
    // send a signal to Python via serial communication
    Serial.println("pressed");

    // update last pressed time:
    lastPressed = millis();

    digitalWrite(ledOne, LOW);
    digitalWrite(ledTwo, LOW);
  } 

  if (millis() - lastPressed >= 10 * 1000) {
    digitalWrite(ledOne, HIGH);
    digitalWrite(ledTwo, HIGH);
  }

  // wait for a short period of time to avoid overwhelming the serial port:
  delay(100);
}