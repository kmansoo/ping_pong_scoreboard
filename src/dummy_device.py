import time
import threading
from xmlrpc.client import Boolean
from src.ping_pong_input_device import InputDevice, InputDeviceEventListener, InputDeviceEvent

class IRRemoteDevice(InputDevice):
    def __init__(self) :
        self._work_thread = None
        self._event_listener = InputDeviceEventListener()

    def __del__(self):
        self.stop_service()
 
    def set_event_listener(self, listener : InputDeviceEventListener) -> None:
         self._event_listener = listener

    def start_service(self) -> Boolean:
        if self._work_thread != None:
            return False

        self._is_requesting_stop_thread = False

        self._work_thread = threading.Thread(target = self.__run)
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
            time.sleep(0.01)   # 10ms  
