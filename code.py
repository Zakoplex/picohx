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
dial1 = analogio.AnalogIn(board.GP26)
dial2 = analogio.AnalogIn(board.GP28)

# initial pre-calibration values with diminished range which get expanded with auto-calibraion if larger range detected
dial1_minvalue = 500
dial1_maxvalue = 65000
dial1_stepvalue = 500
dial1_midivalue = 64

dial2_minvalue = 500
dial2_maxvalue = 65000
dial2_stepvalue = 500
dial2_midivalue = 64

# LEDS
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
    blinkiespeed = 0.062
    for x in range (0,10):
        if blinkiespeed > 0.01: blinkiespeed -= 0.01
        dial1_led.value = True
        time.sleep(blinkiespeed)
        button1_led.value = True
        time.sleep(blinkiespeed)
        dial1_led.value = False
        time.sleep(blinkiespeed)
        button2_led.value = True
        time.sleep(blinkiespeed)
        button1_led.value = False
        time.sleep(blinkiespeed)
        button3_led.value = True
        time.sleep(blinkiespeed)
        button2_led.value = False
        time.sleep(blinkiespeed)
        button4_led.value = True
        time.sleep(blinkiespeed)
        button3_led.value = False
        time.sleep(blinkiespeed)
        button5_led.value = True
        time.sleep(blinkiespeed)
        button4_led.value = False
        time.sleep(blinkiespeed)
        button6_led.value = True
        time.sleep(blinkiespeed)
        button5_led.value = False
        time.sleep(blinkiespeed)
        dial2_led.value = True
        time.sleep(blinkiespeed)
        button6_led.value = False
        time.sleep(blinkiespeed)
        dial2_led.value = False
        time.sleep(blinkiespeed)

def snapshotchangeto(i):
    global currentsnapshot
    #update current snapshot and LED on.
    #accept a value of 1-3 and send a midi message with a zero indexed value (0-2)
    print('%%%% Snapshot ' + str(i))  # display a message on the terminal that it worked
    currentsnapshot = i
    midiuart.write(bytes([0xB0, 69, (i-1)])) # CC69 = 0,1, or 2
    time.sleep(0.01) # small delay to prevent multiple sends from human latency of foot press


# send new midi values of dial positions and bypass state
def dialmidiupdate():
    print('%%%% Dials Midi Update')
    midiuart.write(bytes([0xB0, 110, dial1_midivalue]))
    midiuart.write(bytes([0xB0, 112, dial2_midivalue]))
    # update dial effect bypass state
    if (dial1_midivalue < 1):
        midiuart.write(bytes([0xB0, 111, 0]))
        dial1_led.value = False
        # print('DIAL 1 MIDI BLOCK BYPASSED CC111')
    else:
        midiuart.write(bytes([0xB0, 111, 127]))
        dial1_led.value = True
        # print('DIAL 1 MIDI BLOCK ACTTVE CC111')
    if (dial2_midivalue < 1):
        midiuart.write(bytes([0xB0, 113, 0]))
        dial2_led.value = False
        # print('DIAL 2 MIDI BLOCK BYPASSED CC113')
    else:
        midiuart.write(bytes([0xB0, 113, 127]))
        dial2_led.value = True
        # print('DIAL 2 MIDI BLOCK ACTIVE CC113')

# turn off effects buttons and send midi off states (buttons 2-4)
def effectsbuttonsoff():
    print('%%%% Effects buttons off')
    midiuart.write(bytes([0xB0, 100, 0]))
    button2_led.value = False
    midiuart.write(bytes([0xB0, 101, 0]))
    button3_led.value = False
    midiuart.write(bytes([0xB0, 102, 0]))
    button4_led.value = False

# Program start

blinkies()

led0.value = True # use onboard led as a power indicator

snapshotchangeto(1)
dialmidiupdate()

# Main program run loop
while True:
    time.sleep(0.0025) # set rate of loop to 1/400 second. Midi async bitrate is 31250bps or 3125B/sec midi messages are 3 Bytes so 1000 per second max.
    #time.sleep(1) # DEBUG RATE SET

