const int buttonPinOne = 5;  
const int buttonPinTwo = 6;  
const int startPin = 9;
const int endPin = 8;

int prevButtonStateOne = 0;
int prevButtonStateTwo = 0;
int prevStartState = 0;
int prevEndState = 0;

int buttonStateOne = 0;
int buttonStateTwo = 0; 
int startState = 0;
int endState = 0; 

int delayTime = 1;

void setup() {
	pinMode(buttonPinOne, INPUT);
	pinMode(buttonPinTwo, INPUT);  
  pinMode(startPin, INPUT);  
	pinMode(endPin, INPUT);  


	Serial.begin(9600);
}

void loop() {
	buttonStateOne = digitalRead(buttonPinOne);
	buttonStateTwo = digitalRead(buttonPinTwo);
  startState = digitalRead(startPin);
  endState = digitalRead(endPin); 

	if(buttonStateOne == HIGH && prevButtonStateOne == 0)
	{
		Serial.println("Left");
	}
	prevButtonStateOne = buttonStateOne;

	if(buttonStateTwo == HIGH && prevButtonStateTwo == 0)
	{
		Serial.println("Right");
	}
	prevButtonStateTwo = buttonStateTwo;

	if(startState == HIGH && prevStartState == 0)
	{
		Serial.println("Start");
	}
	prevStartState = startState;

  if(endState == HIGH && prevEndState == 0)
	{
		Serial.println("End");
	}
	prevEndState = endState;

	delay(delayTime * 100);
}
