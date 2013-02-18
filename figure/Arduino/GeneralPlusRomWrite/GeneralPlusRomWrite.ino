#define DATAOUT 11//MOSI
#define DATAIN  12//MISO 
#define SPICLOCK  13//sck
#define SLAVESELECT 10//ss

//opcodes
#define WREN  6
#define WRDI  4
#define RDSR  5
#define WRSR  1
#define READ  3
#define WRITE 2

byte eeprom_output_data;
byte eeprom_input_data=0;
byte clr;
int address=0;
long int once = 0;
//data buffer
char buffer [128];

void fill_buffer()
{
  for (int I=0;I<128;I++)
  {
    buffer[I]=I;
  }
}

char spi_transfer(volatile char data)
{
  SPDR = data;                    // Start the transmission
  while (!(SPSR & (1<<SPIF)))     // Wait the end of the transmission
  {
  };
  return SPDR;                    // return the received byte
}

void setup()
{
  Serial.begin(115200);
 //   Serial.print("serial test \r\n");
  pinMode(DATAOUT, OUTPUT);
  pinMode(DATAIN, INPUT);
  pinMode(SPICLOCK,OUTPUT);
  //  pinMode(13,OUTPUT);
  pinMode(SLAVESELECT,OUTPUT);
  digitalWrite(SLAVESELECT,HIGH); //disable device
      // Serial.print("serial test 2 \r\n");
   //SPCR = 01010000;
   SPCR = 0x50;
      //  Serial.print("serial test 3\r\n");
  //interrupt disabled,spi enabled,msb 1st,master,clk low when idle,
  //sample on leading edge of clk,system clock/4 rate (fastest)
 // SPCR = (1<<SPE)|(1<<MSTR);
  clr=SPSR;
  clr=SPDR;
  delay(10);

      //  Serial.print("serial test 4\r\n");
}

byte read_eeprom(int EEPROM_address)
{
  //READ EEPROM
  int data, data1, data2;
  long int j;
     Serial.print("START\n");
  digitalWrite(SLAVESELECT,LOW);
  spi_transfer(0x03); //transmit read opcode
  spi_transfer(0x00); 
  spi_transfer(0x00);  
  spi_transfer(0x00); 
   delay(50);
   
 //    spi_transfer(0x00); 
 // spi_transfer(0x00);  
  //  spi_transfer(0x00); 
 
 // spi_transfer((char)(EEPROM_address>>8));   //send MSByte address first
 // spi_transfer((char)(EEPROM_address));      //send LSByte address
       for(j = 0; j < 0x80000; j++){
 // data1 = spi_transfer(0x00);
  //data = spi_transfer(0x00); //get data byte
  //data2 = spi_transfer(0x00); //get data byte
    //data = spi_transfer(0xFF); 
   //    if( j%16 == 0){
     //      Serial.print("\n");
          // Serial.print(j, HEX);
          // Serial.print( ": ");
       //}
       // delay(50);
        data = spi_transfer(0x00);
         //Serial.print("0x");
         Serial.print((char)data);
         
         //Serial.print(" ");
       
       } 
  digitalWrite(SLAVESELECT,HIGH); //release chip, signal end transfer
 //   Serial.print(data,HEX);
   //   Serial.print(" ");k
     //   Serial.print(data2,HEX);
       //   Serial.print(" ");
         //   Serial.print(data1,HEX);
           //   Serial.print(" \r\n");
  // Serial.print(" \n DONE");
  return data;
}

void loop()
{
 long int i;
 byte b[256];
 Serial.println("ready");
 
 for(i = 0; i < 256; i++){
   b[i] = Serial.parseInt();
 }
 // Serial.print("loop 1\r\n");
 if((once %256) == 0){
  // eeprom_output_data = read_eeprom(address);
   digitalWrite(SLAVESELECT,LOW);
  spi_transfer(0x06); //transmit read opcode
   digitalWrite(SLAVESELECT,HIGH);
   digitalWrite(SLAVESELECT,LOW);
  spi_transfer(0xd8); 
  spi_transfer(once / 256);  
  spi_transfer(0x00); 
   spi_transfer(0x00);
    digitalWrite(SLAVESELECT,HIGH); 
     delay(1000);
 }
 

       digitalWrite(SLAVESELECT,LOW);
  spi_transfer(0x06); //transmit read opcode
   digitalWrite(SLAVESELECT,HIGH);
       digitalWrite(SLAVESELECT,LOW);
  spi_transfer(0x2); 
  spi_transfer(once / 256);  
  spi_transfer(once % 256); 
   spi_transfer(0);
   for(i = 0; i < 256; i++){
   spi_transfer(b[i]);
 }
    digitalWrite(SLAVESELECT,HIGH); 
    
    once++;
  
  
  
  

   
// once = 100;
//    Serial.print("loop 2\r\n");
 // Serial.print(eeprom_output_data,DEC);
  //Serial.print('\n',BYTE);
  //address++;
  //if (address == 128)
    //address = 0;
 // delay(500); //pause for readability
  

       // digitalWrite(SPICLOCK, HIGH);
     //          digitalWrite(DATAOUT, HIGH);
}


