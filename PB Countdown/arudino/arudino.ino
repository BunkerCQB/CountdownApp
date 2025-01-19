const int TowelForks = 5;  
const int TowelTunnel = 6;  
const int BuzzerForks = 9;
const int BuzzerTunnel = 8;

int prevTowelForks = 0;
int prevTowelTunnel = 0;
int prevBuzzerForks = 0;
int prevBuzzerTunnel = 0;

int TowelStateForks = 0;
int TowelStateTunnel = 0; 
int BuzzerStateForks = 0;
int BuzzerStateTunnel = 0; 

int JumperPin = 10;

int delayTime = 1;

bool running = false;

void setup() {
	pinMode(TowelForks, INPUT);
	pinMode(TowelTunnel, INPUT);  
  pinMode(BuzzerForks, INPUT);  
	pinMode(BuzzerTunnel, INPUT);  
	pinMode(JumperPin, INPUT_PULLUP); 

	Serial.begin(9600);
}

void loop() {
	TowelStateForks = digitalRead(TowelForks);
	TowelStateTunnel = digitalRead(TowelTunnel);
  BuzzerStateForks = digitalRead(BuzzerForks);
  BuzzerStateTunnel = digitalRead(BuzzerTunnel); 
	if(TowelStateForks == HIGH && prevTowelForks == 0)
	{
		Serial.println("TowelForks");
    running = false;
	}
	prevTowelForks = TowelStateForks;

	if(TowelStateTunnel == HIGH && prevTowelTunnel == 0)
	{
		Serial.println("TowelTunnel");
    running = false;

	}
	prevTowelTunnel = TowelStateTunnel;

	if(BuzzerStateForks == HIGH && prevBuzzerForks == 0)
	{
		if (running)
    {
    	Serial.println("BuzzerForks");
      running = false;
    }
    else if (digitalRead(JumperPin))
    {
      Serial.println("Start");
      running = true;
    }
	}
	prevBuzzerForks = BuzzerStateForks;

  if(BuzzerStateTunnel == HIGH && prevBuzzerTunnel == 0)
	{
    if (running)
    {
    	Serial.println("BuzzerTunnel");
      running = false;
    }
    else if (digitalRead(JumperPin))
    {
      Serial.println("Start");
      running = true;
    }
	}
	prevBuzzerTunnel = BuzzerStateTunnel;

	delay(delayTime * 100);
}
