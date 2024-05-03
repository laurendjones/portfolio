#include <Arduino.h>
#include <STM32_CAN.h>
#include <../lib/DAQ_COMMON/can_address.h>
#include <../lib/DAQ_COMMON/data.h>

int canResetPin = PA8;
HardwareSerial Serial1(PA10, PA9);
HardwareSerial xbeeSerial(PA3, PA2);

STM32_CAN can(CAN1, DEF); // Use PA11/12 pins for CAN1.
static CAN_message_t CAN_RX_msg;

bool xbeeWrite = false;
int numReceivedMessages = 0;

uint8 startByte = 42;
uint8 endByte = 69;

struct eCVTData
{
    int64 data1;
    int64 data2;
    int64 data3;
    int64 data4;
    int64 data5;
    int64 data6;
    int64 data7;
    int64 data8;
    int64 data9;
    int64 data10;
    int64 data11;
    int64 data12;
    int64 data13;
    int64 data14;
    int64 data15;
    int64 data16;
} eCVTData;

void setup()
{
    // Serial1.begin(115200);
    xbeeSerial.begin(57600);

    pinMode(PB4, OUTPUT);

    can.begin();
    can.setBaudRate(1000000);
    digitalWrite(canResetPin, 0);
}

void receiveCan()
{
    if (!can.read(CAN_RX_msg))
        return;

    switch (CAN_RX_msg.id)
    {
    case ECVT_DATA1:
        memcpy(&eCVTData.data1, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA2:
        memcpy(&eCVTData.data2, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA3:
        memcpy(&eCVTData.data3, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA4:
        memcpy(&eCVTData.data4, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA5:
        memcpy(&eCVTData.data5, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA6:
        memcpy(&eCVTData.data6, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA7:
        memcpy(&eCVTData.data7, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA8:
        memcpy(&eCVTData.data8, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA9:
        memcpy(&eCVTData.data9, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA10:
        memcpy(&eCVTData.data10, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA11:
        memcpy(&eCVTData.data11, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA12:
        memcpy(&eCVTData.data12, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA13:
        memcpy(&eCVTData.data13, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA14:
        memcpy(&eCVTData.data14, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA15:
        memcpy(&eCVTData.data15, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA16:
        memcpy(&eCVTData.data16, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
        /*
        case CLUTCH_DATA1:
            return;
        case CLUTCH_DATA2:
            return;
        case CLUTCH_DATA3:
            return;
        case CLUTCH_DATA4:
            return;*/
    }
}

void transmitXbee()
{
    const uint32_t period = 25000; // 40 Hz
    static uint32_t prevTime = micros();

    if (micros() - prevTime < period)
        return;

    prevTime += period;

    // Start bits - 42 x 4
    for (int i = 0; i < 4; i++)
        xbeeSerial.write((byte *)&startByte, sizeof(startByte));

    // Write data
    xbeeSerial.write((byte *)&eCVTData, sizeof(ecvt_data));

    // End bits - 69 x 4
    for (int i = 0; i < 4; i++)
        xbeeSerial.write((byte *)&endByte, sizeof(endByte));
}

void heartbeatTimer()
{
    const uint32_t period = 1000;
    static uint32_t prevTime = millis();

    if (millis() - prevTime < period)
        return;

    prevTime += period;

    digitalToggle(PB4);
}

void loop()
{
    receiveCan();
    transmitXbee();
    heartbeatTimer();
}
