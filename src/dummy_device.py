import time
import threading
import random
from src.ping_pong_input_device import InputDevice, InputDeviceEventListener, InputDeviceEvent

class IRRemoteDevice(InputDevice):
    def __init__(self) :
        self._work_thread = None
        self._event_listener = InputDeviceEventListener()

    def __del__(self):
        self.stop_service()
 
    def set_event_listener(self, listener : InputDeviceEventListener) -> None:
         self._event_listener = listener

    def start_service(self) -> bool:
        if self._work_thread != None:
            return False

        self._is_requesting_stop_thread = False

        self._work_thread = threading.Thread(target = self.__run)
        self._work_thread.start()

        return True

    def stop_service(self) -> bool:
        if self._work_thread == None:
            return False

        self._is_requesting_stop_thread = True

        self._work_thread.join()
        self._work_thread = None

        return True

    def __run(self):
        while self._is_requesting_stop_thread == False:
            # 장치에서 눌림 이벤트 확인
            # 만일 이벤트가 있다면, 다음 함수를 호출
            '''
            if event == "0":
                self._event_listener.on_device_new_event(InputDeviceEvent.INCREASE_HOME_SCORE)
            elif event == "1:
                self._event_listener.on_device_new_event(InputDeviceEvent.DECREASE_HOME_SCORE)
            ...
            '''
            # if random.randint(0, 30) == 10:
            #     key_event = random.randint(0, 9)

            #     if key_event == 0:
            #         self._event_listener.on_device_new_event(InputDeviceEvent.INCREASE_HOME_SCORE)
            #     if key_event == 2:
            #         self._event_listener.on_device_new_event(InputDeviceEvent.INCREASE_VISITOR_SCORE)
            
            time.sleep(0.01)   # 10ms  

