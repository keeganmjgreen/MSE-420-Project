
``kneeAngleDataLogger.ino``
===========================

.. code-block:: c

    #include <arduino-timer.h>

    int pinA = 4; // Pin for Encoder Channel A.
    int pinB = 2; // Pin for Encoder Channel B.

    bool oldA; // Old Encoder Channel A signal.
    bool oldB; // Old Encoder Channel B signal.

    bool newA; // New Encoder Channel A signal.
    bool newB; // New Encoder Channel B signal.

    float numDegrees = 0; // Current knee angle (relative — incremental encoder) (0.5° resolution).

    // strDegrees = "±XXX.X\n"
    char strDegrees[7]; // charsPerMessage = 7

    int bitsPerSecond = 9600; // Default baud (data transfer) rate.
    // Reliable over Bluetooth.

| :math:`\small \; \vdots`
| :math:`\small \: \bullet \quad \quad \text{bits per second} = 9\,600`
| :math:`\small \: \bullet \quad \quad \text{start bits per character} = 1`
| :math:`\small \: \bullet \quad \quad \; \! \text{data bits per character} = 8`
| :math:`\small \: \bullet \quad \quad \: \text{stop bits per character} = 1`
| :math:`\small \: \bullet \quad \quad \text{bits per character} = ( \text{start bits} + \text{data bits} + \text{stop bits} ) \ \text{per character} = 10`
| :math:`\small \: \bullet \quad \quad \text{seconds per character ($\,T_\textsf{character}$)} = \text{bits per character} \: / \: \text{bits per second} \approx 0.001\,04`
| :math:`\small \: \bullet \quad \quad \text{characters per message} = 7`
| :math:`\small \: \bullet \quad \quad \text{seconds per message ($\,T_\textsf{message}$)} = \text{seconds per character} \, \cdot \: \text{characters per message} \approx 0.007\,3`
| :math:`\small \: \bullet \quad \quad \text{milliseconds per message} = \lceil \, \text{seconds per message} \: \cdot \, 10^3 \, \rceil = \lceil \, 7.3 \, \rceil = 8 \longrightarrow \boxed{10}`
| :math:`\small \; \vdots`

.. code-block:: c

    /* 
     * int startBitsPerChar = 1;
     * int  dataBitsPerChar = 8;
     * int  stopBitsPerChar = 1;
     * 
     * int bitsPerChar = startBitsPerChar + dataBitsPerChar + stopBitsPerChar;
     * 
     * float secondsPerChar = bitsPerChar / bitsPerSecond;
     * 
     * int charsPerMessage = 7;
     * 
     * float secondsPerMessage = secondsPerChar * charsPerMessage;
     * 
     * int millisPerMessage = ceil(secondsPerMessage * 1e3);
     * 
     */
    
    int millisPerMessage = 10;

    Timer<1, millis, char *> timer;

    void setup()
    {
        pinMode(pinA, INPUT_PULLUP);
        pinMode(pinB, INPUT_PULLUP);
        pinMode(5,    INPUT_PULLUP);

        oldA = digitalRead(pinA);
        oldB = digitalRead(pinB);

        Serial.begin(bitsPerSecond);

        timer.every(millisPerMessage, [](char *strDegrees) -> bool { Serial.println(strDegrees); return true; }, strDegrees);
    }
    void loop()
    {
        if (digitalRead(5))
        {
            timer.tick();
        }

        dtostrf(numDegrees, 3, 1, strDegrees);

        newA = digitalRead(pinA);
        newB = digitalRead(pinB);

        if ((!oldA && newB || oldA && !newB) &&
        (!oldB && !newA || oldB && newA))
        {
            numDegrees += 0.5;
        }
        if ((oldA && newB || !oldA && !newB) &&
        (!oldB && newA || oldB && !newA))
        {
            numDegrees -= 0.5;
        }
        oldA = newA;
        oldB = newB;
    }

----
