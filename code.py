import time
import board
import digitalio
import analogio
import busio

# ################ GLOBALS ##################

# Buttons
button1 = digitalio.DigitalInOut(board.GP6)
button1.switch_to_input(pull=digitalio.Pull.UP)

button2 = digitalio.DigitalInOut(board.GP7)
button2.switch_to_input(pull=digitalio.Pull.UP)

button3 = digitalio.DigitalInOut(board.GP8)
button3.switch_to_input(pull=digitalio.Pull.UP)


# Potentiometers
dial1 = analogio.AnalogIn(board.GP28)
dial2 = analogio.AnalogIn(board.GP27)
# initial pre-calibration values with diminished range.
dial1_minvalue = 1000
# set last value for auto-calibrate decision to update range or send cc
dial1_lastvalue = 32000
dia11_currentvalue = 32000
# set initial value for dial range value per midi CC range of 0-127
dial1_stepvalue = 300
dial1_maxvalue = 63000
dial1_midivalue = 64
dial2_minvalue = 1000
dial2_lastvalue = 32000
dial2_currentvalue = 32000
dial2_stepvalue = 300
dial2_maxvalue = 63000
dial2_midivalue = 64

# SWITCHES
switch1 = digitalio.DigitalInOut(board.GP14)
switch1.switch_to_input(pull=digitalio.Pull.UP)
switch1_lastvalue = switch1.value

switch2 = digitalio.DigitalInOut(board.GP15)
switch2.switch_to_input(pull=digitalio.Pull.UP)
switch2_lastvalue = switch2.value

switch3 = digitalio.DigitalInOut(board.GP12)
switch3.switch_to_input(pull=digitalio.Pull.UP)
switch3_lastvalue = switch3.value

# LEDS
led0 = digitalio.DigitalInOut(board.LED)
led0.direction = digitalio.Direction.OUTPUT

button1_led = digitalio.DigitalInOut(board.GP9)
button1_led.direction = digitalio.Direction.OUTPUT

button2_led = digitalio.DigitalInOut(board.GP10)
button2_led.direction = digitalio.Direction.OUTPUT

button3_led = digitalio.DigitalInOut(board.GP11)
button3_led.direction = digitalio.Direction.OUTPUT

switch1_led = digitalio.DigitalInOut(board.GP20)
switch1_led.direction = digitalio.Direction.OUTPUT

switch2_led = digitalio.DigitalInOut(board.GP21)
switch2_led.direction = digitalio.Direction.OUTPUT

switch3_led = digitalio.DigitalInOut(board.GP13)
switch3_led.direction = digitalio.Direction.OUTPUT

# UART - MIDI port Send Only
midiuart = busio.UART(tx=board.GP4, rx=board.GP5, baudrate=31250)

currentsnapshot = 1

# Function Definitions:

# serial debugging logger
def zakserialdebug(sleeptime):
    print('')
    print('dial1_currentvalue: ' + str(dial1_currentvalue))
    print('dial1changevalue: ' + str(dial1changevalue))
    print('Dial1 minvalue: ' + str(dial1_minvalue) + ' Dial1 Maxvalue: ' + str(dial1_maxvalue) + ' Dial1 stepvalue: ' + str(dial1_stepvalue)
    + ' Dial1 lastvalue: ' + str(dial1_lastvalue) + ' Dial1 midivalue: ' + str(dial1_midivalue) + ' Dial1 raw: ' + str(dial1.value))
    print('')
    print('dial2_currentvalue: ' + str(dial2_currentvalue))
    print('dial2changevalue: ' + str(dial2changevalue))
    print('Dial2 minvalue: ' + str(dial2_minvalue) + ' Dial2 Maxvalue: ' + str(dial2_maxvalue) + ' Dial2 stepvalue: ' + str(dial2_stepvalue)
    + ' Dial2 lastvalue: ' + str(dial2_lastvalue) + ' Dial2 midivalue: ' + str(dial2_midivalue) + ' Dial2 raw: ' + str(dial2.value))
    print('')
    print('Button1: ' + str(button1.value))
    print('Button2: ' + str(button2.value))
    print('Button3: ' + str(button3.value))
    print('')
    print('Switch1: ' + str(switch1.value))
    print('Switch2: ' + str(switch2.value))
    print('')
    time.sleep(sleeptime)

