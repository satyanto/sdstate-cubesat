/*
    Hafidh Satyanto
    Arduino Receiver Code

    Receives over-the-air serial character arrays via LoRa from another transceiver and then converts to string
    to groundstation Raspberry Pi, of which it would then be parsed and processed.

*/

#include <SPI.h>
#include <RH_RF95.h>

#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3

#define RF95_FREQ 915.0
RH_RF95 rf95(RFM95_CS, RFM95_INT);

void setup()
{
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
    while(1);
  }
  Serial.println("LoRa radio initialization OK!");

  rf95.setTxPower(5, false);
}

void loop()
{
  if (rf95.available())
  {
    uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);

    if (rf95.recv(buf, &len))
    {
      Serial.print("Received: ");
      Serial.write((char*)buf);
      Serial.print("\n RSSI: ");
      Serial.println(rf95.lastRssi(), DEC);

    }
    else
    {
      Serial.println("Receive failed.");
    }
  }
}
