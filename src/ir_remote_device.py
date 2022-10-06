# import RPi.GPIO as GPIO

import pigpio
from datetime import datetime
import time
import threading
from src.ping_pong_input_device import InputDevice, InputDeviceEventListener, InputDeviceEvent

class IRRemoteDevice(InputDevice):
    def __init__(self) :
        self.pi = pigpio.pi()
        self.gpio = 18
        self.code_timeout = 5      
        self.in_code = False

        self. new_Keys={
      2209067173 : "CH-", 2475776301 : "CH", 811016773 :"CH+",
      22461621 : "PREV", 1036916573 : "NEXT", 2338142909 : "PLAY",
      383079973 : "VOL-", 2749130309 : "VOL+", 4158662973 : "EQ",
      2266238925 : "0", 3502206629 : "100+", 3131250093 : "200+",
      1902227973 : "1", 435909485 : "2", 2736323565 : "3",
      430130277 : "4", 3072262781 : "5", 3890174357 : "6",
      2890417149 : "7", 2654424341 : "8", 727043261 : "9"
   }
      
        self.pi.set_mode(18, pigpio.INPUT)

        self.cb = self.pi.callback(18, pigpio.EITHER_EDGE, self._cb)


    def __del__(self):
        pass
        # self.pi.stop()
 
    def set_event_listener(self, listener : InputDeviceEventListener) -> None:
         self._event_listener = listener

    def start_service(self) -> bool:
        # if self._work_thread != None:
            # return False

        # self._work_thread = threading.Thread(target = self.__run)
        # self._is_requesting_stop_thread = False
        # self._work_thread.start()

        return True

    def stop_service(self) -> bool:
        # if self._work_thread == None:
            # return False
        self.pi.stop()
        # self._is_requesting_stop_thread = True
        # self._work_thread.join()
        # self._work_thread = None

        return True
    def keyAction(self, hash):
        if hash in self.new_Keys:
            keyValue = self.new_Keys[hash]
            if  keyValue == "0" :
                print("step0")
                self._event_listener.on_device_new_event(InputDeviceEvent.RESET_SCORE) 
            elif keyValue == "1" :
                print("step1")
                self._event_listener.on_device_new_event(InputDeviceEvent.INCREASE_HOME_SCORE)
            elif keyValue == "2" :
                print("step2")
                self._event_listener.on_device_new_event(InputDeviceEvent.DECREASE_HOME_SCORE)
            elif keyValue == "3" :
                print("step3")
                self._event_listener.on_device_new_event(InputDeviceEvent.INCREASE_VISITOR_SCORE)
            elif keyValue == "4" :
                print("step4")
                self._event_listener.on_device_new_event(InputDeviceEvent.DECREASE_VISITOR_SCORE)
            elif keyValue == "5" :
                print("step5")
                self._event_listener.on_device_new_event(InputDeviceEvent.SWITCH_PLAYER_SIDE)
            elif keyValue == "9" :
                print("step9")
                self._event_listener.on_device_new_event(InputDeviceEvent.SWITCH_SERVER)

    def __run(self):               
        pass

    def _hash(self, old_val, new_val):
        if   new_val < (old_val * 0.60):
            val = 13
        elif old_val < (new_val * 0.60):
            val = 23
        else:
            val = 2

        self.hash_val = self.hash_val ^ val
        self.hash_val *= 16777619 # FNV_PRIME_32
        self.hash_val = self.hash_val & ((1<<32)-1)

    def _cb(self, gpio, level, tick):

        if level != pigpio.TIMEOUT:

            if self.in_code == False:
                self.in_code = True
                self.pi.set_watchdog(self.gpio, self.code_timeout)
                self.hash_val = 2166136261 # FNV_BASIS_32
                self.edges = 1
                self.t1 = None
                self.t2 = None
                self.t3 = None
                self.t4 = tick

            else:
                self.edges += 1
                self.t1 = self.t2
                self.t2 = self.t3
                self.t3 = self.t4
                self.t4 = tick

                if self.t1 is not None:
                    d1 = pigpio.tickDiff(self.t1,self.t2)
                    d2 = pigpio.tickDiff(self.t3,self.t4)
                    self._hash(d1, d2)

        else:
            if self.in_code:
                self.in_code = False
                self.pi.set_watchdog(self.gpio, 0)

                if self.edges > 12:
                    self.keyAction(self.hash_val)
   