# Lightshow for startup.
def blinkies():
    for x in range (0,10):
        led0.value = True
        button1_led.value = True
        time.sleep(0.0015)
        switch1_led.value = True
        time.sleep(0.015)
        button2_led.value = True
        time.sleep(0.015)
        switch2_led.value = True
        time.sleep(0.015)
        button3_led.value = True
        time.sleep(0.015)
        switch3_led.value = True
        time.sleep(0.015)
        button1_led.value = False
        time.sleep(0.015)
        switch1_led.value = False
        time.sleep(0.015)
        button2_led.value = False
        time.sleep(0.015)
        switch2_led.value = False
        time.sleep(0.015)
        button3_led.value = False
        time.sleep(0.015)
        switch3_led.value = False
        time.sleep(0.015)
        led0.value = False
        time.sleep(0.02)

def snapshotchangeto(i):
    global currentsnapshot
    #update current snapshot and LED on.
    #accept a value of 1-3 and send a midi message with a zero indexed value (0-2)
    print('%%%%%%%%%%%%%%%%%%%%Snapshot ' + str(i))  # display a message on the terminal that it worked
    currentsnapshot = i
    midiuart.write(bytes([0xB0, 69, (i-1)])) # CC69 = 0,1, or 2 TEST THIS TODO TODO TODO
    time.sleep(0.01) # small delay to prevent multiple sends from human latency of foot press

def ledflash():
    for x in range(0,4):
        button1_led.value = True
        button2_led.value = True
        button3_led.value = True
        switch1_led.value = True
        switch2_led.value = True
        time.sleep(0.02)
        button1_led.value = False
        button2_led.value = False
        button3_led.value = False
        switch1_led.value = False
        switch2_led.value = False
        time.sleep(0.02)

def switchmidiupdate():
    print('%%%%%%%%%%%%% Switch Midi Update')
    # CC100 = 0 or 127 on or off switch 1
    if switch1.value == True:
        midiuart.write(bytes([0xB0, 100, 127]))
        switch1_led.value = True
        print('%%%%%%%%%%%%% Switch 1 ON')
    else:
        midiuart.write(bytes([0xB0, 100, 0]))
        switch1_led.value = False
        print('%%%%%%%%%%%%% Switch 1 OFF')
    if switch2.value == True:
        midiuart.write(bytes([0xB0, 101, 127]))
        switch2_led.value = True
        print('%%%%%%%%%%%%% Switch 2 ON')
    else:
        midiuart.write(bytes([0xB0, 101, 0]))
        switch2_led.value = False
        print('%%%%%%%%%%%%% Switch 2 OFF')
    if switch3.value == True:
        midiuart.write(bytes([0xB0, 102, 127]))
        switch3_led.value = True
        print('%%%%%%%%%%%%% Switch 3 ON')
    else:
        midiuart.write(bytes([0xB0, 102, 0]))
        switch3_led.value = False
        print('%%%%%%%%%%%%% Switch 3 OFF')

# send new midi values of dial positions and bypass state
def dialmidiupdate():
    print('%%%%%%%%%%%%%%%%% Dials Midi Update')
    midiuart.write(bytes([0xB0, 80, dial1_midivalue]))
    midiuart.write(bytes([0xB0, 81, dial2_midivalue]))
    # update dial effect bypass state
    if (dial1_midivalue < 2):
        midiuart.write(bytes([0xB0, 90, 0]))
        print('DIAL 1 MIDI BLOCK BYPASSED CC90')
    else:
        midiuart.write(bytes([0xB0, 90, 127]))
        print('DIAL 1 MIDI BLOCK ACTTVE CC90')
    if (dial2_midivalue < 2):
        midiuart.write(bytes([0xB0, 91, 0]))
        print('DIAL 2 MIDI BLOCK BYPASSED CC91')
    else:
        midiuart.write(bytes([0xB0, 91, 127]))
        print('DIAL 2 MIDI BLOCK ACTIVE CC91')

# Program start

blinkies()

led0.value = True # use onboard led as a power indicator

snapshotchangeto(1)
switchmidiupdate()
dialmidiupdate()

#counter = 1 # Debug counter - TODO TODO TODO delete once done testing

# Main program run loop
while True:
    time.sleep(0.005) # set rate of loop to 1/200 second. Midi async bitrate is 31250bps or 3125B/sec midi messages are 3 Bytes so 1000 per second max.

