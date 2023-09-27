# Measuring Encoder CPR

## Procedure:
1. Connect pico to L293D motor driver
2. Connect all pins as follows:
   1. L293D input 1 to GP14
   2. L293D input 2 to GP15
   3. L293D enable to GP13
   4. Encoder A to GP11
   5. Encoder B to GP12
3. 3D Print a [connector](ConnectorForRotaryPotentiometer.stl) that allows the motor shaft to fit into the 3382 rotary potentiometer
4. Couple the motor shaft to the rotary potentiometer
5. Let program run for a bit and average the encoder CPR values that are spit out.

## Note:
You will need the rp-2040-encoder library in order for this to work.  
To install,  go to sketch -> include library -> manage library -> search for rp2040-encoder-library and click install

## Results:
**Encoder CPR:** 