/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led = 13;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);
    digitalWrite(led, HIGH); 
  delay(10000);  

}

// the loop routine runs over and over again forever:
void loop() {
   // turn the LED on (HIGH is the voltage level)
  digitalWrite(led, HIGH);  
  delay(1000);               // wait for a second
 // digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW

  for(int i = 0; i < 35; i++){
      digitalWrite(led, HIGH);
      delay(5); 
      digitalWrite(led, LOW);  
           delay(5); 
  }
    digitalWrite(led, HIGH);
  while(true){}


}
