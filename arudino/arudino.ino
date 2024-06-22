#include <IRremote.h>

const int cooldownSeconds = 2 * 1000;

const int buttonPinOne = 5;  
const int buttonPinTwo = 6;  
const int irPin = 3;

int buttonStateOne = 0;
int buttonStateTwo = 0;  

long lastPressed = -cooldownSeconds;

IRrecv irrecv(irPin);
decode_results results;

void setup() {
  pinMode(buttonPinOne, INPUT);
  pinMode(buttonPinTwo, INPUT);  

  Serial.begin(9600);

  irrecv.enableIRIn(); // Start the IR receiver
}

void loop() {
  buttonStateOne = digitalRead(buttonPinOne);
  buttonStateTwo = digitalRead(buttonPinTwo);

  if (irrecv.decode(&results) && (millis() - lastPressed >= cooldownSeconds)) {
    Serial.println("signal");
    lastPressed = millis();
    irrecv.resume(); // Receive the next value
  }

  if ((buttonStateOne == HIGH || buttonStateTwo == HIGH) && (millis() - lastPressed >= cooldownSeconds)) {
    if (buttonStateOne == HIGH) {
      Serial.println("red");
    }
    if (buttonStateTwo == HIGH) {
      Serial.println("blue");
    }

    lastPressed = millis();
  } 

  delay(100);
}
