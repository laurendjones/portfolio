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
uint8 endByte = 59;

struct car_data _car_data;

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
        memcpy(&_car_data.ecvt + 0, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA2:
        memcpy(&_car_data.ecvt + 8, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA3:
        memcpy(&_car_data.ecvt + 16, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA4:
        memcpy(&_car_data.ecvt + 24, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA5:
        memcpy(&_car_data.ecvt + 32, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA6:
        memcpy(&_car_data.ecvt + 40, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA7:
        memcpy(&_car_data.ecvt + 48, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA8:
        memcpy(&_car_data.ecvt + 56, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA9:
        memcpy(&_car_data.ecvt + 64, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA10:
        memcpy(&_car_data.ecvt + 72, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA11:
        memcpy(&_car_data.ecvt + 80, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA12:
        memcpy(&_car_data.ecvt + 88, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA13:
        memcpy(&_car_data.ecvt + 96, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA14:
        memcpy(&_car_data.ecvt + 104, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA15:
        memcpy(&_car_data.ecvt + 112, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ECVT_DATA16:
        memcpy(&_car_data.ecvt + 120, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case VOLTAGES:
        memcpy(&_car_data.electrons + 0, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case CURRENTS:
        memcpy(&_car_data.electrons + 8, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case ELEC_DATA3:
        memcpy(&_car_data.electrons + 16, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case IMU_DATA1:
        memcpy(&_car_data.imu + 0, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case IMU_DATA2:
        memcpy(&_car_data.imu + 8, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case IMU_DATA3:
        memcpy(&_car_data.imu + 16, CAN_RX_msg.buf, CAN_RX_msg.len);
        return;
    case IO:
        _car_data.logging = (CAN_RX_msg.buf[0] & 0b01000000) >> 6;
        _car_data.launch = (CAN_RX_msg.buf[0] & 0b0010000) >> 5;
        _car_data.susSoft = (CAN_RX_msg.buf[0] & 0b00010000) >> 4;
        _car_data.susHard = (CAN_RX_msg.buf[0] & 0b00001000) >> 3;
        _car_data.spare = (CAN_RX_msg.buf[0] & 0b00000100) >> 2;
        _car_data.clutchMode = CAN_RX_msg.buf[0] & 0b00000011;
        return;
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
    xbeeSerial.write((byte *)&_car_data.ecvt, sizeof(_car_data.ecvt));
    xbeeSerial.write((byte *)&_car_data.electrons.voltageSenseBatt, sizeof(_car_data.electrons.voltageSenseBatt));
    xbeeSerial.write((byte *)&_car_data.imu.gpsLatitude, sizeof(_car_data.imu.gpsLatitude));
    xbeeSerial.write((byte *)&_car_data.imu.gpsLongitude, sizeof(_car_data.imu.gpsLongitude));
    xbeeSerial.write((byte *)&_car_data.logging, sizeof(_car_data.logging));
    xbeeSerial.write((byte *)&_car_data.launch, sizeof(_car_data.launch));
    xbeeSerial.write((byte *)&_car_data.clutchMode, sizeof(_car_data.clutchMode));

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
