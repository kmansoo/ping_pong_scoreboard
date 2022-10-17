import requests

from device.ping_pong_input_device import InputDeviceEventListener, InputDeviceEvent

# from src.ir_remote_device import IRRemoteDevice
from device.dummy_device import IRRemoteDevice

global ir_device
global all_input_device_event_listener

class AllInputDeviceEventListener(InputDeviceEventListener):
    dest_ip = "localhost"
    port = 8080

    def on_device_new_event(self, new_event : InputDeviceEvent):
        event_data = None

        if new_event == InputDeviceEvent.INCREASE_HOME_SCORE:
            event_data = {"key": "1"}
        elif new_event == InputDeviceEvent.DECREASE_HOME_SCORE:
            event_data = {"key": "2"}
        elif new_event == InputDeviceEvent.INCREASE_VISITOR_SCORE:
            event_data = {"key": "3"}
        elif new_event == InputDeviceEvent.DECREASE_VISITOR_SCORE:
            event_data = {"key": "4"}
        elif new_event == InputDeviceEvent.SWITCH_PLAYER_SIDE:
            event_data = {"key": "5"}
        elif new_event == InputDeviceEvent.SWITCH_SERVER:
            event_data = {"key": "9"}
        elif new_event == InputDeviceEvent.RESET_SCORE:
            event_data = {"key": "0"}

        if event_data != None:
            requests.post("http://%s:%d/event" % (self.dest_ip, self.port), json = event_data, timeout=1)

def start_input_device_service(port, dest_ip = "localhost"):
    global ir_device
    global all_input_device_event_listener

    all_input_device_event_listener = AllInputDeviceEventListener()

    all_input_device_event_listener.dest_ip = dest_ip
    all_input_device_event_listener.port = port

    ir_device = IRRemoteDevice()
    ir_device.set_event_listener(all_input_device_event_listener)
    ir_device.start_service()

def stop_input_device_service():
    global ir_device

    ir_device.stop_service()
