picohx

Test version to try using diffent button layout.\

Use Switch 1 to toggle snapshot 1 / 2
Use switch 2 to set an effect on/off on CC103
Use switch 3 to set an effect on/off on CC104

Circutipython midi foot controller for HX Stomp.


Midi Command on HX stomp:
CC72 = 127 - Move to next preset
CC72 = 0 - Move to previous preset

CC69 = 0 - Select snapshot 1
CC69 = 1 - Select snapshot 2
CC69 = 2 - Select snapshot 3

CC110 (was:CC80) = 0-127 - Dial 1 Potentiometer. (Reverb mix)  Do I need to divide by 100.  to control mix from 0-100?
CC112 (was:CC81) = 0-127 - Dial 2 Potentiometer. (Volume mix)
CC111 (was:CC90) = 0 or 127 - Dial 1 on low value can bypass an effect 
CC113 (was:CC91) - 0 or 127 - Dial 2 on low value can bypass an effect


CC100 = 0 or 127 - Switch 1 Returns a true or false value
CC101 = 0 or 127 - Switch 2 Returns a true or false value
CC102 = 0 or 127 - Switch 3 Returns a true or false value


GPIO Pins:
Dial 1: GP28
Dial 2: GP27
Common Reference Voltage: Pin 35 - ADC_VREF

Switch 1: GP14
Switch 1 Led: GP20
Switch 2: GP15
Switch 2 Led: GP21
Switch 3: GP12
Switch 3 Led: GP13


Button 1: GP6
Button 1 Led: GP9
Button 2: GP7
Button 2 Led: GP10
Button 3: GP8
Button 3 Led: GP11


Midi Send Notes:
Send midi message to uart with:
midiuart.write(bytes([0xB0, 72, 0])) # CC72 = 0 - next patch
midiuart.write(bytes([0xB0, 72, 127])) # CC72 = 127 - previous patch
midiuart.write(bytes([0xB0, 69, (i-1)])) # CC69 = 0,1, or 2 - snapshot select 1, 2, 3
midiuart.write(bytes([0xB0, 100, i])) # CC100 = 0 or 127 on or off switch 1
midiuart.write(bytes([0xB0, 101, i])) # CC101 = 0 or 127 on or off switch 2


Midi Tutorial:

https://learn.sparkfun.com/tutorials/midi-tutorial/all









