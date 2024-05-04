# Radio Software & Architecture

This year we fully designed and implemented a research & development project: wireless data communication, which fully worked at competition! This system has two Xbee 3 Pro 900MHz modules. Below is the architecture for the system. An STM32 forwards a packet to an Xbee via UART and then receives this packet on the second Xbee. This data is read via serial and displays on a live GUI. The frontend handles the displaying of all live sensor values and the backend handles the data from serial. One feature of the backend is a Data Generator which sorts through a data struct (in C++), and in python unpacks the struct and updates each of the data values. If the file of sensors is ever changed, we can easily update it instead of having to rewrite code. 

![image (33)](https://github.com/laurendjones/portfolio/assets/61713371/b83822d9-422b-4c4c-95b8-4b9ec7199a0d)
![image](https://github.com/laurendjones/portfolio/assets/61713371/2d9ce888-96a2-4ee9-a9ae-3dc9ec57b9c2)
![image](https://github.com/laurendjones/portfolio/assets/61713371/096dd5e8-4d8e-496f-861a-fcd5abe0c71f)