# FIRST STEP, READ BUTTONS AND PROCESS SNAPSHOTS, PROGRAM CHANGES, CONTINUOUS CONTROLS
# SECOND STEP, READ AND PROCESS DIALS AND SEND APPROPREATE CC MESSAGES

    # False indicates a button press
    # Read the status of all buttons and decided what the user is trying to do
    if button1.value == False or button2.value == False or button3.value == False or button4.value == False or button5.value == False or button6.value == False:
        print('**** reading buttons')
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

            # Flash led on each tap
            button1_led.value = True
            time.sleep(0.02)
            button1_led.value = False

            #button help variable to track length of hold and turn on tuner when reached
            buttonheld = 0
            while button1.value == False:
                buttonheld += 1
                time.sleep(0.04)
                if buttonheld == 20:
                    print('Switching Tuner mode ON')
                    midiuart.write(bytes([0xB0, 68, 127]))
                    tunerenabled = True
                    for x in range(0,6):
                        button1_led.value = False
                        time.sleep(0.05)
                        button1_led.value = True
                        time.sleep(0.02)

        elif button2.value == False:
            print('**** Button 2 pressed')
            #### BUTTON FOR CC100
            # CC100 = 0 or 127 on/off
            if button2_led.value == False:
                midiuart.write(bytes([0xB0, 100, 127]))
                button2_led.value = True
                print("MIDI CC100 ON")
            else:
                midiuart.write(bytes([0xB0, 100, 0]))
                button2_led.value = False
                print("MIDI CC100 OFF")
            time.sleep(0.2)

        elif button3.value == False:
            print('**** Button 3 pressed')
            #### Button for CC101
            # CC101 = 0 or 127 on/off
            if button3_led.value == False:
                midiuart.write(bytes([0xB0, 101, 127]))
                button3_led.value = True
                print("MIDI CC101 ON")
            else:
                midiuart.write(bytes([0xB0, 101, 0]))
                button3_led.value = False
                print("MIDI CC101 OFF")
            time.sleep(0.2)

        elif button4.value == False:
            print('**** Button 4 pressed')
            #### Button for CC102
            # CC102 = 0 or 127 on/off
            if button4_led.value == False:
                midiuart.write(bytes([0xB0, 102, 127]))
                button4_led.value = True
                print("MIDI CC102 ON")
            else:
                midiuart.write(bytes([0xB0, 102, 0]))
                button4_led.value = False
                print("MIDI CC102 OFF")
            time.sleep(0.2)

        elif button5.value == False:
            print('**** Button 5 pressed')
            #### BUTTON FOR SNAPSHOTS
            if button5_led.value == False:
                snapshotchangeto(2)
                #update dial values after snapshot change
                dialmidiupdate()
                button5_led.value = True
            else:
                snapshotchangeto(1)
                dialmidiupdate()
                button5_led.value = False
            time.sleep(0.2)

        elif button6.value == False:
            #### Button for PATCHES 0 index
            if currentpatch < 3:
                currentpatch +=1
            else:
                currentpatch = 0
            midiuart.write(bytes([0xC0, currentpatch]))
            #update dial values after patch change
            dialmidiupdate()
            #turn off effects buttons with patch change
            effectsbuttonsoff()
            button6_led.value = True
            print('CURRENTPATCH: ' + str(currentpatch))
            # Add a little delay time for buttons to stabalize after release and for a LED blinks
            time.sleep(0.02)
            button6_led.value = False
            time.sleep(0.05)
            button6_led.value = True
            time.sleep(0.02)
            button6_led.value = False

            #allow for slower scrolling and extra time to stablize on a slow button press
            if button6.value == False:
                time.sleep(0.1)

        time.sleep(0.06)

# SECOND STEP DIAL PROCESSING:
#    print(str(dial1.value) + " " + str(dial1_stepvalue)) # FOR DEBUG TO VIEW ACTUAL VALUES OF POTS
#    print(str(dial2.value) + " " + str(dial2_stepvalue)) # FOR DEBUG TO VIEW ACTUAL VALUES OF POTS
#    time.sleep(0.5) # FOR DEBUG TO VIEW ACTUAL VALUES OF POTS

    # Check current max and min values for dials and auto-calibrate
    if dial1.value < dial1_minvalue:
        dial1_minvalue = dial1.value

    if dial1.value > dial1_maxvalue:
        dial1_maxvalue = dial1.value

    if dial2.value < dial2_minvalue:
        dial2_minvalue = dial2.value

    if dial2.value > dial2_maxvalue:
        dial2_maxvalue = dial2.value

    # recaltulate step values
    dial1_stepvalue = int((dial1_maxvalue - dial1_minvalue) / 127)
    dial2_stepvalue = int((dial2_maxvalue - dial2_minvalue) / 127)

    # THE CURRENT VALUE OF THE DIAL HAS CHANGED MORE THAN A STEP VALUE UP OR DOWN THEN UPDATE THE LAST VALUE & SEND A CC for value and bypass
    # read dial value once for use in following calculations to prevent jitter from having different results in multiple comparisons
    dial1current = dial1.value
    dial2current = dial2.value
    dial1selectedmidi = int(dial1current / dial1_stepvalue)
    dial2selectedmidi = int(dial2current / dial2_stepvalue)

    # Only send midi dial is more than 1.5 step values from current raw value.  Pots jitter more than one step and spam midi outherwise.
    if dial1current <  ((dial1_midivalue * dial1_stepvalue) - (1.75 * dial1_stepvalue)) or dial1current > ((dial1_midivalue * dial1_stepvalue) + (1.75 * dial1_stepvalue)):
        print('%%%% DIAL 1 MOVED')
        dial1_midivalue = dial1selectedmidi

        # Sticky for midi values of 0 or 127 and prevent invalid midi values
        if dial1selectedmidi <= 1:
            print("Sticky dial1 low")
            dial1_midivalue = 0
        if dial1selectedmidi >=126:
            print("Sticky dial1 high")
            dial1_midivalue = 127

        dialmidiupdate()

        # FOR DEBUG TO VIEW ACTUAL VALUES OF POTS
        print("Min Val: " + str(dial1_minvalue))
        print("Current: " + str(dial1current))
        print("Max Val: " + str(dial1_maxvalue))
        print("Step   : " + str(dial1_stepvalue))
        print("Select : " + str(dial1selectedmidi))
        print("MIDI   : " + str(dial1_midivalue))
        print("")


    if dial2current <  ((dial2_midivalue * dial2_stepvalue) - (1.75 * dial2_stepvalue)) or dial2current >  ((dial2_midivalue * dial2_stepvalue) + (1.75 * dial2_stepvalue)):
        print('%%%% DIAL 2 MOVED')
        dial2_midivalue = dial2selectedmidi

         # Sticky for midi values of 0 or 127
        if dial2selectedmidi <= 1:
            print("Sticky dial1 low")
            dial2_midivalue = 0
        if dial2selectedmidi >=126:
            print("Sticky dial1 high")
            dial2_midivalue = 127

        dialmidiupdate()

        print("Min Val: " + str(dial2_minvalue))
        print("Current: " + str(dial2current))
        print("Max Val: " + str(dial2_maxvalue))
        print("Step   : " + str(dial2_stepvalue))
        print("Select : " + str(dial2selectedmidi))
        print("MIDI   : " + str(dial2_midivalue))
        print("")


