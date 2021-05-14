
``kneeAngleDataLogger.ino``
===========================

.. code-block:: c

    #include <arduino-timer.h>

    int pinA = 4;
    int pinB = 2;

    bool oldA;
    bool oldB;

    bool newA;
    bool newB;

    float numDegrees = 0;

    char strDegrees[7]; // 7 = charsPerMessage

    int bitsPerSecond = 9600;

    /* 
    * int dataBitsPerChar = 8;
    * int stopBitsPerChar = 1;
    * 
    * int bitsPerChar = dataBitsPerChar + stopBitsPerChar;
    * 
    * float secondsPerChar = bitsPerChar / bitsPerSecond;
    * 
    * int charsPerMessage = 7;
    * 
    * float secondsPerMessage = secondsPerChar * charsPerMessage;
    * 
    * int microsPerMessage = ceil(secondsPerMessage * 1e6);
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
