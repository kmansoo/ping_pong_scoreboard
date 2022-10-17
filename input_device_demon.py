import time
import signal

from device.input_device_service import *

def handler(signum, frame):
    stop_input_device_service()
    exit(1)
 
signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    start_input_device_service(8080)

    while True:    
        time.sleep(0.01)   # 10ms
