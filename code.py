import time
import board
import digitalio
import analogio
import busio

# ################ GLOBALS ##################

# Buttons
button1 = digitalio.DigitalInOut(board.GP1)
button1.switch_to_input(pull=digitalio.Pull.UP)

button2 = digitalio.DigitalInOut(board.GP0)
button2.switch_to_input(pull=digitalio.Pull.UP)

button3 = digitalio.DigitalInOut(board.GP2)
button3.switch_to_input(pull=digitalio.Pull.UP)

button4 = digitalio.DigitalInOut(board.GP3)
button4.switch_to_input(pull=digitalio.Pull.UP)

button5 = digitalio.DigitalInOut(board.GP6)
button5.switch_to_input(pull=digitalio.Pull.UP)

button6 = digitalio.DigitalInOut(board.GP7)
button6.switch_to_input(pull=digitalio.Pull.UP)


# Potentiometers
dial1 = analogio.AnalogIn(board.GP26) #was 28 pre testing hardware
dial2 = analogio.AnalogIn(board.GP28)
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


# LEDS for board & Dial 1 & 2
led0 = digitalio.DigitalInOut(board.LED)
led0.direction = digitalio.Direction.OUTPUT

button1_led = digitalio.DigitalInOut(board.GP8)
button1_led.direction = digitalio.Direction.OUTPUT

button2_led = digitalio.DigitalInOut(board.GP9)
button2_led.direction = digitalio.Direction.OUTPUT

button3_led = digitalio.DigitalInOut(board.GP10)
button3_led.direction = digitalio.Direction.OUTPUT

button4_led = digitalio.DigitalInOut(board.GP11)
button4_led.direction = digitalio.Direction.OUTPUT

button5_led = digitalio.DigitalInOut(board.GP12)
button5_led.direction = digitalio.Direction.OUTPUT

button6_led = digitalio.DigitalInOut(board.GP13)
button6_led.direction = digitalio.Direction.OUTPUT

dial1_led = digitalio.DigitalInOut(board.GP14)
dial1_led.direction = digitalio.Direction.OUTPUT

dial2_led = digitalio.DigitalInOut(board.GP15)
dial2_led.direction = digitalio.Direction.OUTPUT


# UART - MIDI port Send Only
midiuart = busio.UART(tx=board.GP4, rx=board.GP5, baudrate=31250)

currentsnapshot = 1
currentpatch = 0
tunerenabled = False


# Function Definitions:

# Lightshow for startup.
def blinkies():
    for x in range (0,8):
        dial1_led.value = True
        time.sleep(0.0015)
        button1_led.value = True
        time.sleep(0.0015)
        dial1_led.value = False
        time.sleep(0.015)
        button2_led.value = True
        time.sleep(0.015)
        button1_led.value = False
        time.sleep(0.015)
        button3_led.value = True
        time.sleep(0.015)
        button2_led.value = False
        time.sleep(0.015)
        button4_led.value = True
        time.sleep(0.015)
        button3_led.value = False
        time.sleep(0.015)
        button5_led.value = True
        time.sleep(0.015)
        button4_led.value = False
        time.sleep(0.015)
        button6_led.value = True
        time.sleep(0.015)
        button5_led.value = False
        time.sleep(0.015)
        dial2_led.value = True
        time.sleep(0.015)
        button6_led.value = False
        time.sleep(0.015)
        dial2_led.value = False
        time.sleep(0.015)

def snapshotchangeto(i):
    global currentsnapshot
    #update current snapshot and LED on.
    #accept a value of 1-3 and send a midi message with a zero indexed value (0-2)
    print('%%%%%%%%%%%%%%%%%%%%Snapshot ' + str(i))  # display a message on the terminal that it worked
    currentsnapshot = i
    midiuart.write(bytes([0xB0, 69, (i-1)])) # CC69 = 0,1, or 2 TEST THIS TODO TODO TODO
    time.sleep(0.01) # small delay to prevent multiple sends from human latency of foot press


# send new midi values of dial positions and bypass state
def dialmidiupdate():
    print('%%%%%%%%%%%%%%%%% Dials Midi Update')
    midiuart.write(bytes([0xB0, 110, dial1_midivalue]))
    midiuart.write(bytes([0xB0, 112, dial2_midivalue]))
    # update dial effect bypass state
    if (dial1_midivalue < 2):
        midiuart.write(bytes([0xB0, 111, 0]))
        dial1_led.value = False
        print('DIAL 1 MIDI BLOCK BYPASSED CC111')
    else:
        midiuart.write(bytes([0xB0, 111, 127]))
        dial1_led.value = True
        print('DIAL 1 MIDI BLOCK ACTTVE CC111')
    if (dial2_midivalue < 2):
        midiuart.write(bytes([0xB0, 113, 0]))
        dial2_led.value = False
        print('DIAL 2 MIDI BLOCK BYPASSED CC113')
    else:
        midiuart.write(bytes([0xB0, 113, 127]))
        dial2_led.value = True
        print('DIAL 2 MIDI BLOCK ACTIVE CC113')

