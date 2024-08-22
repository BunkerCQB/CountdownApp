const int buttonPinOne = 5;  
const int buttonPinTwo = 6;  

int prevButtonStateOne = 0;
int prevButtonStateTwo = 0;

int buttonStateOne = 0;
int buttonStateTwo = 0;  

int delayTime = 1;

void setup() {
	pinMode(buttonPinOne, INPUT);
	pinMode(buttonPinTwo, INPUT);  

	Serial.begin(9600);
}

void loop() {
	buttonStateOne = digitalRead(buttonPinOne);
	buttonStateTwo = digitalRead(buttonPinTwo);

	if(buttonStateOne == HIGH && prevButtonStateOne == 0)
	{
		Serial.println("red");
	}
	prevButtonStateOne = buttonStateOne;

	if(buttonStateTwo == HIGH && prevButtonStateTwo == 0)
	{
		Serial.println("blue");
	}
	prevButtonStateTwo = buttonStateTwo;

	delay(delayTime * 100);
}
