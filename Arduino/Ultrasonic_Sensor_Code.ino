/*
Pin 13 Triggers the Pulse (Yellow lead)
Pin 10 Recieves the Echo  (Orange lead)
*/

const int Trig_pin =  13;   // pin for triggering pulse
const int Echo_pin = 10;     // pin for recieving echo
long duration;
long distance;


int irReader = 1; // the analog input pin for the ir reader
int irVal = 0; // stores value from Ir reader

int irReader2 = 2; // the analog input pin for the ir reader
int irVal2 = 0; // stores value from Ir reader

void setup() {
  Serial.begin(9600);
 // Serial.println ("Starting");
  // initialize the pulse pin as output
  pinMode(Trig_pin, OUTPUT);      
  // initialize the echo_pin pin as an input:
  pinMode(Echo_pin, INPUT);     
  

}

void loop(){
  digitalWrite(Trig_pin, LOW);
  delayMicroseconds(2);
  digitalWrite(Trig_pin, HIGH);
  delayMicroseconds(2);
  digitalWrite(Trig_pin, LOW);
  duration = pulseIn(Echo_pin,HIGH);
  distance = duration/58.138;
  //Serial.println("Ultrasonic 1");   
  Serial.println(distance, DEC);
  
  
  irVal = analogRead(irReader); // read the value from the ir sensor
  int irValue = 600 - irVal;
  irValue = irValue / 2.5;
 // Serial.println("Infrared 1");    
  Serial.println(irValue);
 
  irVal2 = analogRead(irReader2); // read the value from the ir sensor
  int irValue2 = 600 - irVal2;
  irValue2 = irValue2 / 2.5;
 // Serial.println("Infrared 2");    
  Serial.println(irValue2); 
 
  
  delay(450);
}
