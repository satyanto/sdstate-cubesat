/*
    Hafidh Satyanto
    Arduino Transmitter Code

    Receives Serial strings from Raspberry Pi over 9600 baud then sends it over-the-air - all processing over
    what to send, processing the data, parsing, or doing any processes based on the string data is done on
    the Raspberry Pi itself - the Arduino is here just as a terminal to send whatever over the LoRa antenna.

*/

#include <SPI.h>
#include <RH_RF95.h>

#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3
#define RF95_FREQ 915.0
RH_RF95 rf95(RFM95_CS, RFM95_INT);
String readString;

void setup() {
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  Serial.begin(9600);
  while (!Serial) {
    delay(1);
  }

  delay(100);

  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while(!rf95.init()) {
    Serial.println("LoRa radio initialization failed.");
    while (1);
  }
  Serial.println("LoRa radio initialization OK!");

  rf95.setTxPower(23, false);
}

void loop() {
  while (Serial.available()) {
    delay(1);
    char c = Serial.read();
    readString += c;
  }

  Serial.println("Done reading string!");
  Serial.println(readString);


  readString.trim();
  if (readString.length() >0) {
    if (readString == "Hello") {
      Serial.println("They said Hello!");
    }
    else if (readString == "I hate you") {
      Serial.println("Oh no! They hate me!");
    }
    else {
      Serial.println("They sent a generic message.");
    }

    readString = "";
  }


}
