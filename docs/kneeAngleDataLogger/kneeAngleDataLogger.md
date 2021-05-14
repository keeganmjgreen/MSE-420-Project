# System Level Block Diagrams



## Programming the Arduino



    graph LR
        1[Computer]
        2[Arduino Microcontroller]
        1 -->|USB-to-UART| 2

![](https://mermaid.ink/svg/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICAxW0NvbXB1dGVyXVxuICAgIDJbQXJkdWlubyBNaWNyb2NvbnRyb2xsZXJyXVxuICAgIDEgLS0-fFVTQi10by1VQVJUfCAyIiwibWVybWFpZCI6e30sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)



*Notes:*



- The computer transmits information (a program from the Arduino IDE, in the above case) to the Arduino (and vice-versa, albeit little in the above case) via USB.
- “USB-to-UART” is actually part of an IC onboard the Arduino.
- USB 2 here uses half-[duplex](https://en.wikipedia.org/wiki/Duplex_(telecommunications)) (two-way) [serial communication](https://en.wikipedia.org/wiki/Serial_communication) and [differential signaling](https://en.wikipedia.org/wiki/Differential_signaling).
- UART uses full-[duplex](https://en.wikipedia.org/wiki/Duplex_(telecommunications)) (simultaneous two-way) [serial communication](https://en.wikipedia.org/wiki/Serial_communication).
- UART = [Universal Asynchronous Receiver-Transmitter](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter) communication protocol.



## Programming the BLE Module



    graph LR
        1[Computer]
        2[Arduino Microcontroller]
        1 -->|USB-to-UART| 2
        2 -->|UART-to-USB| 1
        3[BLE Module]
        2 -->|TX-to-TX*| 3
        3 -->|RX-to-RX| 2

![](https://mermaid.ink/svg/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICAxW0NvbXB1dGVyXVxuICAgIDJbQXJkdWlubyBNaWNyb2NvbnRyb2xsZXJyXVxuICAgIDEgLS0-fFVTQi10by1VQVJUfCAyXG4gICAgMiAtLT58VUFSVC10by1VU0J8IDFcbiAgICAzW0JMRSBNb2R1bGVdXG4gICAgMiAtLT58VFgtdG8tVFgqfCAzXG4gICAgMyAtLT58UlgtdG8tUlh8IDIiLCJtZXJtYWlkIjp7fSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)



*Notes:*



- The computer transmits information (BLE module configuration `AT` commands from any serial monitor, in the above case) to the BLE module (and vice-versa) through the Arduino via USB.

- Again, “USB-to-UART” and “UART-to-USB” are actually parts of an IC onboard the Arduino. This IC is ‘tied’ to the Arduino `TX` and `RX` pins.

- `TX` transmits via UART from the labeled device.

- `RX` receives via UART from a communicating device.

- \*using a [voltage divider](https://en.wikipedia.org/wiki/Voltage_divider) with a 1-kΩ resistor from 5.0 V to 3.3 V and a 2-kΩ resistor from 3.3 V to ground (Arduino `GND` pins).

  The [logical high voltage levels](https://en.wikipedia.org/wiki/Logic_level) of the Arduino microcontroller and Bluetooth 4.0 BLE module are around 5.0 V (Arduino `5V0` pin) and 3.3 V (Arduino `3V3` pin), respectively.

  As such and in this one case, not using a [level shifter](https://en.wikipedia.org/wiki/Level_shifter) such as an equivalent voltage divider or transistor equivalent may damage the BLE module.

- BLE = [Bluetooth Low Energy](https://en.wikipedia.org/wiki/Bluetooth_Low_Energy).



## Logging Knee Angle Data



```
graph LR
    1[Rotary Encoder]
    2[Arduino Microcontroller]
    1 --> 2
    3[Wireless Transmission]
    2 -->|UART-to-BLE| 3
    4[Phone]
    3 --> 4
    5[Wired Transmission]
    2 -->|UART-to-USB| 5
    6[Computer]
    5 --> 6
```

![](https://mermaid.ink/svg/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICAxW1JvdGFyeSBFbmNvZGVyXVxuICAgIDJbQXJkdWlubyBNaWNyb2NvbnRyb2xsZXJyXVxuICAgIDEgLS0-IDJcbiAgICAzW1dpcmVsZXNzIFRyYW5zbWlzc2lvbl1cbiAgICAyIC0tPnxVQVJULXRvLUJMRXwgM1xuICAgIDRbUGhvbmVdXG4gICAgMyAtLT4gNFxuICAgIDVbV2lyZWQgVHJhbnNtaXNzaW9uXVxuICAgIDIgLS0-fFVBUlQtdG8tVVNCfCA1XG4gICAgNltDb21wdXRlcl1cbiAgICA1IC0tPiA2IiwibWVybWFpZCI6e30sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

*Notes:*



- Technically-not-a-[servomotor](https://en.wikipedia.org/wiki/Servomotor).
  (No built-in [feedback](https://en.wikipedia.org/wiki/Feedback) [control](https://en.wikipedia.org/wiki/Control_theory) of position or speed.)
  - [Actuator](https://en.wikipedia.org/wiki/Actuator): [DC motor](https://en.wikipedia.org/wiki/DC_motor) with [gear train](https://en.wikipedia.org/wiki/Gear_train).
  - [Sensor](https://en.wikipedia.org/wiki/Sensor): Optical **Rotary Encoder** ([reference](https://en.wikipedia.org/wiki/Rotary_encoder)) in *quadrature*.
    - For position feedback or just sensing (in this case).
    - *Encodes* direction as well as knee angle [increments/decrements](https://en.wikipedia.org/wiki/Incremental_encoder) (0.5° resolution).
    - Transparent disc with two opaque, circular ‘barcodes’ offset from each other by 0.5°.
    - [LED](https://en.wikipedia.org/wiki/Light-emitting_diode)–[photodiode](https://en.wikipedia.org/wiki/Photodiode) pairs placed across these patterned ‘light-slots’.
    - Outputs two digital signals.
  
- [Arduino](https://www.arduino.cc/) **Microcontroller**.
  - Receives encoder signals on digital pins “A” and “B”.
    
  - *Decodes* knee angle from encoder output.

- **UART-to-BLE** = [DSD TECH HM-10 Master and Slave Bluetooth 4.0 LE Module](https://www.amazon.ca/DSD-TECH-Bluetooth-iBeacon-Arduino/dp/B06WGZB2N4).
  - Connected to the Arduino `TX` and `RX` pins.

- Android **Phone**.
  
  - [Serial Bluetooth Terminal](https://play.google.com/store/apps/details?id=de.kai_morich.serial_bluetooth_terminal), by [Kai Morich](https://github.com/kai-morich).
  
- Windows 10 **Computer**.
  
  - [Knee Angle Data Logger Interface](https://colab.research.google.com/drive/1UwJlT_PA8JW-FkqT5CZ-N5BUNcUGnGsa?usp=sharing), by me.
