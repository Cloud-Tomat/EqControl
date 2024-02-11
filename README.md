# EqControl

 Speed control Sketch for Arduino.
 Control a stepper motor drive to compensate precisely earth rotation :
* Compatible with analog Joystick for manual control
* Interruption based precise timing
* Support Auto guiding discrete signal inputs
* Compensation of periodic worm gear errors.

Need to be adapated to your specific setup :

## I/O configuration

#define CLOCK 8 : To stepper motor controler, clock signal
#define MANUAL 9 : Manual Switch input
#define ANA 0 : Joystick analog In
#define DIR 7 : To stepper motor controller direction input
#define ADP 3 : Autoguiding input accelererate
#define ADM 2 : AutoGuiding Input decelerate 





