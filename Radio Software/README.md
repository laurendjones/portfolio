# Radio Software & Architecture

This year we are designing a research & development project: wireless data communication. This system has two Xbee 3 Pro 900MHz modules. Below is the architecture for the system. I have successfully created an Xbee network. An STM32 forwards a packet to an xbee via UART and then receives this packet on the second Xbee. This data is read via serial and displays on a live web-server. I am currently writing the software for the web-server to display live data from the car’s drive-critical sensors.

![image](https://github.com/laurendjones/portfolio/assets/61713371/096dd5e8-4d8e-496f-861a-fcd5abe0c71f)
![image](https://github.com/laurendjones/portfolio/assets/61713371/2d9ce888-96a2-4ee9-a9ae-3dc9ec57b9c2)
