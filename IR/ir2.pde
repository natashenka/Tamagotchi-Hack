/* Control a Lutron Maestro light dimmer */
#define BIT_IS_SET(i, bits)  (1 << i & bits)

// LED connected to digital pin 13
const int LED_PIN = 13;
// Width of a pulse, in microseconds
const int PULSE_WIDTH = 2300;
// # of bytes per command
const int COMMAND_LENGTH = 4;    

volatile int REQUEST[]     = {0xac, 1, 0x24, 0xd7, 0x0a, 1, 0x0e, 0x09, 0x05, 0x01, 0x03, 0x88, 0x00, 0x01, 0x33, 0xc0, 0x0b, 0, 0, 0xff, 1, 0xff, 0xff, 0x55};

volatile int RC[] = {0xac, 0x0b, 0x24, 0xd7, 0x00, 0x47, 0x0, 0x17, 0x5a };
int conf[9];
int r[24];
volatile int bounce = 0;

#include <stdio.h>
               // choose the pin for the LED
int inputPin = 2;               // choose the input pin (for a pushbutton)
int val = 0;                    // variable for reading the pin status
int count;
volatile int b = 0x47;
boolean done = false;

 void suck( int sig ){
        while(digitalRead(inputPin) == sig){  
       }
 
 }
 
 int decodebuf( int* b){
   int a = 0;
   for( int i = 0; i < 8; i++){
     if( b[i] != 1 &&b[i] != 2 &&b[i] != 3){
       Serial.println("I've fallen and i can't get up");
              Serial.println(b[i]);
     }
     if( b[i] == 3)
       b[i] = 2;
     a = a + ((b[i] - 1) << i);
   }
   return a;
 }
 
 void getser(void){
   //while(Serial.available()){
   boolean gr = false;
   boolean gc = false;
   while(true){
  if(!Serial.available())
    continue;
     byte c = Serial.read();
   //Serial.println(c);
   if( c == 'R' ){
   for( int i = 0; i < 24; i++)
 {
    while(!Serial.available());
     r[i] = Serial.read();
    //Serial.println(Serial.read());
 }
 gr = true;
 Serial.println("read request");
 
 }
 
    if( c == 'C' )
 {
   for( int i = 0; i < 9; i++)
 {
   //conf[i] = Serial.read();
    while(!Serial.available());
    conf[i] = Serial.read();
   //Serial.println(Serial.read());
 }
 Serial.println("read conf");
 gc = true;
 }
 if (gr && gc)
   break;
   }
 //}
 }
boolean dec(void){
  // int i = 0;

//  getser();
  int time;
  int diff, hi, lo;
   //char buf[9];
   int buf[400];
   int cycles = 0;
   int c;
   char obuf[12];
   int i;
   //char out = 0xf0;
  // for(i = 0; i < 7; i ++ ) {
    time = millis();
  while(digitalRead(inputPin) == HIGH ){  
    if( millis() - time > 5000){
      return false;
    }
  }
  time = millis();
  
  while(digitalRead(inputPin) == LOW){

  }
   diff = millis() - time;
   time = millis();
  if( diff > 8 && diff < 12){
       
         //while(digitalRead(inputPin) == LOW ){  
       //}
       time = millis();
       while(digitalRead(inputPin) == HIGH ){  
       }
          diff = millis() - time;
          if( diff < 0){
             Serial.println("NEG");
          } 
           if( diff > 1 && diff < 6){ 
              //  Serial.println("HIT ");
              //  Serial.println(diff);
              //  Serial.println( diff);
                cycles = 0;               
                i = 0;
                while(true){
               // suck(HIGH);
                cycles++;
                time = micros();
                suck(LOW);
                lo = micros() - time;
 
                time = micros();
                if( lo > 1000){
                 // Serial.println("SMALL LO");
                 // Serial.println(lo);
                 // Serial.println(cycles);
                  //cycles = 0;
                  break;
                }
                suck(HIGH);
                hi = micros() - time;
                time = micros();
                buf[i] = hi/lo;
                i++;
               }
                Serial.println("DETECTED");
               cycles = cycles/8;
               for( i = 0; i < cycles; i++){ 
                 c = decodebuf( buf + 8*i );
                 sprintf( obuf, "%x ", c);
               
               //for( i = 0; i < 16; i++){
                  Serial.print(obuf);
               }
               cycles = 0;
               return true;
               }
          }
  else{
  
     return false;
  }
  }

void setup()
{
  pinMode(LED_PIN, OUTPUT);
   Serial.begin(9600);      // declare LED as output
  pinMode(inputPin, INPUT); 
   // pinMode(5, INPUT);
   //  attachInterrupt(1, blink, FALLING);
  //  getser();
  //size(400, 300); 

  // set inital background:
//  background(0);


}

/* Modulate pin at 39 kHz for give number of microseconds */
void off(int pin, int time) {
  static const int period = 25;
  // found wait_time by measuring with oscilloscope
// static const int wait_time = 12;  

  for (time = time/period; time > 0; time--) {
    digitalWrite(pin, HIGH);
    delayMicroseconds(9);
    digitalWrite(pin, LOW);
    delayMicroseconds(9);
  }
}



/* Leave pin off for time (given in microseconds) */
void on(int pin, int time) {
  digitalWrite(pin, LOW);
  delayMicroseconds(time);
}

/* Send a byte over the IR LED */
void send_byte(int bits) {
  for (int i = 0; i < 8; i++)
  {
    if (BIT_IS_SET(i, bits)) {
         off(LED_PIN, 500);
      on(LED_PIN, 1270);   

   

    } else {
     
       off(LED_PIN, 500);
      on(LED_PIN, 675);
    


    }
  }
}

/* Send a full command */
void command(volatile int bytes[], int len) {
  
int sum = 0;
  for (int i = 0; i < len -1; i++) {
    send_byte(bytes[i]);
    sum = sum + bytes[i];
  }
  send_byte(sum%256);
  off(LED_PIN, 1200); //check if not working
  on(LED_PIN, 0);
}


void loop()
{

  /*if(!done){
    getser();
    done = true;
  } */ 



while(!dec()){}

 //if( digitalRead( 5 ) == HIGH)

  do{
  off(LED_PIN, 9500);
  on(LED_PIN, 2500);
  command(REQUEST, 24);
  }while(!dec());
  
   do{
  off(LED_PIN, 9500);
  on(LED_PIN, 2500);
  command(RC, 9);
  }while(!dec());
//  delay(10000);
//  dec();
}


   // Serial.println("yes, i do enjoy  being interrupted" );


