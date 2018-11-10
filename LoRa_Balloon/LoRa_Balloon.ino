/*
    Hafidh Satyanto
    Arduino Balloon Code

    Receives Serial strings from Raspberry Pi over 9600 baud then sends it over-the-air - all processing over
    what to send, processing the data, parsing, or doing any processes based on the string data is done on
    the Raspberry Pi itself - the Arduino is here just as a terminal to send whatever over the LoRa antenna.


    So:
    1. Raspberry Pi connects to all sensors and sends a string through the serial port
    2. This ino sketch reads the serial port and sends it over-the-air through LoRa

    Again - any processing is done on the Raspberry Pi of the ground station and the balloon.

    This ino sketch literally just passes through anything that is inside the serial port
    and sends it over the air.

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
  
  while (Serial.available()) {          /*  Check for anything on the serial port  */
    delay(1);
    char c = Serial.read();
    readString += c;
  }
  readString.trim();
  if (readString.length() > 0) {
    char Packet[PacketLength];
    itoa(PacketCounter++, Packet, 10);
    readString.toCharArray(Packet, PacketLength);
    delay(10);
    rf95.send((uint8_t *)Packet, PacketLength);

    delay(10);
    rf95.waitPacketSent();
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);

    if (rf95.waitAvailableTimeout(500))
    {
      if (rf95.recv(buf, &len))
      {
        Serial.print((char*)buf);
        /*Serial.print("RSSI: ");    /* The balloon LoRa doesn't need to report the RSSI to the rasperry pi...
        Serial.println(rf95.lastRssi(), DEC);*/
      }
    }

    readString = "";
  }
}
