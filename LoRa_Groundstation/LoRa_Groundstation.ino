/*
    Hafidh Satyanto
    Arduino Groundstation Code

    Receives over-the-air strings from Raspberry Pi over 9600 baud then prints it in serial port.
    Not sure whether or not to connect the groundstation into a Raspberry Pi for further processing...

    So:
    1.  Arduino connects to antenna and amplifier and periodically checks if receiving anything
    2.  This ino sketch translates any over-the-air strings into the serial port
    3.  The user can 'type' and input directly to the serial port, in which this would send out an
        over the air command to the balloon.

    This ino sketch literally just receives any over-the-air strings and prints it in the serial port.

*/

#include <SPI.h>
#include <RH_RF95.h>

#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3
#define RF95_FREQ 915.0

RH_RF95 rf95(RFM95_CS, RFM95_INT);
String readString;
int PacketLength = 40;
int PacketCounter = 0;
String PacketString;
char packet;

void setup() {
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  Serial.begin(9600);
  while (!Serial) {
    delay(1);
  }
  delay(500);
  digitalWrite(RFM95_RST, LOW);
  delay(100);
  digitalWrite(RFM95_RST, HIGH);
  delay(100);
  while(!rf95.init()) {
    Serial.println("LoRa radio initialization failed.");
    while (1);
  }
  Serial.println("LoRa radio initialization OK!");
  rf95.setTxPower(23, false);
}

void loop() {
  delay(500);

  /*  Keyboard input command check */
  while (Serial.available()) {          /*  Check for anything on the serial port */
    delay(1);
    char c = Serial.read();
    readString += c;
  }
  readString.trim();
  if (readString.length()>0 && readString.substring(1,5)!="RSSI:") {  /* Check what is on the serial port */
    char Packet[PacketLength];
    itoa(PacketCounter++, Packet, 10);
    readString.toCharArray(Packet, PacketLength);
    delay(10);
    rf95.send((uint8_t *)Packet, PacketLength);   /* If it finds anything not RSSI or empty, send it */

    delay(10);
    rf95.waitPacketSent();
    readString = "";
  }

  /* Check any incoming messages */
  if (rf95.available())
  {                                           /* If there is an incoming message, print in serial port */
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);

    /* HighJack 4 Specialized Packet Parser */
    if(rf95.recv(msg, &length))
    {
      packet = msg
      PacketString = String(packet)
    }

    /*if(rf95.recv(buf, &len))
    {
      Serial.println((char*)buf);
      Serial.print("RSSI: ");
      Serial.println(rf95.lastRssi(), DEC);
    }*/
  }
}
