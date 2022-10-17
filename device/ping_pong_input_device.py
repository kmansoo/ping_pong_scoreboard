import abc
from enum import Enum

class InputDeviceEvent(Enum):
    INCREASE_HOME_SCORE = 0
    DECREASE_HOME_SCORE = 1
    INCREASE_VISITOR_SCORE = 2
    DECREASE_VISITOR_SCORE = 3
    SWITCH_PLAYER_SIDE = 4
    SWITCH_SERVER = 5
    RESET_SCORE = 6
    
class InputDeviceEventListener:
    """A PingPingScoreadBoard Input Device Event Listener"""

    def on_device_new_event(self, new_event : InputDeviceEvent):
        pass
    
    def on_new_num_key(self, num_key):
        if num_key == "1":
            self.on_device_new_event(InputDeviceEvent.INCREASE_HOME_SCORE)
        # Decrease a left player score: '2'
        elif num_key == "2":
            self.on_device_new_event(InputDeviceEvent.DECREASE_HOME_SCORE)
        # Increase a right player score: '3'
        elif num_key == "3":
            self.on_device_new_event(InputDeviceEvent.INCREASE_VISITOR_SCORE)
        # Decrease a right player score: '4'
        elif num_key == "4":
            self.on_device_new_event(InputDeviceEvent.DECREASE_VISITOR_SCORE)
        # Switch a display score position for a players
        elif num_key == "5":
            self.on_device_new_event(InputDeviceEvent.SWITCH_PLAYER_SIDE)
        # Switch a server
        elif num_key == "9":
            self.on_device_new_event(InputDeviceEvent.SWITCH_SERVER)
        # Reset scores
        elif num_key == "0":
            self.on_device_new_event(InputDeviceEvent.RESET_SCORE)

class InputDevice(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_event_listener(self, listener : InputDeviceEventListener) -> None:
        raise NotImplemented

    @abc.abstractmethod
    def start_service(self) -> bool:
        raise NotImplemented

    @abc.abstractmethod
    def stop_service(self) -> bool:
        raise NotImplemented