# FIRST STEP, READ BUTTONS AND PROCESS SNAPSHOTS OR PROGRAM CHANGES
# SECOND STEP, READ AND PROCESS DIALS AND SEND APPROPREATE CC MESSAGES
# THIRD STEP, READ AND PROCESS SWITCHES AND SEND APPROPRATE CC MESSAGES

    # False indicates a button press
    # Read the status of all buttons and decided what the user is trying to do
    if button1.value == False or button2.value == False or button3.value == False:
        print('****************reading buttons')
        # Add a little delay time to allow physical button press to stabalize
        time.sleep(0.02)

        # detect for multiple presses first.  Then for single presses
        if button1.value == False and button2.value == False:
            print('%%%%%%%%%%%%%%%%%%Previous Patch selected.............')
            midiuart.write(bytes([0xB0, 72, 0])) # CC72 = 127 TEST THIS TODO TODO TODO
            ledflash()
            currentsnapshot = 1
            snapshotchangeto(currentsnapshot)
            switchmidiupdate()
            dialmidiupdate()
        elif button2.value == False and button3.value == False:
            print('%%%%%%%%%%%%%%%%%Next Patch selected.................')
            midiuart.write(bytes([0xB0, 72, 127])) # CC72 = 0 TEST THIS TODO TODO TODO
            ledflash()
            currentsnapshot = 1
            snapshotchangeto(currentsnapshot)
            switchmidiupdate()
            dialmidiupdate()
        elif button1.value == False:
            if button1_led.value == False:
                snapshotchangeto(2)
                button1_led.value = True
                time.sleep(0.2)
            else:
                snapshotchangeto(1)
                button1_led.value = False
                time.sleep(0.2)
        elif button2.value == False:
            snapshotchangeto(2)
        elif button3.value == False:
            snapshotchangeto(3)
        # Add a little delay time for buttons to stabalize after release
        time.sleep(0.06)

# SECOND STEP DIAL PROCESSING:
    # Run Dials auto-calibration & send Midi CC message if updated
    # Also, send a dial update every x pass through the run loop as the HX Stomp misses updates sent at the same time as patch changes


    # read curren dial value for next calculations
    dial1_currentvalue = dial1.value
    dial2_currentvalue = dial2.value

    # Check current max and min values for dials and update min / max range
    if dial1_currentvalue < dial1_minvalue:
        dial1_minvalue = dial1_currentvalue

    if dial1_currentvalue > dial1_maxvalue:
        dial1_maxvalue = dial1_currentvalue

    if dial2_currentvalue < dial2_minvalue:
        dial2_minvalue = dial2_currentvalue

    if dial2_currentvalue > dial2_maxvalue:
        dial2_maxvalue = dial2_currentvalue

    # recaltulate step values
    dial1_stepvalue = (dial1_maxvalue - dial1_minvalue) / 127
    dial2_stepvalue = (dial2_maxvalue - dial2_minvalue) / 127

    # THE CURRENT VALUE OF THE DIAL HAS CHANGED MORE THAN A STEP VALUE UP OR DOWN THEN UPDATE THE LAST VALUE & SEND A CC for value and bypass
    dial1changevalue = (dial1_currentvalue - dial1_lastvalue) / dial1_stepvalue
    if (dial1changevalue >= 1 or dial1changevalue <= -1):
        dial1_midivalue = int(dial1_currentvalue / dial1_stepvalue)
        if dial1_midivalue > 127:  # Fix for first iteration reading above 127
            dial1_midivalue = 127
        print('%%%%%%%%%%%%%%%%DIAL 1 MOVED - Midi Value: ' + str(dial1_midivalue))
        dialmidiupdate()
        # was midiuart.write(bytes([0xB0, 80, dial1_midivalue]))
        # update for next iteration
        dial1_lastvalue = dial1_currentvalue


    dial2changevalue = (dial2_currentvalue - dial2_lastvalue) / dial2_stepvalue
    if (dial2changevalue >= 1 or dial2changevalue <= -1):
        dial2_midivalue = int(dial2_currentvalue / dial2_stepvalue)
        if dial2_midivalue > 127:  # Fix for first iteration reading above 127
            dial2_midivalue = 127
        print('%%%%%%%%%%%%%%%%DIAL 2 MOVED - Midi Value: ' + str(dial2_midivalue))
        dialmidiupdate()
        #was midiuart.write(bytes([0xB0, 81, dial2_midivalue]))
        dial2_lastvalue = dial2_currentvalue
        # update dial effect bypass state


# THIRD STEP SWITCH PROCESSING:
    # read current switch values and if they are different than the last value then send a midi message
    if switch1.value != switch1_lastvalue:
        print('%%%%%%%%%%%%%%%Switch1 changed')
        switchmidiupdate()
        #udate state for next iteration
        switch1_lastvalue = switch1.value
        time.sleep(0.04)
    if switch2.value != switch2_lastvalue:
       print('%%%%%%%%%%%%%%%%Switch2 changed')
       switchmidiupdate()
       switch2_lastvalue = switch2.value
       time.sleep(0.04)
    if switch3.value != switch3_lastvalue:
       print('%%%%%%%%%%%%%%%%Switch3 changed')
       switchmidiupdate()
       switch3_lastvalue = switch3.value
       time.sleep(0.04)
# Debugging section for serial monitoring
    #counter += 1
    #print(counter)
    #zakserialdebug(0)
