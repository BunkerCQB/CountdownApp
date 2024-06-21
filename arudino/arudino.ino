
const int cooldownSeconds = 6 * 1000;

const int buttonPinOne = 6;  
const int buttonPinTwo = 5;  
const int ledOne = 10;

int buttonStateOne = 0;
int buttonStateTwo = 0;  

long lastPressed = -cooldownSeconds;  

void setup() {
  pinMode(buttonPinOne, INPUT);
  pinMode(buttonPinTwo, INPUT);

  pinMode(ledOne, OUTPUT);
  
  digitalWrite(ledOne, LOW);  

  Serial.begin(9600);
}

void loop() {
  // read the state of the pushbutton value:
  buttonStateOne = digitalRead(buttonPinOne);
  buttonStateTwo = digitalRead(buttonPinTwo);

  // check if the button is pressed and it's been more than 2 seconds since the last press
  if ((buttonStateOne == HIGH || buttonStateTwo == HIGH) && (millis() - lastPressed >= cooldownSeconds)) {
    // send a signal to Python via serial communication
    Serial.println("pressed");

    // update last pressed time:
    lastPressed = millis();

    digitalWrite(ledOne, HIGH);
  } 

  if (millis() - lastPressed >= cooldownSeconds) {
    digitalWrite(ledOne, LOW);
  }

  // wait for a short period of time to avoid overwhelming the serial port:
  delay(100);
}
