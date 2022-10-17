import threading
import os
import signal

from flask import Flask, request, json, jsonify
from device.ping_pong_input_device import InputDeviceEventListener

is_work_thread_stop = False
global key_event_listener

app = Flask(__name__)

@app.route("/event", methods=['POST'])
def test():
    params = request.get_json()

    response = {
        "result": "ok"
    }

    global key_event_listener

    if key_event_listener != None and params.get("key") != None:
        key_event_listener.on_new_num_key(params["key"])
    else:
        response["result"] = "false"

    return jsonify(response)
    
def start_open_api_service(listener : InputDeviceEventListener):
    global key_event_listener
    
    key_event_listener = listener

    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)).start()

def stop_open_api_service():
    sig = getattr(signal, "SIGKILL", signal.SIGTERM)
    os.kill(os.getpid(), sig)