# Program start

blinkies()

led0.value = True # use onboard led as a power indicator

snapshotchangeto(1)
dialmidiupdate()

# Main program run loop
while True:
    time.sleep(0.005) # set rate of loop to 1/200 second. Midi async bitrate is 31250bps or 3125B/sec midi messages are 3 Bytes so 1000 per second max.

# FIRST STEP, READ BUTTONS AND PROCESS SNAPSHOTS, PROGRAM CHANGES, CONTINUOUS CONTROLS
# SECOND STEP, READ AND PROCESS DIALS AND SEND APPROPREATE CC MESSAGES

    # False indicates a button press
    # Read the status of all buttons and decided what the user is trying to do
    if button1.value == False or button2.value == False or button3.value == False or button4.value == False or button5.value == False or button6.value == False:
        print('****************reading buttons')
        # Add a little delay time to allow physical button press to stabalize
        time.sleep(0.02)

        if button1.value == False:
            print('**** Button 1 pressed')
            
            #### Button for TAP/TUNER
            #Send Tap Message
            midiuart.write(bytes([0xB0, 64, 127]))
            print('TAP Sent')
            
            # Turn off tuner on first press of tap button if it is on
            if tunerenabled == True:
                print('Switching Tuner mode OFF')
                midiuart.write(bytes([0xB0, 68, 0]))
                tunerenabled = False
                button1_led.value = False
                time.sleep(0.03)
            # Flash led on each tap
            button1_led.value = True
            time.sleep(0.03)
            button1_led.value = False
            
            #button help variable to track length of hold and turn on tuner when reached
            buttonheld = 0
            while button1.value == False:
                buttonheld += 1
                if buttonheld == 10: button1_led.value = True
                time.sleep(0.05)
                if buttonheld == 10: button1_led.value = False
                if buttonheld == 20:
                    print('Switching Tuner mode ON')
                    midiuart.write(bytes([0xB0, 68, 127]))
                    tunerenabled = True
                    for x in range(0,4):
                        button1_led.value = False
                        time.sleep(0.04)
                        button1_led.value = True
                        time.sleep(0.1)
              
        elif button2.value == False:
            print('**** Button 2 pressed')
            #### BUTTON FOR CC100
            # CC100 = 0 or 127 on/off
            if button2_led.value == False:
                midiuart.write(bytes([0xB0, 100, 127]))
                button2_led.value = True
            else:
                midiuart.write(bytes([0xB0, 100, 0]))
                button2_led.value = False
            time.sleep(0.2)
            
        elif button3.value == False:
            print('**** Button 3 pressed')
            #### Button for CC101
            # CC101 = 0 or 127 on/off
            if button3_led.value == False:
                midiuart.write(bytes([0xB0, 101, 127]))
                button3_led.value = True
            else:
                midiuart.write(bytes([0xB0, 101, 0]))
                button3_led.value = False
            time.sleep(0.2)
                
        elif button4.value == False:
            print('**** Button 4 pressed')
            #### Button for CC102
            # CC102 = 0 or 127 on/off
            if button4_led.value == False:
                midiuart.write(bytes([0xB0, 102, 127]))
                button4_led.value = True
            else:
                midiuart.write(bytes([0xB0, 102, 0]))
                button4_led.value = False
            time.sleep(0.2)
            
        elif button5.value == False:
            print('**** Button 5 pressed')
            #### BUTTON FOR SNAPSHOTS
            if button5_led.value == False:
                snapshotchangeto(2)
                button5_led.value = True
            else:
                snapshotchangeto(1)
                button5_led.value = False
            time.sleep(0.17)

        elif button6.value == False:
            #### Button for PATCHES 0 index
            if currentpatch < 3:
                currentpatch +=1
            else:
                currentpatch = 0
            midiuart.write(bytes([0xC0, currentpatch]))
            button6_led.value = True
            print('CURRENTPATCH: ' + str(currentpatch))
            time.sleep(0.03)        # Add a little delay time for buttons to stabalize after release
            button6_led.value = False
            time.sleep(0.07)
        
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
        # update for next iteration
        dial1_lastvalue = dial1_currentvalue


    dial2changevalue = (dial2_currentvalue - dial2_lastvalue) / dial2_stepvalue
    if (dial2changevalue >= 1 or dial2changevalue <= -1):
        dial2_midivalue = int(dial2_currentvalue / dial2_stepvalue)
        if dial2_midivalue > 127:  # Fix for first iteration reading above 127
            dial2_midivalue = 127
        print('%%%%%%%%%%%%%%%%DIAL 2 MOVED - Midi Value: ' + str(dial2_midivalue))
        dialmidiupdate()
        # update for next iteration
        dial2_lastvalue = dial2_currentvalue
