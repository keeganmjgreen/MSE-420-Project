# Design of an Active Knee Exoskeleton

* Read the [proposal](Project%20Proposal%20%E2%80%94%20Bionic%20Knee%20Actuator%20Device.pdf).
* Read the [report](Project%20%E2%80%94%20Design%20of%20an%20Active%20Knee%20Exoskeleton.pdf).

## Abstract

An anthropometrically-adjustable, ergonomic, active knee exoskeleton is designed — and its materials are selected — to compensate for the indirect effect of large backpack loads on hikers’ knees. This comes at the cost of weight evenly distributed over most of the leg, and that of a power source placed in the aforementioned backpack. By damping the jarring braking motion of hiking downhill, it may also regenerate energy. A motor–drivetrain pair is sized under advisement of the load’s derived speed–torque curve, and a position controller is planned to follow the knee angle curve observed over the course of the gait cycle, in a ‘moving target’ control scheme. These data were collected for design and development in a similar manner to how state feedback may be provided to the controller. Analysis is data-driven and our design is founded on research on hikers’ knee injuries, existing knee exoskeletons, and data acquisition.

## [Deriving the Speed–Torque Curve for a Knee Exoskeleton](https://mse-420-project.readthedocs.io/en/latest/)

Data analysis has been [redone and improved in Python](https://colab.research.google.com/drive/1f8C9Sspb2fGo5s0l91qBrioHCT2sDvNa?usp=sharing), with the help of a [basis expansions module](https://github.com/madrury/basis-expansions).

[![Documentation Status](https://readthedocs.org/projects/mse-420-project/badge/?version=latest)](https://mse-420-project.readthedocs.io/en/latest/?badge=latest)
