## version 0.2
- implement communication using USB UART
- added code to read angle values from the data received from the computer
- added simple calculation- 360 angle means 100% duty value and 0 mean 0%
### TODO
-Calculate the duty cycle from the angles in a way that gives the exact chosen angle for each servo.
## version 0.1
- added configuration of 4 pins for generating pwm signals
- added varaibles for setting frequency of pwm's and duty cycle
### TODO
- change setting of pwm's duty cycle from 0-100 percent range to value adjusted to pwms specifications
- changing duty cycle from command received by USB
