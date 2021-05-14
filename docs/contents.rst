
Keegan Green · kmgreen@sfu.ca

`Design of an Active Knee Exoskeleton <https://github.com/keeganmjgreen/MSE-420-Project>`_
==========================================================================================

* Read the `proposal <https://raw.github.com/keeganmjgreen/MSE-420-Project/master/Project%20Proposal%20%E2%80%94%20Bionic%20Knee%20Actuator%20Device.pdf>`_.
* Read the `report <https://raw.github.com/keeganmjgreen/MSE-420-Project/master/Project%20%E2%80%94%20Design%20of%20an%20Active%20Knee%20Exoskeleton.pdf>`_.

----

Abstract
--------

An anthropometrically-adjustable, ergonomic, active knee exoskeleton is designed **---** and its materials are selected **---** to compensate for the indirect effect of large backpack loads on hikers' knees. This comes at the cost of weight evenly distributed over most of the leg, and that of a power source placed in the aforementioned backpack. By damping the jarring braking motion of hiking downhill, it may also regenerate energy. A motor--drivetrain pair is sized under advisement of the load's derived speed--torque curve, and a position controller is planned to follow the knee angle curve observed over the course of the gait cycle, in a 'moving target' control scheme. These data were collected for design and development in a similar manner to how state feedback may be provided to the controller. Analysis is data-driven and our design is founded on research on hikers' knee injuries, existing knee exoskeletons, and data acquisition.

----

Deriving the Speed--Torque Curve for a Knee Exoskeleton
-------------------------------------------------------

Data analysis has been `redone and improved in Python <https://colab.research.google.com/drive/1f8C9Sspb2fGo5s0l91qBrioHCT2sDvNa?usp=sharing>`_, with the help of a `basis expansions module <https://github.com/madrury/basis-expansions>`_.

Data was collected for the upper and lower leg angles over the course of numerous gait cycles, walking uphill and downhill. For each case, this eventually provided me and my team with the knee angle, angular velocity, angular acceleration, the torque for a backpack load, and the speed--torque curve to to match with that of a to-be-selected motor--drivetrain pair. This would be controlled to follow a moving reference/target **---** the knee angle **---** in user-selectable incline and decline operation modes. *Data analysis is documented as follows.*

.. toctree::

    Deriving_the_Speed_Torque_Curve_for_a_Knee_Exoskeleton

----

.. toctree::

    kneeAngleDataLogger/kneeAngleDataLogger
    kneeAngleDataLogger/kneeAngleDataLogger_ino
    kneeAngleDataLogger/kneeAngleDataLoggerInterface_ipynb

----
