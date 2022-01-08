picohx  - For 6 button 2 dial pedal

TODO:
Change Snapshot button so it moves through three snapshots in order
    1,2,3 and changes led from green->yellow->red

3 on/off buttons for CC100-102
Toggle snapshot 1/2 button
Tap/tuner button 
Patch change button moves through patches in order 0-3

Circutipython midi foot controller for HX Stomp.

Midi Command on HX stomp:

CC69 = 0-2  - Select snapshot 1-3

CC110 = 0-127 - Dial 1 Potentiometer. (Reverb mix) 
CC111 = 0 or 127 - Dial 1 on low value can bypass an effect 
CC112 = 0-127 - Dial 2 Potentiometer. (Volume mix)
CC113 = 0 or 127 - Dial 2 on low value can bypass an effect

CC100 = 0 or 127 - FX1 button
CC101 = 0 or 127 - FX2 button
CC102 = 0 or 127 - FX3 button

GPIO Pins:
Dial 1: GP28
Dial 2: GP27
Common Reference Voltage: Pin 35 - ADC_VREF

MIDI Pins: GP4 send, GP5 receive (not currently used needs optocoupler)


Midi Send Notes/Examples:
Send midi message to uart with:
midiuart.write(bytes([0xB0, 72, 0])) # CC72 = 0 - next patch
midiuart.write(bytes([0xB0, 72, 127])) # CC72 = 127 - previous patch
midiuart.write(bytes([0xB0, 69, (i-1)])) # CC69 = 0,1, or 2 - snapshot select 1, 2, 3
midiuart.write(bytes([0xB0, 100, i])) # CC100 = 0 or 127 on or off switch 1
midiuart.write(bytes([0xB0, 101, i])) # CC101 = 0 or 127 on or off switch 2


Midi Tutorial:
https://learn.sparkfun.com/tutorials/midi-tutorial/all
