import threading
from bluepy import btle
import time

value = [0] * 30
address = "98:CD:AC:61:DF:CA"
service_uuid = "39d65ea2-8ada-48e4-85cd-d216f7341114"
char_uuid =  "13053c07-fcbd-4886-9aa0-d903406761a2"
p = None
svc = None
ch = None

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
    def handleNotification(self, cHandle, data):
        print(data)
        print(data[0])
        value.pop(0)
        value.append(data[0])

def ThreadRoutine():
    global p
    while True:
        if p.waitForNotifications(1.0):
            continue

def startBLE():
    global address
    global service_uuid
    global char_uuid
    global p
    global svc
    global ch
    p = btle.Peripheral(address)
    p.setDelegate(MyDelegate())

    svc = p.getServiceByUUID(service_uuid)
    ch = svc.getCharacteristics(char_uuid)[0]

    setup_data = b"\x01\x00"
        #ch.write(setup_data)
    p.writeCharacteristic(ch.valHandle + 1, setup_data)
    ch_data = p.readCharacteristic(ch.valHandle + 1)
    t = threading.Thread(target=ThreadRoutine, args=())
    t.start()  
