from enum import Enum

class InputDeviceEvent(Enum):
    INCREASE_HOME_SCORE = 0
    DECREASE_HOME_SCORE = 1
    INCREASE_VISITOR_SCORE = 2
    DECREASE_VISITOR_SCORE = 3
    SWITCH_PLAYER_SIDE = 4
    SWITCH_SERVER = 5
    RESET_SCORE = 6
    
class InputDeviceEventListener():
    """A PingPingScoreadBoard Input Device Event Listener"""

    def on_device_new_event(self, new_event : InputDeviceEvent):
        pass
