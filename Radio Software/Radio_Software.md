# Radio Software & Architecture

This year we are designing a wireless data communication system with two Xbee 3 Pro 900MHz modules. Below is the architecture for the system. I have successfully created the Xbee network. I have been able to forward a packet from an STM32 to an xbee via UART and then receive on the second Xbee. This data is read voa serial and displays on a live web-server. I am currently writing the software for 
the web-server to display live data from the car’s drive-critical sensors.