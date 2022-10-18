import threading
import json
import paho.mqtt.client as mqtt

from device.ping_pong_input_device import InputDevice, InputDeviceEventListener, InputDeviceEvent

class MQTTKeyEventDevice(InputDevice):
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

        self._client = mqtt.Client()
        self._connection_status = 0 # 0: Idel, 1: connecting, 2: connected

        self._client.on_connect = self.__mqtt_on_connect
        self._client.on_disconnect = self.__mqtt_on_disconnect
        self._client.on_subscribe = self.__mqtt_on_subscribe
        self._client.on_message = self.__mqtt_on_message

        self._client.loop_start()

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
            if self._connection_status == 0:
                self._connection_status = 1

                self._client.connect_async("localhost", port=1883, keepalive=60, bind_address="")
            else:
                time.sleep(0.01)   # 10ms

    def __mqtt_on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[MQTT] Connected to Broker")

            self._connection_status = 2

            client.subscribe('event/key', 1)
            # client.loop_forever()
        else:
            print("[MQTT] Couldn't connected to Broker")
            self._connection_status = 0


    def __mqtt_on_disconnect(self, client, userdata, flags, rc=0):
        print("[MQTT] Disconnected from Broker")

        self._connection_status = 0

    def __mqtt_on_subscribe(self, client, userdata, mid, granted_qos):
        print("[MQTT] Subscribed: MID: " + str(mid) + ", granted_qos: " + str(granted_qos))

    def __mqtt_on_message(self, client, userdata, msg):
        event_key = json.loads(msg.payload.decode("utf-8"))

        if "key" in event_key:
            self._event_listener.on_new_num_key(event_key["key"])

