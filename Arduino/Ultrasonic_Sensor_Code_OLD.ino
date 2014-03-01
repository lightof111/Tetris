/*
Pin 13 Triggers the Pulse (Yellow lead)
Pin 10 Recieves the Echo  (Orange lead)
*/

const int Trig_pin =  13;   // pin for triggering pulse
const int Echo_pin = 10;     // pin for recieving echo
long duration;
long distance;

void setup() {
  Serial.begin(9600);
  Serial.println ("Starting");
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
  Serial.println("Distance: ");   
  Serial.println(distance, DEC);
}

