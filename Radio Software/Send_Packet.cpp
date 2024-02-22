#include <Arduino.h>

HardwareSerial Serial1(PA10, PA9);
HardwareSerial xbeeSerial(PA3, PA2);

struct Packet
{
    // String helloworld = "hello world";
    int8_t intint = rand() % 100; // maps from ASCII
};

Packet testPacket;
int i = 0;

void setup()
{
    Serial1.begin(9600);
    xbeeSerial.begin(9600);

    Serial1.println("Setup Complete");
    xbeeSerial.print("Setup Complete");
}

void loop()
{
    Serial1.println("");

    /*xbeeSerial.write((byte)testPacket.helloworld[i]);
    i++;
    if (i == 12)
    {
        i = 0;
        xbeeSerial.write((byte)testPacket.intint);
    }*/
    xbeeSerial.write((byte)rand() % 100);
    xbeeSerial.write("     ");
    xbeeSerial.write((byte)rand() % 200);
    delay(10);
}
