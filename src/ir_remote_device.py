from xmlrpc.client import Boolean
import RPi.GPIO as GPIO
from datetime import datetime
import time
import threading
from src.ping_pong_input_device import InputDevice, InputDeviceEventListener, InputDeviceEvent

pin = 12


class IRRemoteDevice(InputDevice):
    def __init__(self) :
        self._work_thread = None
        self._event_listener = InputDeviceEventListener()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN)
        self.Buttons = [ 0x300ff6897, 0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5, 0x300ff42bd, 0x300ff4ab5, 0x300ff52ad, 0x300ff9867, 0x300ffb04f, 0x300ffa25d, 0x300ff629d, 0x300ffe21d, 0x300ff22dd, 0x300ff02fd, 0x300ffc23d, 0x300ffe01f, 0x300ffa857, 0x300ff906f]
        self.ButtonsNames = ["key_0", "key_1", "key_2", "key_3", "key_4", "key_5", "key_6", "key_7", "key_8", "key_9", "key_100", "key_200", "key_channeldown", "key_channel", "key_channelup", "key_prev", "key_next", "key_play", "key_minus", "key_plus", "key_equal" ]

    def __del__(self):
        self.stop_service()
 
    def set_event_listener(self, listener : InputDeviceEventListener) -> None:
         self._event_listener = listener

    def start_service(self) -> Boolean:
        if self._work_thread != None:
            return False

        self._work_thread = threading.Thread(target = self.__run)

        self._is_requesting_stop_thread = False
        self._work_thread.start()

        return True

    def stop_service(self) -> Boolean:
        if self._work_thread == None:
            return False

        self._is_requesting_stop_thread = True
        self._work_thread.join()
        self._work_thread = None

        return True

    def __run(self):
        while self._is_requesting_stop_thread == False:
            Buttons = self.getButtons()

            inData = self.convertHex(self.getBinary()) #Runs subs to get incoming hex value

            for button in range(len(Buttons)):#Runs through every value in list
                if hex(Buttons[button]) == inData: #Checks this against incoming
                    if self._event_listener != None:
                        self._event_listener.on_device_new_event(InputDeviceEvent.DECREASE_HOME_SCORE)
                    pass

            time.sleep(0.01)   # 1ms
            
            continue

    def getButtons(self) :
        return self.Buttons
    
    def getButtonsNames(self) :
        return self.ButtonsNames

    def getBinary(self) :
        num1s= 0
        binary=1  # The binary value
        command=[]  # The list to store pulse times in
        previousValue=0  # The last value
        value=GPIO.input(pin)  # The current value
        while value:
            time.sleep(0.0001) # This sleep decreases CPU utilization immensely
            value = GPIO.input(pin)
        
        startTime = datetime.now()
        while True:
            if previousValue != value:
                now = datetime.now()
                pulseTime = now - startTime #Calculate the time of pulse
                startTime = now #Reset start time
                command.append((previousValue, pulseTime.microseconds)) #Store recorded data

            if value:
                num1s += 1
            else:
                num1s = 0
            
            if num1s > 10000:
                break

            previousValue = value
            value = GPIO.input(pin)
        
        for (typ, tme) in command:
            if typ == 1: #If looking at rest period
                if tme > 1000: #If pulse greater than 1000us
                    binary = binary *10 +1 #Must be 1
                else:
                    binary *= 10 #Must be 0
        
        if len(str(binary)) > 34: #Sometimes, there is some stray characters
            binary = int(str(binary)[:34])

        return binary
	
# Convert value to hex
    def convertHex(self, binaryValue):
        tmpB2 = int(str(binaryValue),2) #Temporarely propper base 2
        return hex(tmpB2)

	
    
    def IRthreadRoutine(self):
        while True:
            inData = self.convertHex(self.getBinary()) #Runs subs to get incoming hex value
            for button in range(len(self.Buttons)):#Runs through every value in list
                if hex(self.Buttons[button]) == inData: #Checks this against incoming
                    print(self.ButtonsNames[button]) #Prints corresponding english name for button
                    # functionName(button)
    
